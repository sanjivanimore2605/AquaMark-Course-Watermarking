import os
import uuid
import fitz  # PyMuPDF
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.models import Document, User
from app.schemas.schemas import DocumentResponse
from app.security.deps import get_current_user
from app.cryptography.engine import calculate_sha256
from app.services.audit import log_audit_event

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Validate extension and content type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    stored_name = f"{uuid.uuid4()}.pdf"
    file_path = os.path.join(settings.UPLOAD_DIR, stored_name)
    
    # Write in chunks and calculate size
    size = 0
    with open(file_path, "wb") as buffer:
        while chunk := await file.read(65536):
            size += len(chunk)
            if size > settings.MAX_UPLOAD_SIZE_BYTES:
                buffer.close()
                if os.path.exists(file_path):
                    os.remove(file_path)
                raise HTTPException(status_code=400, detail="File size exceeds maximum limit (25MB).")
            buffer.write(chunk)
            
    # Validate PDF structure safely using PyMuPDF
    try:
        doc = fitz.open(file_path)
        page_count = len(doc)
        doc.close()
        if page_count < 1:
            raise ValueError("Empty PDF")
        if page_count > settings.MAX_PAGE_COUNT:
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=400, detail=f"PDF page count exceeds maximum allowable limit of {settings.MAX_PAGE_COUNT}.")
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=400, detail=f"Corrupt or malformed PDF: {str(e)}")
        
    # Calculate SHA-256
    file_sha256 = calculate_sha256(file_path)
    
    # Store record
    document = Document(
        title=file.filename.rsplit(".", 1)[0],
        original_filename=file.filename,
        stored_original_filename=stored_name,
        file_size_bytes=size,
        page_count=page_count,
        original_sha256=file_sha256,
        owner_id=current_user.id
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    
    log_audit_event(
        db,
        "DOCUMENT_UPLOAD",
        actor_id=current_user.id,
        document_id=document.id,
        details={"filename": file.filename, "sha256": file_sha256, "pages": page_count}
    )
    return document

@router.get("", response_model=List[DocumentResponse])
def list_documents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    docs = db.query(Document).filter(Document.owner_id == current_user.id).order_by(Document.created_at.desc()).all()
    for d in docs:
        d.watermark_records_count = len(d.watermark_records)
    return docs

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")
    if doc.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized access to this document.")
    doc.watermark_records_count = len(doc.watermark_records)
    return doc

@router.get("/{document_id}/download-original")
def download_original(document_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")
    if doc.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized access to this document.")
        
    path = os.path.join(settings.UPLOAD_DIR, doc.stored_original_filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found on storage disk.")
    return FileResponse(path, filename=doc.original_filename, media_type="application/pdf")

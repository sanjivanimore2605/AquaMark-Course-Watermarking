import os
import uuid
import json
from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, Response
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.models import Document, WatermarkRecord, User
from app.schemas.schemas import ApplyWatermarkRequest, WatermarkRecordResponse
from app.security.deps import get_current_user
from app.watermarking.visible import apply_visible_watermark
from app.watermarking.invisible_dct import apply_invisible_watermark_pdf
from app.cryptography.engine import (
    calculate_sha256,
    calculate_hmac_sha256,
    sign_canonical_manifest,
    get_or_create_system_keypair,
    SYSTEM_KEY_ID
)
from app.services.audit import log_audit_event

router = APIRouter(prefix="/watermarks", tags=["Watermarking"])

@router.post("/apply", response_model=WatermarkRecordResponse, status_code=status.HTTP_201_CREATED)
def apply_watermark(
    req: ApplyWatermarkRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    doc = db.query(Document).filter(Document.id == req.document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")
    if doc.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized access to document.")
        
    input_path = os.path.join(settings.UPLOAD_DIR, doc.stored_original_filename)
    if not os.path.exists(input_path):
        raise HTTPException(status_code=404, detail="Original document file not found on storage.")
        
    protected_filename = f"protected_{uuid.uuid4()}.pdf"
    output_path = os.path.join(settings.PROTECTED_DIR, protected_filename)
    
    algorithm_name = ""
    if req.watermark_type == "visible":
        algorithm_name = "Visible-AlphaOverlay-v1"
        subtext = req.subtext or (f"Recipient: {req.recipient_identifier}" if req.recipient_identifier else "")
        apply_visible_watermark(
            input_pdf_path=input_path,
            output_pdf_path=output_path,
            text=req.text,
            subtext=subtext,
            opacity=req.opacity or 0.3,
            font_size=req.font_size or 36.0,
            rotation=req.rotation or 45.0
        )
    elif req.watermark_type == "invisible_dct":
        algorithm_name = "DCT-SpreadSpectrum-v1"
        payload = req.text
        if req.recipient_identifier:
            payload = f"{req.text}:{req.recipient_identifier}"
        apply_invisible_watermark_pdf(
            input_pdf_path=input_path,
            output_pdf_path=output_path,
            payload_text=payload
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid watermark type. Must be 'visible' or 'invisible_dct'.")
        
    # Calculate integrity & hashes
    protected_size = os.path.getsize(output_path)
    protected_sha256 = calculate_sha256(output_path)
    hmac_val = calculate_hmac_sha256(settings.SECRET_KEY, f"{doc.original_sha256}:{protected_sha256}")
    
    # Generate cryptographic manifest
    manifest_id = f"manifest_{uuid.uuid4()}"
    created_iso = datetime.now(timezone.utc).isoformat()
    manifest_dict = {
        "manifest_version": "1.0",
        "manifest_id": manifest_id,
        "document_id": doc.id,
        "document_title": doc.title,
        "original_sha256": doc.original_sha256,
        "protected_sha256": protected_sha256,
        "hmac_sha256": hmac_val,
        "watermark_type": req.watermark_type,
        "watermark_algorithm": algorithm_name,
        "payload_text": req.text,
        "recipient_identifier": req.recipient_identifier,
        "issuer_id": current_user.id,
        "issuer_email": current_user.email,
        "signing_key_id": SYSTEM_KEY_ID,
        "timestamp_utc": created_iso
    }
    
    # Sign manifest with Ed25519 system authority
    priv_pem, pub_pem = get_or_create_system_keypair()
    digital_sig = sign_canonical_manifest(priv_pem, manifest_dict)
    
    # Save record
    wm_record = WatermarkRecord(
        document_id=doc.id,
        watermark_type=req.watermark_type,
        watermark_algorithm=algorithm_name,
        algorithm_version="1.0.0",
        payload_text=req.text,
        recipient_identifier=req.recipient_identifier,
        recipient_email=req.recipient_email,
        stored_protected_filename=protected_filename,
        protected_file_size_bytes=protected_size,
        protected_sha256=protected_sha256,
        hmac_sha256=hmac_val,
        manifest_id=manifest_id,
        manifest_json=json.dumps(manifest_dict),
        digital_signature=digital_sig,
        signing_key_id=SYSTEM_KEY_ID
    )
    db.add(wm_record)
    db.commit()
    db.refresh(wm_record)
    
    log_audit_event(
        db,
        "WATERMARK_APPLY",
        actor_id=current_user.id,
        document_id=doc.id,
        details={
            "type": req.watermark_type,
            "manifest_id": manifest_id,
            "recipient_id": req.recipient_identifier
        }
    )
    return wm_record

@router.get("/records/{record_id}", response_model=WatermarkRecordResponse)
def get_watermark_record(record_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rec = db.query(WatermarkRecord).filter(WatermarkRecord.id == record_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Watermark record not found.")
    if rec.document.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized.")
    return rec

@router.get("/records/{record_id}/download")
def download_protected_pdf(record_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rec = db.query(WatermarkRecord).filter(WatermarkRecord.id == record_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Watermark record not found.")
    if rec.document.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized.")
        
    path = os.path.join(settings.PROTECTED_DIR, rec.stored_protected_filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File missing from disk.")
    download_name = f"AquaMark_Secured_{rec.document.original_filename}"
    return FileResponse(path, filename=download_name, media_type="application/pdf")

@router.get("/records/{record_id}/manifest")
def download_manifest_json(record_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rec = db.query(WatermarkRecord).filter(WatermarkRecord.id == record_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Watermark record not found.")
    if rec.document.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized.")
        
    manifest_data = json.loads(rec.manifest_json)
    manifest_data["digital_signature"] = rec.digital_signature
    return Response(content=json.dumps(manifest_data, indent=2), media_type="application/json")

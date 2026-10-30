import os
import json
import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.responses import FileResponse, Response
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.models import Document, WatermarkRecord, VerificationRecord, User
from app.schemas.schemas import VerificationResultResponse
from app.security.deps import get_current_user_optional
from app.cryptography.engine import (
    calculate_sha256,
    verify_manifest_signature,
    get_or_create_system_keypair,
    SYSTEM_KEY_ID
)
from app.watermarking.invisible_dct import detect_invisible_watermark_pdf
from app.services.audit import log_audit_event
from app.reports.pdf_generator import generate_pdf_verification_report

router = APIRouter(prefix="/verify", tags=["Verification"])

@router.post("", response_model=VerificationResultResponse)
async def verify_document(
    file: UploadFile = File(...),
    manifest_file: Optional[UploadFile] = File(None),
    manifest_text: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    # Save candidate file temporarily
    temp_candidate = os.path.join("/tmp", f"cand_{uuid.uuid4()}.pdf")
    with open(temp_candidate, "wb") as f:
        while chunk := await file.read(65536):
            f.write(chunk)
            
    candidate_hash = calculate_sha256(temp_candidate)
    
    # Parse manifest if provided
    parsed_manifest = None
    if manifest_file:
        try:
            content = await manifest_file.read()
            parsed_manifest = json.loads(content.decode("utf-8"))
        except Exception:
            pass
    elif manifest_text:
        try:
            parsed_manifest = json.loads(manifest_text)
        except Exception:
            pass
            
    # Search DB by candidate hash or manifest
    watermark_rec = None
    exact_hash_match = False
    
    if parsed_manifest and "manifest_id" in parsed_manifest:
        watermark_rec = db.query(WatermarkRecord).filter(WatermarkRecord.manifest_id == parsed_manifest["manifest_id"]).first()
    
    if not watermark_rec:
        # Search by exact protected SHA-256 match
        watermark_rec = db.query(WatermarkRecord).filter(WatermarkRecord.protected_sha256 == candidate_hash).first()
        if watermark_rec:
            exact_hash_match = True
            parsed_manifest = json.loads(watermark_rec.manifest_json)
            parsed_manifest["digital_signature"] = watermark_rec.digital_signature
            
    # Evaluate Signature and Keys
    signature_valid = False
    signing_key_trusted = False
    manifest_id_val = None
    signing_key_id_val = None
    
    if parsed_manifest:
        manifest_id_val = parsed_manifest.get("manifest_id")
        signing_key_id_val = parsed_manifest.get("signing_key_id")
        sig_b64 = parsed_manifest.get("digital_signature")
        
        # Strip signature field before evaluating canonical signature
        manifest_copy = {k: v for k, v in parsed_manifest.items() if k != "digital_signature"}
        
        # Check against trusted authority key
        _, system_pub_pem = get_or_create_system_keypair()
        if signing_key_id_val == SYSTEM_KEY_ID:
            signing_key_trusted = True
            if sig_b64:
                signature_valid = verify_manifest_signature(system_pub_pem, manifest_copy, sig_b64)
                
        # Also check hash match from manifest
        if parsed_manifest.get("protected_sha256") == candidate_hash:
            exact_hash_match = True
            
    # Evaluate Digital Watermark Presence
    dct_result = detect_invisible_watermark_pdf(temp_candidate)
    watermark_detected = dct_result.get("detected", False)
    extracted_payload = dct_result.get("extracted_payload")
    
    payload_match = False
    if watermark_rec and extracted_payload:
        if watermark_rec.payload_text in extracted_payload:
            payload_match = True
    elif parsed_manifest and extracted_payload:
        if parsed_manifest.get("payload_text", "") in extracted_payload:
            payload_match = True

    # Determine Summary Status Verdict
    if exact_hash_match and signature_valid and signing_key_trusted:
        status_summary = "AUTHENTIC_EXACT_MATCH"
    elif watermark_detected and payload_match and signature_valid:
        status_summary = "AUTHENTIC_WATERMARK_CONFIRMED"
    elif exact_hash_match:
        status_summary = "AUTHENTIC_HASH_MATCH_NO_SIGNATURE"
    elif signature_valid and not exact_hash_match:
        status_summary = "TAMPERED_DOCUMENT_MODIFIED"
    elif not signing_key_trusted and parsed_manifest:
        status_summary = "UNTRUSTED_SIGNING_AUTHORITY"
    else:
        status_summary = "UNREGISTERED_OR_ALTERED"

    full_report = {
        "status_summary": status_summary,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "candidate_filename": file.filename,
        "candidate_sha256": candidate_hash,
        "exact_hash_match": exact_hash_match,
        "signature_valid": signature_valid,
        "signing_key_trusted": signing_key_trusted,
        "signing_key_id": signing_key_id_val,
        "manifest_id": manifest_id_val,
        "watermark_algorithm": watermark_rec.watermark_algorithm if watermark_rec else "Unknown/Forensic Scan",
        "watermark_detected": watermark_detected,
        "watermark_payload_match": payload_match,
        "extracted_payload": extracted_payload,
        "recipient_identifier": watermark_rec.recipient_identifier if watermark_rec else parsed_manifest.get("recipient_identifier") if parsed_manifest else None
    }

    # Store verification record
    v_record = VerificationRecord(
        document_id=watermark_rec.document_id if watermark_rec else None,
        watermark_record_id=watermark_rec.id if watermark_rec else None,
        verified_by_user_id=current_user.id if current_user else None,
        candidate_filename=file.filename,
        candidate_sha256=candidate_hash,
        exact_hash_match=exact_hash_match,
        signature_valid=signature_valid,
        signing_key_trusted=signing_key_trusted,
        watermark_detected=watermark_detected,
        watermark_payload_match=payload_match,
        extracted_payload=extracted_payload,
        status_summary=status_summary,
        full_report_json=json.dumps(full_report)
    )
    db.add(v_record)
    db.commit()
    db.refresh(v_record)
    
    # Cleanup temp file
    if os.path.exists(temp_candidate):
        os.remove(temp_candidate)
        
    log_audit_event(
        db,
        "DOCUMENT_VERIFY",
        actor_id=current_user.id if current_user else None,
        document_id=watermark_rec.document_id if watermark_rec else None,
        details={"verdict": status_summary, "sha256": candidate_hash}
    )
    
    return {
        "id": v_record.id,
        "candidate_filename": v_record.candidate_filename,
        "candidate_sha256": v_record.candidate_sha256,
        "exact_hash_match": v_record.exact_hash_match,
        "signature_valid": v_record.signature_valid,
        "signing_key_trusted": v_record.signing_key_trusted,
        "watermark_detected": v_record.watermark_detected,
        "watermark_payload_match": v_record.watermark_payload_match,
        "extracted_payload": v_record.extracted_payload,
        "status_summary": v_record.status_summary,
        "full_report": full_report,
        "created_at": v_record.created_at
    }

@router.get("/reports/{report_id}/pdf")
def download_verification_report_pdf(report_id: str, db: Session = Depends(get_db)):
    rec = db.query(VerificationRecord).filter(VerificationRecord.id == report_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Verification report not found.")
        
    report_data = json.loads(rec.full_report_json)
    output_pdf_path = os.path.join(settings.BASE_STORAGE_PATH, f"report_{rec.id}.pdf")
    generate_pdf_verification_report(report_data, output_pdf_path)
    
    return FileResponse(output_pdf_path, filename=f"AquaMark_Certificate_{rec.id}.pdf", media_type="application/pdf")

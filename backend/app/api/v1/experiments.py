import os
import json
import fitz
from PIL import Image
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.models import WatermarkRecord, RobustnessExperiment, User
from app.schemas.schemas import RobustnessExperimentRequest, RobustnessExperimentResponse
from app.security.deps import get_current_user
from app.watermarking.robustness import run_single_experiment
from app.services.audit import log_audit_event

router = APIRouter(prefix="/experiments", tags=["Robustness Lab"])

@router.post("/run", response_model=RobustnessExperimentResponse, status_code=status.HTTP_201_CREATED)
def run_robustness_test(
    req: RobustnessExperimentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    wm = db.query(WatermarkRecord).filter(WatermarkRecord.id == req.watermark_record_id).first()
    if not wm:
        raise HTTPException(status_code=404, detail="Watermark record not found.")
        
    doc_path = os.path.join(settings.UPLOAD_DIR, wm.document.stored_original_filename)
    if not os.path.exists(doc_path):
        raise HTTPException(status_code=404, detail="Carrier document file missing from disk.")
        
    # Render page 1 as carrier image
    doc = fitz.open(doc_path)
    page = doc[0]
    pix = page.get_pixmap(dpi=150)
    carrier_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    doc.close()
    
    # Run trial
    result = run_single_experiment(
        carrier_image=carrier_img,
        payload_text=wm.payload_text,
        transformation_type=req.transformation_type,
        intensity=req.intensity
    )
    
    exp = RobustnessExperiment(
        watermark_record_id=wm.id,
        transformation_type=req.transformation_type,
        transformation_params_json=json.dumps({"intensity": req.intensity}),
        detected=result["detected"],
        payload_recovered=result["payload_recovered"],
        bit_error_rate=result["bit_error_rate"],
        extracted_payload=result["extracted_payload"],
        psnr_db=result["psnr_db"],
        execution_duration_ms=result["duration_ms"]
    )
    db.add(exp)
    db.commit()
    db.refresh(exp)
    
    log_audit_event(
        db,
        "ROBUSTNESS_EXPERIMENT",
        actor_id=current_user.id,
        document_id=wm.document_id,
        details={"transformation": req.transformation_type, "recovered": result["payload_recovered"]}
    )
    
    return exp

@router.get("/history/{watermark_record_id}", response_model=List[RobustnessExperimentResponse])
def get_experiment_history(
    watermark_record_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(RobustnessExperiment).filter(
        RobustnessExperiment.watermark_record_id == watermark_record_id
    ).order_by(RobustnessExperiment.created_at.desc()).all()

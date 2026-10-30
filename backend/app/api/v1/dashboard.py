import json
from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Document, WatermarkRecord, VerificationRecord, AuditEvent, User
from app.security.deps import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Dict[str, Any]:
    # Query user metrics
    user_docs_count = db.query(Document).filter(Document.owner_id == current_user.id).count()
    
    user_wm_count = db.query(WatermarkRecord).join(Document).filter(
        Document.owner_id == current_user.id
    ).count()
    
    verifications_count = db.query(VerificationRecord).count()
    
    # Recent documents
    recent_docs = db.query(Document).filter(
        Document.owner_id == current_user.id
    ).order_by(Document.created_at.desc()).limit(5).all()
    
    # Watermark type distribution
    visible_count = db.query(WatermarkRecord).join(Document).filter(
        Document.owner_id == current_user.id,
        WatermarkRecord.watermark_type == "visible"
    ).count()
    
    invisible_count = db.query(WatermarkRecord).join(Document).filter(
        Document.owner_id == current_user.id,
        WatermarkRecord.watermark_type == "invisible_dct"
    ).count()
    
    # Recent audit trail
    recent_audits = db.query(AuditEvent).order_by(AuditEvent.timestamp.desc()).limit(8).all()
    
    return {
        "total_documents": user_docs_count,
        "total_watermarked": user_wm_count,
        "total_verifications": verifications_count,
        "watermark_breakdown": {
            "visible": visible_count,
            "invisible_dct": invisible_count
        },
        "recent_documents": [
            {
                "id": d.id,
                "title": d.title,
                "original_filename": d.original_filename,
                "page_count": d.page_count,
                "created_at": d.created_at.isoformat()
            } for d in recent_docs
        ],
        "recent_audit_trail": [
            {
                "id": a.id,
                "event_type": a.event_type,
                "status": a.status,
                "timestamp": a.timestamp.isoformat(),
                "current_hash": a.current_hash[:16] + "..."
            } for a in recent_audits
        ]
    }

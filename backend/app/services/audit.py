import json
from typing import Optional, Any
from sqlalchemy.orm import Session
from app.models.models import AuditEvent
from app.cryptography.engine import calculate_sha256_bytes

def log_audit_event(
    db: Session,
    event_type: str,
    actor_id: Optional[str] = None,
    document_id: Optional[str] = None,
    status: str = "SUCCESS",
    details: Optional[dict] = None,
    ip_address: Optional[str] = None
) -> AuditEvent:
    """
    Creates a tamper-evident chained audit event record.
    The current hash incorporates the previous event's hash, forming a cryptographic hash chain.
    """
    last_event = db.query(AuditEvent).order_by(AuditEvent.timestamp.desc()).first()
    prev_hash = last_event.current_hash if last_event else "0" * 64
    
    details_str = json.dumps(details or {}, sort_keys=True)
    chain_payload = f"{prev_hash}:{actor_id or 'SYSTEM'}:{event_type}:{status}:{details_str}"
    current_hash = calculate_sha256_bytes(chain_payload.encode("utf-8"))
    
    event = AuditEvent(
        actor_id=actor_id,
        event_type=event_type,
        document_id=document_id,
        status=status,
        details_json=details_str,
        previous_hash=prev_hash,
        current_hash=current_hash,
        ip_address=ip_address
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

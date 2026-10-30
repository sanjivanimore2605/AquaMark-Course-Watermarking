import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    institution = Column(String(255), nullable=True)
    role = Column(String(50), default="instructor", nullable=False)  # instructor, student, admin
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)
    
    # Relationships
    documents = relationship("Document", back_populates="owner", cascade="all, delete-orphan")
    audit_events = relationship("AuditEvent", back_populates="actor")
    signing_keys = relationship("SigningKey", back_populates="user")

class SigningKey(Base):
    __tablename__ = "signing_keys"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    key_id = Column(String(100), unique=True, index=True, nullable=False)
    algorithm = Column(String(50), default="Ed25519", nullable=False)
    public_key_pem = Column(Text, nullable=False)
    private_key_encrypted = Column(Text, nullable=False)  # Encrypted with server master key
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    revoked_at = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="signing_keys")

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    stored_original_filename = Column(String(255), nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    page_count = Column(Integer, nullable=False)
    original_sha256 = Column(String(64), index=True, nullable=False)
    owner_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="documents")
    watermark_records = relationship("WatermarkRecord", back_populates="document", cascade="all, delete-orphan")
    verification_records = relationship("VerificationRecord", back_populates="document", cascade="all, delete-orphan")

class WatermarkRecord(Base):
    __tablename__ = "watermark_records"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=False)
    watermark_type = Column(String(50), nullable=False)  # visible, invisible_dct, hybrid
    watermark_algorithm = Column(String(100), nullable=False)  # e.g., DCT-SpreadSpectrum-v1, Visible-AlphaOverlay-v1
    algorithm_version = Column(String(20), default="1.0.0", nullable=False)
    
    # Watermark configuration / payload parameters (stored safely)
    payload_text = Column(String(255), nullable=False)
    recipient_identifier = Column(String(100), index=True, nullable=True)
    recipient_email = Column(String(255), nullable=True)
    
    # Output file and integrity
    stored_protected_filename = Column(String(255), nullable=False)
    protected_file_size_bytes = Column(Integer, nullable=False)
    protected_sha256 = Column(String(64), index=True, nullable=False)
    hmac_sha256 = Column(String(64), nullable=False)
    
    # Cryptographic Manifest linkage
    manifest_id = Column(String(100), unique=True, index=True, nullable=False)
    manifest_json = Column(Text, nullable=False)
    digital_signature = Column(Text, nullable=False)
    signing_key_id = Column(String(100), nullable=False)
    
    created_at = Column(DateTime, default=utc_now, nullable=False)
    
    document = relationship("Document", back_populates="watermark_records")
    verification_records = relationship("VerificationRecord", back_populates="watermark_record")

class VerificationRecord(Base):
    __tablename__ = "verification_records"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=True)
    watermark_record_id = Column(String(36), ForeignKey("watermark_records.id"), nullable=True)
    verified_by_user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    
    candidate_filename = Column(String(255), nullable=False)
    candidate_sha256 = Column(String(64), nullable=False)
    
    # Verification checks
    exact_hash_match = Column(Boolean, default=False, nullable=False)
    signature_valid = Column(Boolean, default=False, nullable=False)
    signing_key_trusted = Column(Boolean, default=False, nullable=False)
    watermark_detected = Column(Boolean, default=False, nullable=False)
    watermark_payload_match = Column(Boolean, default=False, nullable=False)
    extracted_payload = Column(String(255), nullable=True)
    
    status_summary = Column(String(100), nullable=False)  # AUTHENTIC_EXACT, AUTHENTIC_WATERMARK_CONFIRMED, TAMPERED_SIGNATURE_FAIL, UNREGISTERED
    full_report_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    
    document = relationship("Document", back_populates="verification_records")
    watermark_record = relationship("WatermarkRecord", back_populates="verification_records")

class RobustnessExperiment(Base):
    __tablename__ = "robustness_experiments"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    watermark_record_id = Column(String(36), ForeignKey("watermark_records.id"), nullable=False)
    transformation_type = Column(String(50), nullable=False)  # jpeg_compression, resize, gaussian_noise, crop, rotation
    transformation_params_json = Column(Text, nullable=False)
    
    detected = Column(Boolean, default=False, nullable=False)
    payload_recovered = Column(Boolean, default=False, nullable=False)
    bit_error_rate = Column(Float, default=0.0, nullable=False)
    extracted_payload = Column(String(255), nullable=True)
    psnr_db = Column(Float, nullable=True)
    execution_duration_ms = Column(Integer, default=0, nullable=False)
    
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)

class AuditEvent(Base):
    __tablename__ = "audit_events"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    actor_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    event_type = Column(String(100), nullable=False)  # USER_LOGIN, DOCUMENT_UPLOAD, WATERMARK_APPLY, VERIFY_ATTEMPT, etc.
    document_id = Column(String(36), nullable=True)
    ip_address = Column(String(50), nullable=True)
    status = Column(String(20), default="SUCCESS", nullable=False)
    details_json = Column(Text, nullable=True)
    previous_hash = Column(String(64), nullable=True)  # Tamper-evident chaining
    current_hash = Column(String(64), nullable=False)
    timestamp = Column(DateTime, default=utc_now, nullable=False)
    
    actor = relationship("User", back_populates="audit_events")

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Any
from datetime import datetime

# Auth schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: Optional[str] = None
    institution: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: Optional[str] = None
    institution: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Watermark application schemas
class ApplyWatermarkRequest(BaseModel):
    document_id: str
    watermark_type: str = Field(description="'visible' or 'invisible_dct'")
    text: str = Field(min_length=1, max_length=100)
    subtext: Optional[str] = None
    recipient_identifier: Optional[str] = None
    recipient_email: Optional[str] = None
    opacity: Optional[float] = 0.3
    font_size: Optional[float] = 36.0
    rotation: Optional[float] = 45.0

class WatermarkRecordResponse(BaseModel):
    id: str
    document_id: str
    watermark_type: str
    watermark_algorithm: str
    algorithm_version: str
    payload_text: str
    recipient_identifier: Optional[str]
    protected_file_size_bytes: int
    protected_sha256: str
    manifest_id: str
    signing_key_id: str
    created_at: datetime

    class Config:
        from_attributes = True

# Document schemas
class DocumentResponse(BaseModel):
    id: str
    title: str
    original_filename: str
    file_size_bytes: int
    page_count: int
    original_sha256: str
    owner_id: str
    created_at: datetime
    watermark_records_count: Optional[int] = 0
    watermark_records: Optional[List[WatermarkRecordResponse]] = []

    class Config:
        from_attributes = True

# Verification schemas
class VerificationRequest(BaseModel):
    manifest_json: Optional[str] = None

class VerificationResultResponse(BaseModel):
    id: str
    candidate_filename: str
    candidate_sha256: str
    exact_hash_match: bool
    signature_valid: bool
    signing_key_trusted: bool
    watermark_detected: bool
    watermark_payload_match: bool
    extracted_payload: Optional[str]
    status_summary: str
    full_report: dict
    created_at: datetime

# Robustness schemas
class RobustnessExperimentRequest(BaseModel):
    watermark_record_id: str
    transformation_type: str
    intensity: float

class RobustnessExperimentResponse(BaseModel):
    id: str
    transformation_type: str
    transformation_params_json: str
    detected: bool
    payload_recovered: bool
    bit_error_rate: float
    extracted_payload: Optional[str]
    psnr_db: Optional[float]
    execution_duration_ms: int
    created_at: datetime

    class Config:
        from_attributes = True

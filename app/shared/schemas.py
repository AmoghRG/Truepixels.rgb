"""Cross-module shared data structures and interface schemas.

Conforms strictly to Module Interface Contract v1.0 (Contracts C1, C2, C3).
"""
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Tuple
from pydantic import BaseModel, ConfigDict, Field


# --- Contract C1: M1 to M2 (Preprocessed Image) ---
class NormalizationParams(BaseModel):
    mean: Tuple[float, float, float] = (0.48145466, 0.4578275, 0.40821073)
    std: Tuple[float, float, float] = (0.26862954, 0.26130258, 0.27577711)
    scheme: Literal["clip_openai", "imagenet"] = "clip_openai"


class PreprocessedImage(BaseModel):
    """Hand-off from M1 pipeline (0.3.4) to M2 pipeline (0.4.1 / 0.4.2)."""
    image_id: int = Field(..., description="Foreign key to D2.images")
    user_id: int = Field(..., description="Owner user ID for authorization and D4 linkage")
    tensor_ref: str = Field(..., description="Filesystem path to .npy tensor on shared volume")
    shape: Tuple[int, int, int] = Field((3, 224, 224), description="(C, H, W)")
    dtype: Literal["float32"] = "float32"
    normalization: NormalizationParams = Field(default_factory=NormalizationParams)
    source_reference: str = Field(..., description="Path to decoded ORIGINAL image at native resolution")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(arbitrary_types_allowed=True)


# --- Contract C3: M1 to M2 and M3 (Session and Identity) ---
class SessionContext(BaseModel):
    """Validated session identity passed from FastAPI dependency."""
    user_id: int
    email: str
    role: Literal["User", "Admin"]
    account_status: Literal["active", "disabled", "removed"]
    session_token: str
    issued_at: datetime
    expires_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Contract C2: M2 to M3 (Inference Output Reference) ---
class ActivationBundle(BaseModel):
    backbone: Literal["clip_vit_b32", "clip_vit_l14"] = "clip_vit_b32"
    patch_grid: Tuple[int, int] = (7, 7)
    attention: Optional[Any] = None
    patch_embeddings: Optional[Any] = None
    head_gradients: Optional[Any] = None
    spectrum: Optional[Any] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


class InferenceOutput(BaseModel):
    prediction_id: int
    image_id: int
    user_id: int
    model_id: int
    predicted_class: Literal["Real", "AI Generated"]
    confidence_score: float
    semantic_score: float
    frequency_score: float
    fusion_score: float
    prediction_timestamp: datetime
    latency_ms: int
    activations: Optional[ActivationBundle] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

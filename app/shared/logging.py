"""Contract C5 logging stub with automatic secret redaction and non-throwing best-effort execution.

Conforms to Module Interface Contract v1.0 Section 8 and SRS F.15 / NF.7.
"""
import logging
import re
import sys
from typing import Literal, Optional

logger = logging.getLogger("truepixels.audit")
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [AUDIT-%(name)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Regex patterns for sensitive information that must NEVER appear in logs
REDACTION_PATTERNS = [
    (re.compile(r'(?i)(password|pass|secret|token|bearer|auth|authorization)\s*[:=]\s*["\']?([^"\'\s,]+)["\']?'), r'\1=[REDACTED]'),
    (re.compile(r'(?i)bearer\s+[a-zA-Z0-9\-_.]+', re.IGNORECASE), 'Bearer [REDACTED]'),
    (re.compile(r'ey[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}'), '[JWT_REDACTED]'),
]


def redact_secrets(text: str) -> str:
    """Sanitizes text to prevent accidental credential leakage in log records."""
    if not text:
        return ""
    redacted = str(text)
    for pattern, replacement in REDACTION_PATTERNS:
        redacted = pattern.sub(replacement, redacted)
    return redacted


def emit(
    event_type: Literal["authentication", "prediction-request", "administrative-action", "error"],
    event_detail: str,
    severity: Literal["info", "warning", "error"] = "info",
    user_id: Optional[int] = None,
    request_id: Optional[str] = None,
) -> None:
    """Contract C5 logging entrypoint.

    Synchronous, non-throwing, and best-effort.
    """
    try:
        sanitized_detail = redact_secrets(event_detail)
        log_payload = f"type={event_type} | severity={severity} | user_id={user_id} | req_id={request_id} | {sanitized_detail}"
        
        if severity == "error":
            logger.error(log_payload)
        elif severity == "warning":
            logger.warning(log_payload)
        else:
            logger.info(log_payload)
    except Exception as e:
        # Non-throwing guarantee (PRD 5.3.1 / Goal G4)
        sys.stderr.write(f"[LOGGING-EMIT-FAIL] Failed to emit audit log: {e}\n")

"""Exported FastAPI dependencies for authentication and role-based access control.

Imported by Module M2 and Module M3 across the system boundary (Contract C3).
"""
from app.m1_access.security import current_session, require_role

__all__ = ["current_session", "require_role"]

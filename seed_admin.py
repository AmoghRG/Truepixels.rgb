"""Script to seed an initial Admin account into the database."""
from app.m1_access.models import User
from app.m1_access.security import hash_password
from app.shared.db import SessionLocal, init_db

init_db()
db = SessionLocal()

admin_email = "admin@truepixels.rgb"
admin_pwd = "AdminSecurePassword123!"

existing = db.query(User).filter(User.email == admin_email).first()
if not existing:
    admin = User(
        full_name="System Administrator",
        email=admin_email,
        password_hash=hash_password(admin_pwd),
        role="Admin",
        account_status="active",
        is_email_verified=True,
    )
    db.add(admin)
    db.commit()
    print(f"Admin account created successfully!")
    print(f"Email:    {admin_email}")
    print(f"Password: {admin_pwd}")
else:
    print(f"Admin account already exists: {admin_email}")

db.close()

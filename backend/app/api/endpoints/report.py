from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.domain_models import User, Report
from app.schemas.report_schemas import ReportCreate, ReportResponse
from app.deps import get_current_user
from app.ai_engine.stylometry_killer import sanitize_report_text
import os
import uuid

router = APIRouter()

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/", response_model=ReportResponse)
async def create_report(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    title: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(None)
) -> Any:
    print(f"DEBUG: Menerima laporan baru: {title}")

    # 1. Simpan gambar jika ada
    image_url = None
    if image and image.filename:
        print(f"DEBUG: Menyimpan gambar {image.filename}")
        file_extension = os.path.splitext(image.filename)[1]
        file_name = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        try:
            with open(file_path, "wb") as buffer:
                content = await image.read()
                buffer.write(content)
            # URL yang bisa diakses via browser
            image_url = f"/uploads/{file_name}"
        except Exception as e:
            print(f"DEBUG: Gagal simpan gambar: {e}")

    # 2. Jalankan Anti-Stylometry AI
    print("DEBUG: Menjalankan AI Sanitization...")
    sanitized_content = await sanitize_report_text(description)

    # Tentukan status berdasarkan hasil AI
    status = "processed"
    if "Error" in sanitized_content or "Unauthorized" in sanitized_content:
        status = "pending (AI Error)"
        print("DEBUG: AI Gagal memproses, cek API Key Groq Anda!")

    # 3. Simpan ke database
    db_obj = Report(
        title=title,
        description=description,
        sanitized_content=sanitized_content,
        image_url=image_url,
        status=status,
        user_id=current_user.id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    print(f"DEBUG: Laporan berhasil disimpan dengan ID: {db_obj.id}")
    return db_obj

@router.get("/my-reports", response_model=List[ReportResponse])
def read_my_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    return db.query(Report).filter(Report.user_id == current_user.id).order_by(Report.created_at.desc()).all()

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
    # 1. Save image if exists
    image_url = None
    if image:
        file_extension = os.path.splitext(image.filename)[1]
        file_name = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        with open(file_path, "wb") as buffer:
            content = await image.read()
            buffer.write(content)
        # In a real app, this would be a public URL
        image_url = file_path

    # 2. Run anti-stylometry
    sanitized_content = await sanitize_report_text(description)

    # 3. Save to database
    db_obj = Report(
        title=title,
        description=description,
        sanitized_content=sanitized_content,
        image_url=image_url,
        user_id=current_user.id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/my-reports", response_model=List[ReportResponse])
def read_my_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    return current_user.reports

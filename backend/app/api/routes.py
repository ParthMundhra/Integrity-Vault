from fastapi import APIRouter, UploadFile, File, Depends
from app.services.hashing import hash_file
from app.db.database import get_db
from app.db.models import Evidence
from sqlalchemy.orm import Session
from fastapi import HTTPException

router = APIRouter()

@router.post("/evidence/upload")
async def upload_evidence(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()

    file_hash = hash_file(content)

    evidence = Evidence(
        file_name=file.filename,
        hash=file_hash
    )

    db.add(evidence)
    db.commit()
    db.refresh(evidence)

    return {
        "evidence_id": evidence.id,
        "hash": file_hash
    }

@router.get("/evidence/{evidence_id}")
def get_evidence(evidence_id: str, db: Session = Depends(get_db)):
    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()

    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")

    return {
        "evidence_id": evidence.id,
        "file_name": evidence.file_name,
        "hash": evidence.hash
    }

@router.post("/evidence/verify")
async def verify_evidence(
    evidence_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Get stored record
    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()

    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")

    # Read uploaded file
    content = await file.read()

    # Hash again
    new_hash = hash_file(content)

    # Compare
    if new_hash == evidence.hash:
        return {
            "status": "VERIFIED",
            "message": "File is intact",
            "hash": new_hash
        }
    else:
        return {
            "status": "TAMPERED",
            "message": "File has been modified",
            "original_hash": evidence.hash,
            "new_hash": new_hash
        }
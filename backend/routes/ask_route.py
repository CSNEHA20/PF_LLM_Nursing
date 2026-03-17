from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import os
import shutil
from services.gemini_client import upload_document
from services.file_search_service import search_documents
from services.store_service import get_active_store

router = APIRouter()


# ── Ask endpoint ─────────────────────────────────────────────────────────────

class AskRequest(BaseModel):
    question: str
    store_name: Optional[str] = None   # If omitted, active store is used automatically


@router.post("/ask")
async def ask_question(request: AskRequest):
    """
    Ask a question grounded in documents from the ACTIVE store.
    Optionally pass store_name to query a specific store instead.
    """
    print(f"DEBUG QUESTION: {request.question}")
    print(f"DEBUG ASK STORE (requested): {request.store_name or '(active)'}")

    response = search_documents(request.question, store_name=request.store_name)

    # Report which store was actually used
    used_store = request.store_name or get_active_store()
    return {"answer": response, "store": used_store}


# ── Upload endpoint ───────────────────────────────────────────────────────────

@router.post("/upload-document")
async def upload_document_endpoint(file: UploadFile = File(...)):
    """
    Upload a PDF or TXT document to the Gemini Files API.
    The file is automatically added to the currently ACTIVE store.
    No store_name parameter is required.
    """
    print(f"DEBUG UPLOAD FILE NAME: {file.filename}")

    # Create uploads temp folder if it does not exist
    os.makedirs("uploads", exist_ok=True)

    # Save the uploaded file temporarily
    file_path = os.path.join("uploads", file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Upload to Gemini — active store is resolved automatically inside upload_document
        file_id = upload_document(file_path)

        print(f"DEBUG FILE ID: {file_id}")

        # Clean up temp file after successful Gemini upload
        if os.path.exists(file_path):
            os.remove(file_path)

        active_store = get_active_store()

        return {
            "message": "Document uploaded successfully",
            "file_id": file_id,
            "store": active_store,
        }

    except Exception as e:
        # Clean up temp file on error too
        if os.path.exists(file_path):
            os.remove(file_path)

        print(f"DEBUG Gemini upload error: {e}")
        return JSONResponse(
            status_code=400,
            content={
                "error": "Gemini upload failed",
                "details": str(e),
            },
        )

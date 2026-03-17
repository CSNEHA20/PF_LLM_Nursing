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
async def upload_document_endpoint(
    file: UploadFile = File(...),
    store_name: Optional[str] = None
):
    """
    Upload a PDF or TXT document to the Gemini Files API.
    The file is added to the specified store, or the currently ACTIVE store if omitted.
    """
    print(f"DEBUG UPLOAD FILE NAME: {file.filename}")

    # Create uploads temp folder if it does not exist
    os.makedirs("uploads", exist_ok=True)

    # Save the uploaded file temporarily
    file_path = os.path.join("uploads", file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Upload to Gemini — store_name can be None to use active store
        file_id = upload_document(file_path, store_name=store_name)

        print(f"DEBUG FILE ID: {file_id}")
        print(f"DEBUG TARGET STORE: {store_name or '(active)'}")

        # Clean up temp file after successful Gemini upload
        if os.path.exists(file_path):
            os.remove(file_path)

        # Use the provided store_name or resolve what the actual active/default store is
        used_store = store_name or get_active_store()

        return {
            "message": "Document uploaded successfully",
            "file_id": file_id,
            "store": used_store,
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

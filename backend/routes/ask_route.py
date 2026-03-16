from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import shutil
from services.gemini_client import upload_document
# Import search_documents from services.file_search_service
from services.file_search_service import search_documents

# Create router = APIRouter()
router = APIRouter()

class AskRequest(BaseModel):
    question: str

# Create POST /ask endpoint
@router.post("/ask")
async def ask_question(request: AskRequest):
    # Call search_documents(question)
    response = search_documents(request.question)
    
    # Return the Gemini response
    return {"answer": response}

@router.post("/upload-document")
async def upload_document_endpoint(file: UploadFile = File(...)):
    # Create a folder named "uploads" if it does not exist
    os.makedirs("uploads", exist_ok=True)
    
    # Save the uploaded file temporarily inside the uploads folder
    file_path = os.path.join("uploads", file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Pass the saved file path to the Gemini upload function
        file_id = upload_document(file_path)
        
        # Clean up the temporary file only after Gemini upload completes successfully
        if os.path.exists(file_path):
            os.remove(file_path)

        # Return a success response with the file ID
        return {
            "message": "Document uploaded successfully",
            "file_id": file_id
        }
    except Exception as e:
        print(f"Gemini upload error: {e}")
        return JSONResponse(
            status_code=400,
            content={
                "error": "Gemini upload failed",
                "details": str(e)
            }
        )

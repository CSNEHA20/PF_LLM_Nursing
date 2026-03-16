from fastapi import APIRouter
from services.gemini_client import get_gemini_client

router = APIRouter()

@router.get("/documents")
def list_documents():

    client = get_gemini_client()

    try:
        files = client.files.list()

        return {
            "documents": [file.name for file in files]
        }

    except Exception as e:
        return {"error": str(e)}

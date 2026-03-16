from google import genai
from config.settings import settings

def get_gemini_client():
    """
    Initializes the Gemini client using the API key
    loaded from environment variables.
    """
    if not settings.GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY not found in environment variables. "
            "Check your .env file and settings configuration."
        )

    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return client

def upload_document(file_path: str) -> str:
    """
    Uploads a document to the Gemini Files API.
    Returns the uploaded file name.
    """
    client = get_gemini_client()

    try:
        uploaded_file = client.files.upload(file=file_path)
        print("DEBUG: File uploaded to Gemini:", uploaded_file.name)
        return uploaded_file.name

    except Exception as e:
        print("DEBUG ERROR: Gemini upload failed:", str(e))
        raise e

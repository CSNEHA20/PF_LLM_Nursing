from google import genai
from config.settings import settings
from services.store_service import add_file


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
    Uploads a document to the Gemini Files API and persists the file ID
    into the currently ACTIVE store automatically.
    No store_name parameter needed — the active store is resolved internally.

    Args:
        file_path: Local path to the file to upload.

    Returns:
        The uploaded Gemini file name (e.g. 'files/abc123').
    """
    client = get_gemini_client()

    print(f"DEBUG UPLOAD FILE PATH: {file_path}")

    try:
        uploaded_file = client.files.upload(file=file_path)
        file_id = uploaded_file.name

        # Capture the MIME type returned by Gemini (e.g. application/pdf, text/plain)
        mime_type = getattr(uploaded_file, "mime_type", "application/pdf") or "application/pdf"

        print(f"DEBUG: File uploaded to Gemini: {file_id}")
        print(f"DEBUG: MIME type: {mime_type}")

        # Persist file_id + mime_type into the active store (auto-resolved)
        add_file(file_id, mime_type)

        return file_id

    except Exception as e:
        print(f"DEBUG ERROR: Gemini upload failed: {str(e)}")
        raise e

from google.genai import types
from services.gemini_client import get_gemini_client
from services.store_service import get_active_files, get_files_from_store, get_active_store

# Gemini File API requires the full HTTPS URI, not just the short name.
# Short name format : "files/0070ww0ivunq"
# Full URI format   : "https://generativelanguage.googleapis.com/v1beta/files/0070ww0ivunq"
GEMINI_FILES_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"


def _to_full_uri(file_id: str) -> str:
    """
    Convert a short Gemini file name such as 'files/abc123'
    to the full HTTPS URI that the API requires.
    If the value already starts with 'https://' it is returned unchanged.
    """
    if file_id.startswith("https://"):
        return file_id
    # Strip any leading slash just in case
    return f"{GEMINI_FILES_BASE_URL}/{file_id.lstrip('/')}"


def search_documents(question: str, store_name: str = None) -> str:
    """
    Real RAG implementation:
    1. Load stored Gemini file IDs from the ACTIVE store (or a named store if specified).
    2. Convert each short file name to its full HTTPS URI.
    3. Attach those files to the Gemini generate_content call via file_uri parts.
    4. Return a grounded answer from the uploaded nursing documents.

    Args:
        question:   The user's question.
        store_name: Optional. If omitted, the active store is used automatically.
    """
    client = get_gemini_client()

    # Use named store if provided, otherwise fall back to the active store
    if store_name:
        file_entries = get_files_from_store(store_name)
        used_store = store_name
    else:
        file_entries = get_active_files()
        used_store = get_active_store()

    print(f"DEBUG ASK STORE: {used_store}")
    print(f"DEBUG FILES USED: {file_entries}")

    if not file_entries:
        return (
            f"No documents uploaded yet in store '{used_store}'. "
            "Please upload a nursing document first."
        )

    # Build the contents list using the SDK types so file_uri is correct
    parts = []

    for entry in file_entries:
        file_id  = entry["file_id"]
        mime_typ = entry.get("mime_type", "application/pdf")
        full_uri = _to_full_uri(file_id)
        print(f"DEBUG URI: {full_uri} | MIME: {mime_typ}")
        parts.append(types.Part.from_uri(file_uri=full_uri, mime_type=mime_typ))

    # Add the user question as the final text part
    parts.append(types.Part.from_text(text=question))

    contents = [types.Content(role="user", parts=parts)]

    system_instruction = (
        "You are a Nursing AI Assistant. "
        "Answer ONLY from the uploaded nursing documents provided. "
        "If the answer is not found in the documents, respond with: "
        "'Answer not available in uploaded documents.' "
        "Do NOT hallucinate or use external knowledge."
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
            ),
        )

        print("DEBUG: Gemini RAG response received")
        return response.text

    except Exception as e:
        print("ERROR:", str(e))

        if "exceeds the supported page limit" in str(e):
            return (
                "Document too large. Please upload smaller PDFs (less than 1000 pages)."
            )

        return f"Unable to answer from documents. Error: {str(e)}"

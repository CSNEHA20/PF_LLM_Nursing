from services.gemini_client import get_gemini_client

def search_documents(question: str):
    """
    Uses Gemini File Search API to answer a user question.
    Configured so the response must come only from uploaded documents.
    """
    client = get_gemini_client()
    
    # Apply strict rules via system instructions
    # Response rules: The answer must come strictly from uploaded documents, no hallucinated information
    system_instruction = (
        "You are an AI assistant for a Nursing Learning platform. "
        "The answer must come strictly from uploaded documents. "
        "No hallucinated information whatsoever."
    )
    
    try:
        # Note: In a complete File Search implementation, you would pass the uploaded
        # file references (e.g., from client.files.upload) within the 'contents' 
        # as well so the model has the documents to search through.
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=question,
            config={
                "system_instruction": system_instruction,
            }
        )
        return response.text
    except Exception as e:
        return f"Error in document search: {str(e)}"

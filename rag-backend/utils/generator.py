import google.generativeai as genai
import os


# ✅ Configure your Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Replace with your actual key

# ✅ Initialize the model
_model = genai.GenerativeModel("gemini-2.5-pro")

# ✅ Define the ask function
def ask_gemini(query: str, context_chunks: list[str]) -> str:
    # Combine all context chunks into one string
    context = "\n\n".join(context_chunks)

    # Build the prompt with context and question
    prompt = f"""

    Use the context to answer with high accuracy and cite quotes from context when relevant. If you don't know the answer, just say "I don't know". Do not make up an answer.
    --- Context Start ---
    {context}
    --- Context End ---

    Question: {query}
    Answer:
    """

    # Generate the response
    resp = _model.generate_content(prompt)
    return (resp.text or "").strip()
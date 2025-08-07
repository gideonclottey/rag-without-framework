import google.generativeai as genai

# ✅ Configure your Gemini API key
genai.configure(api_key="AIzaSyD3R1iQ4HpBvWWZceHkRqyv0f63pwZHVvg")  # Replace with your actual key

# ✅ Initialize the model
model = genai.GenerativeModel("gemini-2.5-pro")

# ✅ Define the ask function
def ask_gemini(query: str, context_chunks: list[str]) -> str:
    # Combine all context chunks into one string
    context = "\n\n".join(context_chunks)

    # Build the prompt with context and question
    prompt = f"""
You are a helpful assistant. Use the context to answer the question with 95% high confidence.

--- Context Start ---
{context}
--- Context End ---

Question: {query}
Answer:
"""

    try:
        # Call Gemini to generate content
        response = model.generate_content(prompt)

        # Print and return the response
        print("✅ Gemini Response:\n", response.text)
        return response.text.strip()

    except Exception as e:
        print("❌ Error calling Gemini:", e)
        return "An error occurred."

# # ✅ Example usage
# if __name__ == "__main__":
#     context = [
#         "Retrieval-Augmented Generation (RAG) is a technique that enhances large language models by providing them with external documents retrieved from a knowledge base at query time."
#     ]
#     query = "What is the purpose of RAG in LLMs?"
#     answer = ask_gemini(query, context)
#     print("\nFinal Answer:", answer)

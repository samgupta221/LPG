from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

model_name = os.getenv("GROQ_MODEL_NAME")
if not model_name:
    model_name = "llama-3.1-8b-instant"

if not api_key:
    raise ValueError("GROQ_API_KEY not found. Please set it in your .env file.")

llm = ChatGroq(
    api_key=api_key,
    model=model_name
)

if __name__ == "__main__":
    response = llm.invoke("Two most important ingredients in samosa are")
    print(response.content)
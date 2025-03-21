import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Try using the correct model name
model = genai.GenerativeModel("gemini-1.5-pro")  # Use this instead of "gemini-pro"

response = model.generate_content("Hello, how are you?")
print(response.text)

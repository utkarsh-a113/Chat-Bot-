# AIzaSyBbb2PHiTUEagg2fKGBcX-oJlIecE8xD4Q
import google.generativeai as genai

# Configure your API key
genai.configure(api_key="AIzaSyBbb2PHiTUEagg2fKGBcX-oJlIecE8xD4Q")

# Use the correct available model name
model = genai.GenerativeModel("models/gemini-2.5-flash")

# Generate a response
response = model.generate_content("Hello! This is a test for the auto-reply system.")
print(response.text)


import google.generativeai as genai

genai.configure(api_key="AIzaSyD3R1iQ4HpBvWWZceHkRqyv0f63pwZHVvg")

model = genai.GenerativeModel("gemini-2.5-pro")

response = model.generate_content("Say hello in 5 languages")
print(response.text)

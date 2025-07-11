import google.generativeai as genai

genai.configure(api_key="AIzaSyDTTMTlPrQY-MfIo6d5wdtDKS7-BpcRw-Y")

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Say hello world")
print(response.text)
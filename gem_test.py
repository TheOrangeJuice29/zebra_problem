"""import google.generativeai as genai

# Set your API key from https://makersuite.google.com/app/apikey
genai.configure(api_key="AIzaSyAPLu-rmYdwB253UUcXTa_2FilPFqLnNbY")

# Load Gemini 1.5 Pro (or 1.0 Pro if you prefer)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Or, if you want to try Gemini 1.0 Pro:
# model = genai.GenerativeModel("gemini-pro")

response = model.generate_content("Say hello.")
print(response.text)"""


from gemini_api import model

"""response = model.generate_content("The Spaniard owns a dog. What else can you deduce?")
print(response.text)"""

response = model.generate_content("Say hello.")
print(response.text)
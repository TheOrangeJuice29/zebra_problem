import google.generativeai as gen

gen.configure(api_key = "")
model = gen.GenerativeModel("gemini-1.5-flash")
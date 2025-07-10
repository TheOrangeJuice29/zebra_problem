import google.generativeai as gen

gen.configure(api_key = "AIzaSyAPLu-rmYdwB253UUcXTa_2FilPFqLnNbY")
model = gen.GenerativeModel("gemini-1.5-flash")
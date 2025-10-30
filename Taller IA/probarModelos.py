import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv(r"E:\licenciatura Magaly\IA y Sistemas Expertos\Taller IA\.env")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

models = genai.list_models(page_size=20)
for m in models:
    print(m.name, m.supported_generation_methods)
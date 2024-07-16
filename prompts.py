import google.generativeai as genai
import os

def configure_genai():
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    return genai.GenerativeModel('gemini-pro'), genai.GenerativeModel('gemini-pro-vision')

model, vision_model = configure_genai()

def get_gemini_response(prompt, image=None):
    if image:
        response = vision_model.generate_content([prompt, image])
    else:
        response = model.generate_content(prompt)
    return response.text
import os
from PIL import Image
import google.generativeai as genai
from db import save_analysis, save_names

# Configure Gemini API key
genai.configure(api_key="Add your keys")

def get_image_description(image_path):
    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
        with open(image_path, "rb") as img_file:
            image_data = img_file.read()

        content = [
            {
                "role": "user",
                "parts": [
                    {"text": "Describe this image in detail."},
                    {"inline_data": {"mime_type": "image/jpeg", "data": image_data}},
                ],
            }
        ]

        response = model.generate_content(contents=content)
        description = response.text
        save_analysis(os.path.basename(image_path), description)
        return description

    except Exception as e:
        return f"[Error] Could not process image: {e}"

def extract_names_from_image(image_path):
    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
        with open(image_path, "rb") as img_file:
            image_data = img_file.read()

        content = [
            {
                "role": "user",
                "parts": [
                    {"text": "Extract all the human names visible in this image. Return just a list, one name per line."},
                    {"inline_data": {"mime_type": "image/jpeg", "data": image_data}},
                ],
            }
        ]

        response = model.generate_content(contents=content)
        raw_names = response.text.strip().splitlines()

        # ✅ Clean the names
        cleaned_names = [name.strip() for name in raw_names if name.strip()]
        filename = os.path.basename(image_path)

        # ✅ Save once
        save_names(cleaned_names, filename)

        return cleaned_names

    except Exception as e:
        return [f"[Error] Failed to extract names: {e}"]

import os
import google.generativeai as genai
from db import save_analysis

# Configure Gemini
genai.configure(api_key="AIzaSyCR9ocWQa0aknbGJsUTSgJ8qbwCJ4UTcpY")  # ← Replace with your actual API key

def get_image_description(image_path):
    try:
        if not os.path.exists(image_path):
            return "[Error] Image file not found."

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

        # Save to DB and JSON
        save_analysis(os.path.basename(image_path), description)

        return description

    except Exception as e:
        return f"[Error] Could not process image: {e}"

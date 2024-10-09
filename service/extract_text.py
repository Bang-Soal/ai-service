from PIL import Image
import requests
import pytesseract

class ExtractTextFromImage:
    def extract_text(image_url):
        img = Image.open(requests.get(image_url, stream=True).raw)
        text = pytesseract.image_to_string(img)
        return text
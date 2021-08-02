from PIL import Image
import pytesseract

def execute(image, lang):
    img = Image.open(image)
    txt = pytesseract.image_to_string(img, lang = lang)
    return txt
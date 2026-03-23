import easyocr
from PIL import Image

class OCRHandler:
    def __init__(self, languages=['ar', 'en']):

        self.reader = easyocr.Reader(languages)

    def extract_text(self, image):


        import numpy as np
        image_array = np.array(image)

        results = self.reader.readtext(image_array)

        extracted = []
        for bbox, text, prob in results:
            extracted.append({'text': text })
        return extracted
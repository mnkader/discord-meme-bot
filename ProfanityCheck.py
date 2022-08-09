from better_profanity import profanity
from pytesseract import pytesseract
from PIL import Image
import io
import requests

class ProfanityCheck:
    def __init__(self, profane_words_file, path_to_tesseract):
        self.profanity = profanity
        pytesseract.tesseract_cmd = path_to_tesseract   
        self.add_profane_list()
        
    def add_profane_list(self):
        with open('profanity_list.txt', 'r') as file:
            profanity.add_censor_words(file.read().split(','))
 
    def get_image_from_url(self, url):
        response = requests.get(url, stream=True)
        return Image.open(io.BytesIO(response.content))

    def check_image(self, url):
        img = self.get_image_from_url(url)
        imagetext = pytesseract.image_to_string(img)
        return self.contains_profanity(imagetext)

    def add_bad_word(self, word):
        with open('profanity_list.txt', 'a') as file:
            file.write(',' + word)
        profanity.add_censor_words([word])

    def contains_profanity(self, data):
        return profanity.contains_profanity(data)
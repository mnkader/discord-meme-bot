from ProfanityCheck import ProfanityCheck

#after testing, delete words added from profanity_list.txt
class Test:
    def __init__(self):
        self.profanity_checker = ProfanityCheck('TODO', 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe')
        
    def check_images(self):
        assert self.profanity_checker.check_image('https://static1.bigstockphoto.com/6/6/1/large1500/166959749.jpg') == True
        assert self.profanity_checker.check_image('https://i.etsystatic.com/15192127/r/il/0e2fab/1949102233/il_794xN.1949102233_pa8h.jpg') == True
        assert self.profanity_checker.check_image('https://rlv.zcache.com/accounting_swear_words_annoying_funny_accountant_poster-r6744fd7ea1e942f89ecaee2354bd82fd_i4w_8byvr_630.jpg') == False
        assert self.profanity_checker.check_image('https://i1.wp.com/childhoodexplained.com/wp-content/uploads/2020/07/Kids-and-Swear-Words-1.jpg') == False

    def check_string(self):
        my_harmelss_string = 'This is my harmless string, keyword fudge'
        my_harmful_string = 'This mf is harmful'
        self.is_profane(my_harmelss_string)#false
        self.is_profane(my_harmful_string)#true
        self.profanity_checker.add_bad_word('fudge')
        print('added \'fudge\' as a bad word')
        self.is_profane(my_harmelss_string)#true
    
    def is_profane(self, string):
        print(str(self.profanity_checker.contains_profanity(string)) + '::', string)
        
test = Test()
test.check_string()
test.check_images()
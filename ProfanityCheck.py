from better_profanity import profanity

class ProfanityCheck:
    def add_bad_word(self, word):
        profanity.add_censor_words([word])

    def contains_profanity(self, data):
        return profanity.contains_profanity(data)
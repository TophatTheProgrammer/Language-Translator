from deep_translator import GoogleTranslator
from lingua import LanguageDetectorBuilder

class Translator:
    """A translator class to translate text"""

    def __init__(self, to_lang, presentable_lang):
        """Initialize the translator"""
        self.to_lang = to_lang
        self.presentable_lang = presentable_lang
        self.translator = GoogleTranslator(source="auto", target=self.to_lang)
        self.language_detector = LanguageDetectorBuilder.from_all_languages().build()


    def Translation(self, text):
        """translate the given text to the translator to_lang language"""
        
        #detect the language used
        lang = self.language_detector.detect_language_of(text)
        if text == "":
            return ["", "unknown"]
        else:

            #translate the text and then return the text and the language used
            translated_text = self.translator.translate(text)
            return [translated_text, lang.name.lower()]
        
        
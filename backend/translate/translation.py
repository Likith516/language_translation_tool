import pickle
import os

from transformers import MarianTokenizer, MarianMTModel


class TranslationBNR32:
    """
       A class used to help in maintaining translation pairs
       and use the models accordingly

       ...

       Attributes
       ----------
       lang1 : str
           a formatted string to represent the source language
       lang2 : str
           a formatted string to represent the target language

       Methods
       -------
       translate(text=None)
           Translates the given text using the models and returns
           the translated text

       """

    def __init__(self, lang1, lang2):
        """
        Parameters
        ----------
        lang1 : str
            formated string of the source language
            ['en', 'de', 'fr', 'hi']
        lang2 : str
            formatted string of the target language
            ['en', 'de', 'fr', 'hi'] and != lang1

        """
        self.lang1 = lang1
        self.lang2 = lang2
        self.runTests()

    def saveModel(self, lang1, lang2):
        """
        Obtains the cache files and saves the models

        Parameters
        ----------
        lang1 : str
            formated string of the source language
            ['en', 'de', 'fr', 'hi']
        lang2 : str
            formatted string of the target language
            ['en', 'de', 'fr', 'hi'] and != lang1
        """
        model_name = f'Helsinki-NLP/opus-mt-{lang1}-{lang2}'
        name = f"{lang1}-{lang2}"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        f = open("TranslationBNR32/models/" +name + ".pkl", "wb")
        pickle.dump([tokenizer, model], f)
        f.close()

    def runTests(self):
        """
        A method to verify the integrity of the models and cache built

        """
        if not os.path.exists('TranslationBNR32/models'):
            os.mkdir(os.path.join('TranslationBNR32', 'models'))
            print("Models not found, creating models")
            for i in [("en", "hi"), ("en", "de"), ("en", "fr")]:
                self.saveModel(i[0], i[1])
                self.saveModel(i[1], i[0])
            print("Finished making models")

    def translate(self, text):
        """
        Translates the given text using the appropraite model

        Parameters
        ----------
        text : str
            The text to be translated

        Returns
        -------
        translated_text: str
            The translated text passed to be converted to speech output

        """
        file_name = f"TranslationBNR32/models/{self.lang1}-{self.lang2}.pkl"
        f = open(file_name, "rb")
        tokenizer, model = pickle.load(f)
        tokenized_text = tokenizer.__call__([text], return_tensors='pt')
        translation = model.generate(**tokenized_text)
        translated_text = tokenizer.decode(translation[0], skip_special_tokens=True)
        return translated_text
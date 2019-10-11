import re
import string
from abc import ABC
from html.parser import HTMLParser
from spacy.lang import punctuation
from spacy.lang.en import stop_words
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES

cachedStopWords = list(stop_words.STOP_WORDS)
cachedStopWords += list(punctuation.TOKENIZER_SUFFIXES)
cachedStopWords += list(punctuation.TOKENIZER_PREFIXES)
cachedStopWords += list(string.digits)
cachedStopWords += ['““', "’’", '–', "’", '”']

lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)

punctuation = string.punctuation + '”' + '“' + '–'


class MLStripper(HTMLParser, ABC):
    """
    Strip HTML from strings in Python
    https://stackoverflow.com/a/925630/5983691
    """
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def remove_html(text):
    """
    Remove html strings in text (see above class)
    :param text: string
    :return: string
    """
    s = MLStripper()
    s.feed(text)

    return s.get_data()


def stopwords_lemmatizing(text):
    """
    Remove stop words and lemmatize the text
    :param text: string
    :return: string
    """
    result = [''.join(lemmatizer(word, u"NOUN")) for word in text.split() if word not in cachedStopWords]

    return ' '.join(result)


def remove_digits(text):
    """
    Remove all digits
    :param text: string
    :return: string
    """
    result = ''.join(i for i in text if not i.isdigit()).lower()

    return ' '.join(result.split())


def remove_newlines(text):
    """
    Remove newline characters
    :param text: string
    :return: string
    """
    return text.replace('\\n', ' ').replace('\\r', ' ').replace('\n', ' ').replace('\r', ' ').replace('\\', ' ')


def remove_punctuation(text):
    """
    remove all punctuations from text
    :param text: string
    :return: string
    """
    return text.translate(str.maketrans('', '', punctuation))


def remove_latex(text):
    """
    Remove latex formatted content from text
    :param text: string
    :return: string
    """
    regex = r"(\$+)(?:(?!\1)[\s\S])*\1"
    subst = " "
    result = re.sub(regex, subst, text, 0, re.MULTILINE)

    return result

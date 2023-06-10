from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.utils import get_stop_words
import json

def bulletpoints(text):
    LANGUAGE = "german"
    SENTENCES_COUNT = 5

    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    summarizer = LexRankSummarizer()
    summarizer.stop_words = get_stop_words(LANGUAGE)
    summary = summarizer(parser.document, SENTENCES_COUNT)

    bullet_points = [str(bullet) for bullet in summary]
    result = {'Bulletpoints': bullet_points}
    
    return result

def bulletpoints_number(text, number):
    LANGUAGE = "german"
    SENTENCES_COUNT = number

    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    summarizer = LexRankSummarizer()
    summarizer.stop_words = get_stop_words(LANGUAGE)
    summary = summarizer(parser.document, SENTENCES_COUNT)

    bullet_points = [str(bullet) for bullet in summary]
    result = {'Bulletpoints': bullet_points}
    
    return result


def bulletpoints_number_tokenizer(text, number, tokenizer ):
    LANGUAGE = tokenizer
    SENTENCES_COUNT = number

    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    summarizer = LexRankSummarizer()
    summarizer.stop_words = get_stop_words(LANGUAGE)
    summary = summarizer(parser.document, SENTENCES_COUNT)

    bullet_points = [str(bullet) for bullet in summary]
    result = {'Bulletpoints': bullet_points}
    
    return result
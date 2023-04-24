from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.utils import get_stop_words

LANGUAGE = "german"
SENTENCES_COUNT = 5
text = "geschichte atmega328p"
if __name__ == "__main__":
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    summarizer = LexRankSummarizer()
    summarizer.stop_words = get_stop_words(LANGUAGE)
    summary = summarizer(parser.document, SENTENCES_COUNT)

    bullet_points = "\n- ".join(map(str, summary))
    print("- " + bullet_points)
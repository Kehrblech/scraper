from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
import json

# Returns summary of "german" text with fixed 3 Sentences
def luhn_summarizer(text):
    parser = PlaintextParser.from_string(text, Tokenizer("german"))

    # summarizer
    summarizer = LuhnSummarizer()
    summary = summarizer(parser.document, sentences_count=1)

    output = {
            'Topics': [str(sentence) for sentence in summary]
        }
    # output_json = json.dumps(output, ensure_ascii=False)
    return output
# Returns summary of "german" text with dynamic Sentences_Value 
def luhn_summarizer_number(text, sentences_number):
    parser = PlaintextParser.from_string(text, Tokenizer("german"))

    # summarizer
    summarizer = LuhnSummarizer()
    summary = summarizer(parser.document, sentences_count=sentences_number)

    output = {
            'Topics': [str(sentence) for sentence in summary]
        }
    # output_json = json.dumps(output, ensure_ascii=False)
    return output

# Returns summary of dynamic language text with fixed 3 Sentences
def luhn_summarizer_number_tokenizer(text, tokenizer):
    parser = PlaintextParser.from_string(text, Tokenizer(tokenizer))

    # summarizer
    summarizer = LuhnSummarizer()
    summary = summarizer(parser.document, sentences_count=3)

    output = {
            'Topics': [str(sentence) for sentence in summary]
        }
    # output_json = json.dumps(output, ensure_ascii=False)
    return output
# Returns summary of dynamic language text with dynamic Sentences_Value 
def luhn_summarizer_number_tokenizer(text, sentences_number, tokenizer):
    parser = PlaintextParser.from_string(text, Tokenizer(tokenizer))

    # summarizer
    summarizer = LuhnSummarizer()
    summary = summarizer(parser.document, sentences_count=sentences_number)

    output = {
            'Topics': [str(sentence) for sentence in summary]
        }
    # output_json = json.dumps(output, ensure_ascii=False)
    return output

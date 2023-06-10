from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import json

def lsa_summarzier(text):
    #  Create Parsers and Tokenizers also LSASummarizer  
    parser = PlaintextParser.from_string(text, Tokenizer("german"))
    summarizer = LsaSummarizer()

    # Get topics and also count parameter 
    topics = summarizer(parser.document, 5) 
        
    output = {
        'Topics': [str(topic).strip() for topic in topics]
    }
    #output_json = json.dumps(output, ensure_ascii=False)
    return output

def lsa_summarzier_number(text, number):
    #  Create Parsers and Tokenizers also LSASummarizer  
    parser = PlaintextParser.from_string(text, Tokenizer("german"))
    summarizer = LsaSummarizer()

    # Get topics and also count parameter 
    topics = summarizer(parser.document, 5) 
        
    output = {
        'Topics': [str(topic) for topic in topics]
    }
    #output_json = json.dumps(output, ensure_ascii=False)
    return output

def lsa_summarzier_number_tokenizer(text, number, tokenizer):
    #  Create Parsers and Tokenizers also LSASummarizer  
    parser = PlaintextParser.from_string(text, Tokenizer(tokenizer))
    summarizer = LsaSummarizer()

    # Get topics and also count parameter 
    topics = summarizer(parser.document, 5) 
        
    output = {
        'Topics': [str(topic) for topic in topics]
    }
    #output_json = json.dumps(output, ensure_ascii=False)
    return output
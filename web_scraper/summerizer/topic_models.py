from gensim import corpora, models
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import re
import json


    
def topics(text,number_of_topics):
    
    clean_text = re.sub(r"[^\w\s]", "", text)  # Entfernt alle Sonderzeichen außer Wortzeichen und Leerzeichen

    # Tokenisierung und Entfernung von Stoppwörtern
    stop_words = stopwords.words('german')
    tokens = [token for token in word_tokenize(clean_text, language='german') if token.lower() not in stop_words]

    # Erstellen des Textkorpus
    text_corpus = [tokens]

    # Erstellen des Wörterbuchs
    dictionary = corpora.Dictionary(text_corpus)

    # Erstellen des Bag-of-Words-Vektors
    bow_vector = dictionary.doc2bow(tokens)

    # Anpassung des Corpus-Formats
    corpus = [bow_vector]

    # Erstellen des LDA-Modells
    lda_model = models.LdaModel(corpus=corpus, num_topics=number_of_topics, id2word=dictionary, passes=25)

    # Ausgabe der Themen
    topics = lda_model.print_topics(num_words=5)


    # Erstellen der JSON-Struktur
    output = {
        'topics': []
    }

    for topic in topics:
        topic_words = topic[1].split(' + ')
        topic_words_dict = {}
        for word in topic_words:
            word_prob = word.split('*')
            topic_words_dict[word_prob[1].replace('"', '').strip()] = float(word_prob[0])
        output['topics'].append(topic_words_dict)

    # Speichern der JSON-Struktur in eine Datei
    output_json = json.dumps(output)
    return output_json
        
    
import spacy
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import defaultdict
import heapq

class TextSummarizer:
    def __init__(self):
        nltk.download('punkt')
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words('english'))

    def preprocess_text(self, text):
        # Tokenize sentences
        sentences = sent_tokenize(text)
        # Tokenize words and remove stopwords
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalnum() and word not in self.stop_words]
        return sentences, words

    def calculate_sentence_scores(self, sentences, words):
        word_freq = defaultdict(int)
        for word in words:
            word_freq[word] += 1
            
        max_freq = max(word_freq.values())
        
        for word in word_freq.keys():
            word_freq[word] = (word_freq[word]/max_freq)
            
        sentence_scores = defaultdict(int)
        for sentence in sentences:
            for word, freq in word_freq.items():
                if word in sentence.lower():
                    sentence_scores[sentence] += freq
                    
        return sentence_scores

    def get_summary(self, text, num_sentences=3):
        sentences, words = self.preprocess_text(text)
        sentence_scores = self.calculate_sentence_scores(sentences, words)
        summary_sentences = heapq.nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
        return ' '.join(summary_sentences)
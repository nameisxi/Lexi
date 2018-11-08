import numpy as np
import pandas as pd
import os


class SentimentLexiconCreator:
    def __init__(self):
        self.nothing = None

        
    def classify_text(self, text, positive_rating_limit, negative_rating_limit):
        positive_reviews = []
        neutral_reviews = []
        negative_reviews = []
        for i in range(len(text)):
            if text.iloc[i, 1] > positive_rating_limit:
                positive_reviews.append(text.iloc[i, 0])
            elif text.iloc[i, 1] < negative_rating_limit:
                negative_reviews.append(text.iloc[i, 0])
            else:
                neutral_reviews.append(text.iloc[i, 0])
        return positive_reviews, neutral_reviews, negative_reviews

    def get_words(self, texts, minimum_word_frequency):
        word_counts = dict()
        for text in texts:
            text = text.replace('!', '.')
            text = text.replace('?', '.')
            text = text.replace('\n', '.')
            text = text.replace('-', '.')
            text = text.replace(',', '.')
            sentences = text.split('.')
            for sentence in sentences:
                words = sentence.split(' ')
                for word in words:
                    if len(word) < 2:
                        continue
                    word = word.lower()
                    if word not in word_counts.keys():
                        word_counts[word] = 0
                    word_counts[word] += 1
        qualifying_words = [word for word in word_counts.keys() if word_counts[word] >= minimum_word_frequency]
        qualifying_word_counts = {word: word_counts[word] for word in qualifying_words}
        return qualifying_words, qualifying_word_counts

    def pmi(self, word, text, unique_words_count, qualifying_word_counts, sentiment_word_count, qualifying_sentiment_word_counts): 
        '''Pointwise mutual information'''
        if word not in qualifying_sentiment_word_counts.keys():
            return None
        return np.log((qualifying_sentiment_word_counts[word] * unique_words_count)/(qualifying_word_counts[word] * sentiment_word_count))

    def semantic_orientation_score(self, positive_text, negative_text, qualifying_words, qualifying_word_counts, qualifying_positive_words, qualifying_positive_word_counts, qualifying_negative_words, qualifying_negative_word_counts):
        '''Semantic orientation score'''
        scores = []
        unique_words_count = len(qualifying_words)
        positive_word_count = len(qualifying_positive_words)
        negative_word_count = len(qualifying_negative_words)
        for word in qualifying_words:
            positive_pmi = self.pmi(word, positive_text, unique_words_count, qualifying_word_counts, positive_word_count, qualifying_positive_word_counts)
            negative_pmi = self.pmi(word, negative_text, unique_words_count, qualifying_word_counts, negative_word_count, qualifying_negative_word_counts)
            if positive_pmi == None or negative_pmi == None:
                scores.append(None)
                continue
            score = positive_pmi - negative_pmi
            scores.append(score)
        return scores

    def get_sentiment_lexicons(self, data, minimum_word_frequency, positive_rating_limit, negative_rating_limit):
        print('        Separeting words...')
        qualifying_words, qualifying_word_counts = self.get_words(data.iloc[:, 0], minimum_word_frequency)
        print('        Done')

        print('        Classifying reviews...')
        positive_text, neutral_text, negative_text = self.classify_text(data, positive_rating_limit, negative_rating_limit)
        print('        Done')
        
        print('        Separeting positive and negative words...')
        qualifyin_positive_words, qualifying_positive_word_counts = self.get_words(positive_text, 1)
        qualifying_negative_words, qualifying_negative_word_counts = self.get_words(negative_text, 1)
        print('        Done')

        print('        Calculating semantic orientation scores...')
        scores = self.semantic_orientation_score(positive_text, negative_text, qualifying_words, qualifying_word_counts, qualifyin_positive_words, qualifying_positive_word_counts, qualifying_negative_words, qualifying_negative_word_counts)
        print('        Done')
        
        valid_words = [qualifying_words[i] for i in range(len(qualifying_words)) if scores[i] != None]
        valid_scores = [score for score in scores if score != None]
        return valid_words, valid_scores
        
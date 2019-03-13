import os

import numpy as np
import pandas as pd
from docutils.parsers.rst.directives import percentage


class SentimentLexiconCreator:
    def print_status(self, i, length, string, percentage=True):
        ''' This is art. '''
        if percentage:
            output_string = f'        {string}: {int(((i + 1) / length) * 100)}%'
        else:
            output_string = f'        {string}'
        print(output_string, end="\r")


    def classify_text(self, text, positive_rating_limit, negative_rating_limit):
        length = len(text)
        positive_reviews, neutral_reviews, negative_reviews = [], [], []
        for i in range(length):
            self.print_status(i, length, 'Classifying reviews')
            if text.iloc[i, 1] > positive_rating_limit:
                positive_reviews.append(text.iloc[i, 0])
            elif text.iloc[i, 1] < negative_rating_limit:
                negative_reviews.append(text.iloc[i, 0])
            else:
                neutral_reviews.append(text.iloc[i, 0])
        return positive_reviews, neutral_reviews, negative_reviews


    def clean_review(self, review, negation=False, split=False):
        review = review.replace('\n', ' ')
        review = review.replace('-', ' ')
        review = review.replace('+', ' ')
        review = review.replace('(', ' ')
        review = review.replace(')', ' ')
        if negation:
            review = review.replace('!', ' ! ')
            review = review.replace('?', ' ? ')
            review = review.replace('.', ' . ')
            review = review.replace(',', ' , ')
            review = review.replace(':', ' : ')
            review = review.replace(';', ' ; ')
        else:
            review = review.replace('!', ' ')
            review = review.replace('?', ' ')
            review = review.replace('.', ' ')
            review = review.replace(',', ' ')
            review = review.replace(':', ' ')
            review = review.replace(';', ' ')
        review = review.strip().lower()
        if split:
            review = review.split()
        return review


    def clean_reviews(self, reviews, negation=False, split=False):
        cleaned_reviews = []
        for i in range(len(reviews)):         
            cleaned_reviews.append(self.clean_review(reviews[i], negation=negation, split=split))
        return cleaned_reviews


    def count_unique(self, words):
        unique = set(words[0])
        if len(words) > 1:
            for i in range(1, len(words)):
                unique.update(words[i])
        return len(unique)


    def count(self, word, reviews):
        count = 0
        for review in reviews:
            count += review.count(word)
        return count


    def get_so(self, word, pos_reviews, neg_reviews):
        w_in_neg = self.count(word, neg_reviews) + 1
        w_in_pos = self.count(word, pos_reviews) + 1

        denominator = w_in_neg * self.count_unique(pos_reviews)
        nominator =  w_in_pos * self.count_unique(neg_reviews)
        fraction = nominator / denominator
        score = np.log2(fraction)
        return score


    def get_negated_so(self, i, words, pos_reviews, neg_reviews):
        punctuations = [",", ".", ":", ";", "!", "?"]
        score = 0
        for j in range(i, len(words)):
            if words[j] in punctuations:
                break
            score += self.get_so(words[j], pos_reviews, neg_reviews)
        return score


    def get_unique_words(self, reviews, minimum_word_frequency):
        length = len(reviews)
        words = []
        unique_words = set()
        for i, review in enumerate(reviews):
            self.print_status(i, length, 'Searching unique words')
            for word in review:
                unique_words.add(word)
        print()
        print('        -Done')
        length = len(unique_words)
        selected_words = []
        for i, word in enumerate(unique_words):
            self.print_status(i, length, 'Counting occurances')
            if self.count(word, reviews) >= minimum_word_frequency:
                selected_words.append(word)
        return selected_words


    def get_negated_scores(self, reviews, minimum_word_frequency, pos_reviews, neg_reviews):
        negations = ["ei", "mutta"]
        unique_words, scores = [], []
        length = len(reviews)

        self.print_status(None, None, 'Preparing data: 0%', percentage=False)
        words = self.clean_reviews(reviews, negation=False, split=True)
        self.print_status(None, None, 'Preparing data: 20%', percentage=False)
        qualified_words = self.get_unique_words(words, minimum_word_frequency)
        self.print_status(None, None, 'Preparing data: 40%', percentage=False)
        reviews = self.clean_reviews(reviews, negation=True, split=True)
        self.print_status(None, None, 'Preparing data: 60%', percentage=False)
        pos_reviews = self.clean_reviews(pos_reviews, negation=False, split=False)
        self.print_status(None, None, 'Preparing data: 80%', percentage=False)
        neg_reviews = self.clean_reviews(neg_reviews, negation=False, split=False)
        self.print_status(None, None, 'Preparing data: 100%', percentage=False)
        print()
        print('        -Done')
        for i, review in enumerate(reviews):
            self.print_status(i, length, 'Calculating semantic orientation scores')
            score = 0
            for j, word in enumerate(review):
                if word not in qualified_words or word in unique_words:
                    continue
                if word in negations:
                    score = self.get_negated_so(j, review, pos_reviews, neg_reviews)
                else:
                    score = self.get_so(word, pos_reviews, neg_reviews)
                unique_words.append(word)
                scores.append(score)
        return unique_words, scores


    def get_scores(self, reviews, minimum_word_frequency, pos_reviews, neg_reviews):
        negations = ["ei", "mutta"]
        scores = []

        self.print_status(None, None, 'Preparing data: 0%', percentage=False)
        pos_reviews = self.clean_reviews(pos_reviews, negation=False, split=True)
        self.print_status(None, None, 'Preparing data: 33%', percentage=False)
        neg_reviews = self.clean_reviews(neg_reviews, negation=False, split=True)
        self.print_status(None, None, 'Preparing data: 66%', percentage=False)
        words = self.clean_reviews(reviews, negation=False, split=True)
        self.print_status(None, None, 'Preparing data: 100%', percentage=False)
        print()
        print('        -Done')
        unique_words = self.get_unique_words(words, minimum_word_frequency)
        length = len(unique_words)
        print()
        print('        -Done')
        for i, word in enumerate(unique_words):
            self.print_status(i, length, 'Calculating semantic orientation scores')
            score = self.get_so(word, pos_reviews, neg_reviews)
            scores.append(score)
        return unique_words, scores


    def get_sentiment_lexicon(self, data, minimum_word_frequency, positive_rating_limit, negative_rating_limit, detect_negation):    
        data.iloc[:, 0] = data.iloc[:, 0].apply(str)

        pos_rev, _, neg_rev = self.classify_text(data, positive_rating_limit, negative_rating_limit)
        print()
        print('        -Done')

        words, scores = [], []
        if detect_negation:
            words, scores = self.get_negated_scores(data.iloc[:, 0], minimum_word_frequency, pos_rev, neg_rev)
        else:
            words, scores = self.get_scores(data.iloc[:, 0], minimum_word_frequency, pos_rev, neg_rev)
        print()
        print('        -Done')
        return words, scores


class SentimentClassifier():
    def __init__(self, words, scores):
        self.words = words
        self.scores = scores

    def classify(self, texts, slc):
        texts_cleaned = slc.clean_reviews(texts, negation=False, split=True)
        sentiments = []
        for text in texts_cleaned:
            score = 0
            for word in text:
                if word in self.words:
                    score += self.scores[self.words.index(word)]
            if score > 0:
                sentiments.append('Positive')
            elif score < 0:
                sentiments.append('Negative')
            else: 
                sentiments.append('Neutral')
        return texts, sentiments


def parse_file_name(file_name):
    possible_extension = file_name[len(file_name) - 4:]
    if possible_extension == '.csv':
        return file_name
    return file_name + '.csv'


def main():
    print()
    print()
    print('#' * 80)
    print('-' * 38 + 'Lexi' + '-' * 38)
    print(' ' * 27 + 'Sentiment lexicon creator')
    print(' ' * 38 + 'and')
    print(' ' * 35 + 'classifier')
    print('#' * 80)
    print()
    print()
    print()

    current_directory = os.getcwd()
    current_directory = current_directory[:len(current_directory) - 8]
    file_name = input("CSV file's name: ")
    file_name = parse_file_name(file_name)
    file_path = current_directory + file_name
    minimum_word_frequency = input('Minimum word frequency in the given corpus: ').strip().lower()
    if minimum_word_frequency == '':
        minimum_word_frequency = 5
    positive_rating_limit = input("Rating is positive if it's larger than: ").strip().lower()
    if positive_rating_limit == '':
        positive_rating_limit = 3
    negative_rating_limit = input("Rating is negative if it's smaller than: ").strip().lower()
    if negative_rating_limit == '':
        negative_rating_limit = 3
    detect_negation = input("Use negation detection when calculating sentiment orientation score? [y/n]: ").strip().lower()
    if detect_negation == 'y':
        detect_negation = True
    else:
        detect_negation = False

    print()
    print('Reading file...')
    data = pd.read_csv(file_path)
    print('-Done')

    print()
    print('Creating sentiment lexicon...')
    slc = SentimentLexiconCreator()
    words, scores = slc.get_sentiment_lexicon(data, int(minimum_word_frequency), int(positive_rating_limit), int(negative_rating_limit), detect_negation)
    #sentiments = ['positive' if score > 0 'negative' if score < 0 else 'neutral' for score in scores if score]
    print('-' * 80)
    print('Sentiment lexicon done')
    print('-' * 80)

    classify_or_not = input('Do you want to use classification? [y/n]: ').strip().lower()
    if classify_or_not == 'y':
        sc = SentimentClassifier(words, scores)
        classification_file_name = input("Classification file's name: ")
        classification_file_name = parse_file_name(classification_file_name)
        if classification_file_name == '':
            classification_file_name = file_name
        file_path = current_directory + classification_file_name

        print()
        print('Reading file...')
        data = pd.read_csv(file_path)
        print('-Done')

        print()
        print('Classifying...')
        texts = data.iloc[:, 0].apply(str)
        texts, sentiments = sc.classify(texts, slc)
        print('-Done')
        
        print()
        file_name = input('File name for classification results: ')
        file_name = parse_file_name(file_name)
        results = pd.DataFrame({'data': texts, 'sentiment': sentiments})
        results.to_csv(current_directory + file_name, index=False)
        print(f'File "{file_name}" has been saved to "{current_directory}"')

    print()
    save_or_not = input('Do you want to save the created lexicon? [y/n]: ').strip().lower()
    if save_or_not == 'y':    
        file_name = input('File name for the created lexicon: ')
        file_name = parse_file_name(file_name)
        output = pd.DataFrame({'word': words, 'score': scores})
        output.to_csv(current_directory + file_name, index=False)
        print(f'File "{file_name}" has been saved to "{current_directory}"')
    return


if __name__ == '__main__':
    main()

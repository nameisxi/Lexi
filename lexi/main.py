import os

import numpy as np
import pandas as pd

#from .slc import SentimentLexiconCreator

#######################################################################################################################
#slc.py


class SentimentLexiconCreator:
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
                scores.append('undefined')
                continue
            score = positive_pmi - negative_pmi
            scores.append(score)
        return scores

    def get_sentiment_lexicons(self, data, minimum_word_frequency, positive_rating_limit, negative_rating_limit):
        print('        Separeting words...')
        qualifying_words, qualifying_word_counts = self.get_words(data.iloc[:, 0], minimum_word_frequency)
        print('        -Done')

        print('        Classifying reviews...')
        positive_text, neutral_text, negative_text = self.classify_text(data, positive_rating_limit, negative_rating_limit)
        print('        -Done')
        
        print('        Separeting positive and negative words...')
        qualifyin_positive_words, qualifying_positive_word_counts = self.get_words(positive_text, 1)
        qualifying_negative_words, qualifying_negative_word_counts = self.get_words(negative_text, 1)
        print('        -Done')

        print('        Calculating semantic orientation scores...')
        scores = self.semantic_orientation_score(positive_text, negative_text, qualifying_words, qualifying_word_counts, qualifyin_positive_words, qualifying_positive_word_counts, qualifying_negative_words, qualifying_negative_word_counts)
        print('        -Done')
        
        return qualifying_words, scores


#######################################################################################################################


#######################################################################################################################
#sc.py

class SentimentClassifier():
    def __init__(self, words, lexicon):
        self.words = words
        self.lexicon = lexicon

    def get_words(self, text):
        words = []
        text = text.replace('!', '.')
        text = text.replace('?', '.')
        text = text.replace('\n', '.')
        text = text.replace('-', '.')
        text = text.replace(',', '.')
        sentences = text.split('.')
        for sentence in sentences:
            words = sentence.split(' ')
            for word in words:
                words.append(word.lower())
        return words

    def classify(self, text):
        words = self.get_words(text)
        score = 0
        for i in range(len(words)):
            word = words[i]
            if word in self.words:
                lexicon_score = self.lexicon[words.index(word)]
                if lexicon_score != 'undefined':
                    score += lexicon_score
        if score > 0:
            return 'Positive'
        elif score < 0:
            return 'Negative'
        return 'Neutral'

#######################################################################################################################


def parse_file_name(file_name):
    possible_extension = file_name[len(file_name) - 4:]
    if possible_extension == '.csv':
        return file_name
    return file_name + '.csv'

def help():
    print('')
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('+    Example:')
    print('+    Restaurant reviews with a rating range of 0 to 10')
    print('+    Example CSV file:')
    print('+                         ')
    print('+    | Reviews | Ratings |')
    print('+    +-------------------+')
    print('+    | "Test"  |    7    |')
    print('+    | "Test 2"|    3    |')
    print('+    | "Test 3"|    10   |')
    print('+    +-------------------+')
    print('+                         ')
    print("+    CSV file's name (with extension): example_file.csv")
    print('+    Minimum word frequency in the given corpus: 5')
    print("+    Rating is positive if it's larger than: 5")
    print("+    Rating is negative if it's smaller than: 5")
    print('+    Reading file...')
    print('+    Creating sentiment lexicon...')
    print('+    -----------------------')
    print('+    Sentiment lexicon done')
    print('+    -----------------------')
    print('+    File name for the created lexicon (without extension): sentiment_lexicon')
    print('+    File "sentiment_lexicon.csv" has been saved to "./current/directory/"')
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('')


def main():
    print('')
    print('')
    print('#############################')
    print('------------Lexi------------')
    print(' Sentiment lexicon creator  ')
    print('            and             ')
    print('         classifier         ')
    print('#############################')
    print('')
    print('')
    print('The given file should be in CSV file format.')
    print('It also should have atleast two columns.')
    print("The first column should have all the text that's")
    print('going to be analyzed, and the second column should')
    print("have all the ratings for the given text's.")
    print('Type "help" for an example.')
    print('')

    current_directory = os.getcwd()
    current_directory = current_directory[:len(current_directory) - 9]
    file_path = None
    minimum_word_frequency = None
    positive_rating_limit = None
    negative_rating_limit = None

    run = True
    while run:
        file_name = input("CSV file's name: ")
        file_name = parse_file_name(file_name)
        file_path = current_directory + file_name
        if file_name.strip().lower() == 'help':
            help()
            continue
        minimum_word_frequency = input('Minimum word frequency in the given corpus: ')
        if minimum_word_frequency.strip().lower() == 'help':
            help()
            continue
        positive_rating_limit = input("Rating is positive if it's larger than: ")
        if positive_rating_limit.strip().lower() == 'help':
            help()
            continue
        negative_rating_limit = input("Rating is negative if it's smaller than: ")
        if negative_rating_limit.strip().lower() == 'help':
            help()
            continue

        run = False

    print('')
    print('Reading file...')
    data = pd.read_csv(file_path)

    print('')
    print('Creating sentiment lexicon...')
    slc = SentimentLexiconCreator()
    words, lexicons = slc.get_sentiment_lexicons(data, int(minimum_word_frequency), int(positive_rating_limit), int(negative_rating_limit))

    print('-----------------------')
    print('Sentiment lexicon done')
    print('-----------------------')

    classify_or_not = input('Do you want to classify texts after creating the lexicon? [y/n]: ').strip().lower()
    #classify_or_not = 'n'
    if classify_or_not == 'y':
        text = None
        run = True
        while run:
            text = input('Text to be classified: ').strip().lower()
            if text == 'help':
                help()
                continue
            run = False
        sc = SentimentClassifier(words, lexicons)
        sentiment = sc.classify(text)
        print('Sentiment:', sentiment)

    save_or_not = input('Do you want to save the created lexicon? [y/n]: ').strip().lower()
    if save_or_not == 'y':    
        file_name = input('File name for the created lexicon: ')
        file_name = parse_file_name(file_name)
        output = pd.DataFrame({'word': words, 'lexicon': lexicons})
        output.to_csv(current_directory + file_name, index=False)
        print(f'File "{file_name}" has been saved to "{current_directory}"')
        return


if __name__ == '__main__':
    main()

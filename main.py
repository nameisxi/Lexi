import os

import numpy as np
import pandas as pd

from sentiment-lexicon-creator import SentimentLexiconCreator


def parse_file_name(file_name):
    possible_extension = file_name[len(file_name) - 4:]
    if possible_extension == '.csv':
        return file_name[:len(file_name) - 4]
    return file_name

def help():
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


def main():
    print('############################')
    print('Sentiment Lexicon Creator')
    print('############################')
    print('The given file should be in CSV file format.')
    print('It also should have atleast two columns.')
    print("The first column should have all the text that's")
    print('going to be analyzed, and the second column should')
    print("have all the ratings for the given text's.")
    print('Type "help" for an example.')

    file_path = None
    minimum_word_frequency = None
    positive_rating_limit = None
    negative_rating_limit = None

    run = True
    while run:
        file_name = input("CSV file's name: ")
        file_name = parse_file_name(file_name)
        file_path = './' + file_name
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
        
    file_name = input('File name for the created lexicon (without extension): ')
    file_name = parse_file_name + '.csv'
    output = pd.DataFrame({'word': words, 'lexicon': lexicons})
    output.to_csv(file_name)

    current_directory = os.getcwd()
    print(f'File "{file_name}" has been saved to "{current_directory}"')



if __name__ == '__main__':
    main()

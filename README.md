# Lexi

## What is Lexi and why use it:
Lexi is first and foremost a polarity lexicon creator and it can give a prediction based on a created lexicon. The actual polarity lexicon creation process is based on a semantic orientation score, which is a well-known method to calculate polarities for words. It's not deep learning, but it works.

## Installation:
1. Clone this project

## How to use Lexi:
0. Your dataset has to be in CSV format with atleast two columns. 
   The first two columns need to have the following structure:
   
| text_data | rating_data |
| --------- | ----------- |
| String | Integer or Float |

For example:

| text_data | rating_data |
| --------- | ----------- |
| This is an example | 3 |
| This also is an example | 7 |

1. Run the main.py file located at the src subfolder

2. Give Lexi your dataset's name. It should be located in the same directory where you cloned Lexi to.

3. Give Lexi the threshold count on which word is considered relevant (= how many times it needs to appear to be relevant).

4. Give Lexi the positive rating threshold (= rating that is larger than the given value is considered positive).

5. Give Lexi the negative rating threshold (= rating that is smaller than the given value is considered negative).

6. Tell Lexi to use, or not to use negation detection (using negation detection usually boosts the accuracy a little bit).

7. Tell Lexi to classify, or not to classify documents based on your generated lexicon. If you decide to classify documents, Lexi will prompt you to give a to be classified file's name and it also expects it to be found in the same directory to which you cloned Lexi to. After the classification process, Lexi's going to ask a filename for the classification results.

8. Tell Lexi to save, or not to save the created lexicon. If you decide to save the lexicon, Lexi's going to prompt you for a filename.

9. If everything went fine, and you decided to save your lexicon and/or classification results, the relevant files should be located in the directory where you clone Lexi to.

Example lexicon from the previous "data":

| word | score |
| --------- | ----------- |
| this | -0.3219280948873623 |
| example | -0.3219280948873623 |
| also | 0.6780719051126377 |
| an | -0.3219280948873623 |
| is | -0.3219280948873623 |

Example classification results from the previous "data":

| data | sentiment |
| --------- | ----------- |
| This is an example | Negative |
| This also is an example | Positive |

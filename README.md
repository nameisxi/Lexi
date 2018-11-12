# Lexi
### Sentiment classifier and lexicon creator

#### Installation:
1. Clone this project

   Example:
```console
foo@bar:~$ git clone https://github.com/nameisxi/Lexi.git
foo@bar:~$ ls
Lexi
```
#### How to use Lexi:
1. Either clone this project to the same directory where your file to be used is located at,
   or just move that file to the same directory where you cloned Lexi to. 
   
Example:
```console
foo@bar:~/your/location/$ ls
Lexi  file-to-be-used.csv
```

2. Run the main file:
```console
foo@bar:~/your/location/$ ls
Lexi  file-to-be-used.csv
foo@bar:~$ cd Lexi
foo@bar:~$ ls
lexi  LICENSE.txt  README.md
foo@bar:~$ cd lexi
foo@bar:~$ ls
main.py
foo@bar:~$ python3 main.py


#############################
------------Lexi------------
 Sentiment lexicon creator  
            and             
         classifier         
#############################


The given file should be in CSV file format.
It also should have atleast two columns.
The first column should have all the text that's
going to be analyzed, and the second column should
have all the ratings for the given text's.
Type "help" for an example.
```
3. Follow along the prompted questions:

CSV file's name = The name of the CSV file to be used.
```console
CSV file's name: file-to-be-used
```

Minimum word frequency in the given corpus = How many times does a word have to come up in your dataset, to be counted.
```console
Minimum word frequency in the given corpus: 5
```

Rating is positive if it's larger than = Rating that is considered to be positive. Say you had a dataset of movie reviews (ratings on a scale of 1 to 5) and you would classify 4 & 5 to be positive, then you would answer 3, because 4 and 5 both are larger than 3.
```console
Rating is positive if it's larger than: 3
```

Rating is negative if it's smaller than = Rating that is considered to be negative. Say you had a dataset of movie reviews (ratings on a scale of 1 to 5) and you would classify 1 & 2 to be negative, then you would answer 3, because 1 and 2 both are smaller than 3.
```console
Rating is negative if it's smaller than: 3
```

4. If everything went fine, you should see this output:
```console
Reading file...

Creating sentiment lexicon...
        Separeting words...
        -Done
        Classifying reviews...
        -Done
        Separeting positive and negative words...
        -Done
        Calculating semantic orientation scores...
        -Done
-----------------------
Sentiment lexicon done
-----------------------
```

5. After this, you still have couple of questions to be answered:

Answer y if you want to get the sentiment of a given text based on the created lexicon, answer n if you're here
just for the lexicon.
```console
Do you want to classify texts after creating the lexicon? [y/n]: y
```

if you answered y, there should be a prompt asking for the specific text you want to classify.
```console
Text to be classified: This is my test text. It can be classified as positive, neutral, or negative based on the lexicon.
Sentiment: Neutral
```

Answer y if you want to save the created lexicon, otherwise answer n.
```console
Do you want to save the created lexicon? [y/n]: y
```

If you answered y, you'll be asked for the filename, of the created lexicon.
```console
File name for the created lexicon: results
File "results.csv" has been saved to "/your/location/"
```






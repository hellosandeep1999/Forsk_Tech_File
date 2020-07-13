"""
NLP Stands for Natural Language Processing

How computer understands what we speak, since it is not c/c++/java or Assembly Language

Also the Human language is evolving which is becoming more difficult 
for computers to understand

Give example of Rajasthani Language which changes its dialect every 3 kilometers

Give perfect example of Google Translate for a AI based NLP product 

Alexa is voice based search , also uses NLP and AI in the background

Text-based communication has become one of the most common forms of expression. 
We email, text message, tweet, and update our statuses on a daily basis. 
As a result, unstructured text data has become extremely common, 
and analyzing large quantities of text data is now a key way to understand 
what people are thinking.

Tweets on Twitter help us find trending news topics in the world. 

Reviews on Amazon help users purchase the best-rated products

These examples of organizing and structuring knowledge represent NLP tasks


How to process text data
NLP is a field of computer science that focuses on the interaction between 
computers and humans. 
NLP techniques are used to analyze text, providing a way for computers 
to understand human language.

NLP is the ability of Computer program to understand human langauge 

Libraries - NLTK(from Standford), TextBlob, Gensim, 
            spaCy, polyglot, Stanford Core NLP, Vader
"""






# Explain Restaurant_Review.tsv  ( tab seperated values ) 
# Data is scrapped from the feedback and manually tagged as LIKED 1 or NOT LIKED 0
# Training 10K data manually to tag the reviews as Positive / Negative 
# So for a new review we need to predict whether it is GOOD or BAD
# So is this a Regression or Classification problem ?
# Supervised ML - Sentiment Analysis/Opinion Mining is the focus of today 
# Example of Movie Review ( Positive / Negative ), 
# Social Media comments
# Article Tagging 
# Daily Hunt App

"""
Our Classification Algorithm only understand number

How to convert the textual data into numbers ?
NLP Steps
    1. Noise Removal / Stopword Removal 
    2. Lexicon Normalization - Stemming
    3. Vectorisation / Bag of Words Model
    4. Creation of Machine Learning Model 


Step 1: Noise Removal / Stopword Removal / Clean Up Process
        this is good     ---> positive 
        good             ---> positive  ( removal of this and is stopwoods)

        Stopwords removing = remove articles from the sentense does not 
                             change the sentiments of the statement      



Step 2: Stemming is the process to find the root form of word ( first form )
        hated, hating, loving, loved
        hate and love
        
        
Step 3: Vectorisation
        Convert text data to numeric form
        We would label Encode and then OneHotEncoding
        

Step 4: ML - classification to build the model        
"""

# Importing the libraries
import pandas as pd

# Importing the dataset
# Ignore double qoutes, use 3 
dataset = pd.read_csv('data/Restaurant_Reviews.tsv', delimiter = '\t')


# Cleaning the texts
# Noise removal
""" language stopwords 
(commonly used words of a language – is, am, the, of, in etc), 
URLs or links, social media entities (mentions, hashtags), 
punctuations and industry specific words. 
This step deals with removal of all types of noisy entities present in the text.
"""

#python -c "import nltk"
# !pip install nltk


import nltk
# download the latest list of stopwords from Standford Server 
#nltk.download('stopwords')
from nltk.corpus import stopwords


# Stemming:  Stemming is a rudimentary rule-based process 
# of stripping the suffixes (“ing”, “ly”, “es”, “s” etc) from a word.
"""
The most common lexicon normalization practices are :

Stemming:  Stemming is a rudimentary rule-based process of stripping the 
suffixes (“ing”, “ly”, “es”, “s” etc) from a word.

Lemmatization: Lemmatization, on the other hand, is an organized 
& step by step procedure of obtaining the root form of 
the word, it makes use of vocabulary (dictionary importance of words) 
and morphological analysis (word structure and grammar relations).
"""

#For Stemming use the PorterStemmer class object 
from nltk.stem.porter import PorterStemmer
#from nltk.stem.wordnet import WordNetLemmatizer 



"""
Apply the process to one line of text
This will help in understanding the below logic
"""
#perform row wise noise removal and stemming
#let's do it on just first row data
# Wow... Loved this place.    1


import re
print(dataset['Review'][0])


"""
Search through regex for special character set , using the substitute function 
substitute the regex with space ' ' 
[^a-zA-Z ] finds those which does not belong to a to z or A to Z
"""
review = re.sub('[^a-zA-Z]', ' ', dataset['Review'][0])
print(review)

review = review.lower()
print(review)

review = review.split()
print(review)


#We need to check whether it is a stopword, if YES then remove it
review = [word for word in review 
          if not word in set(stopwords.words('english'))]
    
print(review)


#lem = WordNetLemmatizer() #Another way of finding root word
ps = PorterStemmer()

review = [ps.stem(word) for word in review]
print(review)


review = ' '.join(review)
print(review)


#now do the same for every row in dataset. run to loop for all rows

# Add into this bigger list
corpus = []
 
for i in range(0, 1000):
    review = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i])
    review = review.lower()
    review = review.split()
    review = [word for word in review if not word in set(stopwords.words('english'))]
    
    ps = PorterStemmer()
    review = [ps.stem(word) for word in review]
    
    review = ' '.join(review)
    
    corpus.append(review)

print(corpus)
print(len(corpus))


# Creating the Bag of Words model
# Also known as the vector space model
# Text to Features (Feature Engineering on text data)
# Conversion of text to Numeric data is known as Feature Extraction 
"""
Rahul   -   nice place
Nitish  -   good one
Ravi    -   awesome

How to convert the above into numneric form ?

New column are created for each unique word

Then it applies a logic similar to OneHotEncoding, but in Onehot there use to 
be one 1 in each row
If good comes twice then it will come twice in the column

nice    place   good    one     awesome
1        1        0      0        0
0        0        1      1        0
0        0        0      0        1

This process is known as Vectorisation of your text
This concept is known as Bag of Words model in NLP

There are other ways to convert text to numerical ways
    1. Bag of Words 
    2. TF-IDF ( compressed way, does not create too much columns )
    3. Word Embedding ( used in Deep Learning)
"""  

"""
internally it creates a dictionary of unique words with values as the count
{
"nice" : 1,
"place" : 1,
"good" : 1,
"one" : 1,
"awesome" : 1
}
top 1500 unique needs to be taken
"""
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 1500)

# it is known as sparse matrix of the features ND Array
features = cv.fit_transform(corpus).toarray() # 1500 columns
labels = dataset.iloc[:, 1].values

print(features.shape)
print(labels.shape)


# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
features_train, features_test, labels_train, labels_test = \
train_test_split(features, labels, test_size = 0.20, random_state = 0)



#applying knn on this text dataset
# Fitting Knn to the Training set
from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier()
classifier.fit(features_train, labels_train)

# Predicting the Test set results
labels_pred = classifier.predict(features_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm_knn = confusion_matrix(labels_test, labels_pred)
print(cm_knn) 
# for better NLP results we need lot of data

# Fitting Naive Bayes to the Training set
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(features_train, labels_train)

# Predicting the Test set results
labels_pred = classifier.predict(features_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm_nb = confusion_matrix(labels_test, labels_pred)
print(cm_nb)
# for better NLP results we need lot of data


# How to predict for a new data ?
# We need to follow the same steps and create the sparse matrix for it 
# only transform and not fit_transform 



"""
Q1. Code Challegene (NLP)
Dataset: amazon_cells_labelled.txt


The Data has sentences from Amazon Reviews

Each line in Data Set is tagged positive or negative

Create a Machine learning model using Natural Language Processing that can 
predict wheter a given review about the product is positive or negative

"""


"""
Q2. Code Challenge (Connecting Hearts)


What influences love at first sight? (Or, at least, love in the first four minutes?) 
This dataset was compiled by Columbia Business School Professors Ray Fisman and Sheena Iyengar 
for their paper Gender Differences in Mate Selection: Evidence from a Speed Dating Experiment.

Data was gathered from participants in experimental speed dating events from 2002-2004. 
During the events, the attendees would have a four minute "first date" with 
every other participant of the opposite sex. At the end of their four minutes, 
participants were asked if they would like to see their date again.

They were also asked to rate their date on six attributes: Attractiveness, 
Sincerity, Intelligence, Fun, Ambition, and Shared Interests.

The dataset also includes questionnaire data gathered from participants at different points in the process.

These fields include: demographics, dating habits, self-perception across 
key attributes, beliefs on what others find valuable in a mate, and lifestyle information.

See the Key document attached for details of every column and for the survey details.


What does a person look for in a partner? (both male and female)


For example: being funny is more important for women than man in selecting 
a partner! Being sincere on the other hand is more important to men than women.

What does a person think that their partner would look for in them? Do you 
think what a man thinks a woman wants from them matches to what women 
really wants in them or vice versa. TIP: If it doesn’t then it will be one sided :)

Plot Graphs for:
How often do they go out (not necessarily on dates)?
In which activities are they interested?
    
If the partner is from the same race are they more keen to go for a date?
What are the least desirable attributes in a male partner? Does this differ 
for female partners?
How important do people think attractiveness is in potential mate selection 
vs. its real impact?


"""

"""
Q3 movie.csv 

Program Specification

Import movie.csv file

There are two categories: Pos (reviews that express a positive or favorable sentiment) 
and Neg (reviews that express a negative or unfavorable sentiment). 
For this assignment, we will assume that all reviews are either positive or negative; 
there are no neutral reviews.

Perform sentiment analysis on the text reviews to determine whether its positive 
or negative and build confusion matrix to determine the accuracy.

"""



# Skip from here onwards

"""
https://www.analyticsvidhya.com/blog/2017/01/ultimate-guide-to-understand-implement-natural-language-processing-codes-in-python/
https://www.analyticsvidhya.com/blog/2014/11/text-data-cleaning-steps-python/
"""

"""
Naive Bayes
https://monkeylearn.com/blog/practical-explanation-naive-bayes-classifier/
"""

"""
What's the difference between  a naive Bayes classifier and a Bayesian network?


Naive Bayes assumes that all the features are conditionally 
independent of each other. This therefore permits us to use the 
Bayesian rule for probability. Usually this independence 
assumption works well for most cases, if even in actuality
 they are not really independent.
Bayesian network does not have such assumptions. 
All the dependence in Bayesian Network has to be modeled. 
The Bayesian network (graph) formed can be learned by the 
machine itself, or can be designed in prior, by the developer, 
if he has sufficient knowledge of the dependencies.

"""
"""
the usual deep learning libraries that provide 
tensor algebra primitives and few other utilities to 
code models, while at the same time making it more general than other 
specialized libraries like PyText, StanfordNLP, AllenNLP, and OpenCV.
"""
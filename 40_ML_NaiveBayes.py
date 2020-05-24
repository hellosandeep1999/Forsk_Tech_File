# First run the code and show and then explain the math behind it

"""
Naive Bayes flavour ( variants )
    1. Gaussian     ( for continuous data like numerical )
    2. Bernolli     ( for discrete values like 0 or 1 )
    3. Multinomial  ( for text data like NLP )
"""
     
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB

# Importing dataset
data = pd.read_csv("training_titanic.csv")

print(data.shape)


# Convert categorical variable to numeric ( Label Encoding )
# Label Encoding using numpy

data["Sex_cleaned"]=np.where(data["Sex"]=="male",0,1)

print(data.shape)


data["Embarked_cleaned"]=np.where(data["Embarked"]=="S",0,
                                  np.where(data["Embarked"]=="C",1,
                                           np.where(data["Embarked"]=="Q",2,3)
                                          )
                                 )
                                  
                                  # S == 0  C == 1  Q == 2  anyother == 3
print(data.shape)
             

                     
# Cleaning dataset of NaN
# This will delete the data which has categorical data and missing rows
data.isnull().any(axis=0)
data=data[[
    "Survived",
    "Pclass",
    "Sex_cleaned",
    "Age",
    "SibSp",
    "Parch",
    "Fare",
    "Embarked_cleaned"
]].dropna(axis=0, how='any')  # any and all reference to the columns

print(data.shape)  # this has deleted the missing data rows


# Split dataset in training and test datasets
from sklearn.model_selection import train_test_split

# We have not seperated the feature and label, we have given the whole data
# thats why we only have features test and train 
# we have taken care where we are training the model in fit method
features_train, features_test =\
train_test_split(data, test_size=0.5, random_state=0)
#  we are passing full data as features and no labels are passed


gnb = GaussianNB()

used_features =[
    "Pclass",
    "Sex_cleaned",
    "Age",
    "SibSp",
    "Parch",
    "Fare",
    "Embarked_cleaned"
]  # "Survived" is the column for labeleling 

# Train classifier
gnb.fit(
    features_train[used_features].values,  # features are passed
    features_train["Survived"].values      # labels is passed
)


labels_pred = gnb.predict(features_test[used_features])


# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm_gnb = confusion_matrix(features_test["Survived"], labels_pred)
print(cm_gnb)

# Score
print( (cm_gnb[0][0] + cm_gnb[1][1]) / (cm_gnb[0][0] + cm_gnb[1][1] + cm_gnb[0][1] + cm_gnb[1][0]))
#0.7647058823529411

mnb = MultinomialNB()
used_features =[

    "Pclass",
    "Sex_cleaned",
    "Age",
    "SibSp",
    "Parch",
    "Fare",
    "Embarked_cleaned"
   
]

# Train classifier
mnb.fit(
    features_train[used_features].values,
    features_train["Survived"].values
)
labels_pred = mnb.predict(features_test[used_features])

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm_mnb = confusion_matrix(features_test["Survived"], labels_pred)
print(cm_mnb)


print( (cm_mnb[0][0] + cm_mnb[1][1]) / (cm_mnb[0][0] + cm_mnb[1][1] + cm_mnb[0][1] + cm_mnb[1][0]))
#0.6694677871148459

bnb = BernoulliNB()
used_features =[

    "Pclass",
    "Sex_cleaned",
    "Age",
    "SibSp",
    "Parch",
    "Fare",
    "Embarked_cleaned"
   
]

# Train classifier
bnb.fit(
    features_train[used_features].values,
    features_train["Survived"]
)
labels_pred = bnb.predict(features_test[used_features])

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm_bnb = confusion_matrix(features_test["Survived"], labels_pred)
print(cm_bnb)

print( (cm_bnb[0][0] + cm_bnb[1][1]) / (cm_bnb[0][0] + cm_bnb[1][1] + cm_bnb[0][1] + cm_bnb[1][0]))
#0.7478991596638656


# Now explain the pdf ( Multinomial Naive Bayes )
# Naive Bayes is a probability based Model
# If A very Close Game is directly in the training data , 
# then probability is easy 
# We can just count how many times it is coming
# To twist the solution we will use the Bayes Theorem 
# So it is based on Bayes Theorem and Naive Principle ( Naive bayes)
# Since demoninators are same we would only calculate Numerators 
# Taking P(Sports) is 3/5 and P(Not Sports) is 2/5 , its easy to calculate 
# P(a very close game/sports) and P(a very close game/Not sports) needs to be calculated
# for which we require Naive Principle
# How to handle the case of ZERO, which will make everything 0
# Laplace smoothening or correction  or Additive Smoothening is the solution 
# 14 total unique words are there
# We dont every time add 1 but we add alpha
# alpha can be any value greater than 1
# alpha needs to be multipled by unique counts in the denominator (alpha*unique)


"""
Q1. dataset: 
    pima-indians-diabetes.csv

Perform both Multinomial and Gaussian Naive Bayes classification 
after taking care of NA values (maybe replaced with zero in dataset)

Calculate accuracy for both Naive Bayes classification model.

"""


#https://towardsdatascience.com/naive-bayes-classifier-81d512f50a7c
#https://hub.packtpub.com/implementing-3-naive-bayes-classifiers-in-scikit-learn/














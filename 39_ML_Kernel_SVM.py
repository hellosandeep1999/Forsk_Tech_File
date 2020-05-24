"""
                             Classification Algo
                                /           \
                               /             \
                              /               \
                Support Vector Machine    Naive Bayes
                        ( SVM )                        (NB)
                        
Bayes Probablity Theorm and Naive Principle based.
There is Support Vector Regressor(SVR) used for Regression


SVM is popular for solving NLP ( Natural Language Processsing ) problems
Sentiment Analysis in NLP is used to get the polarity, opinion mining, positive / Negative
NLP is text processing to detect text classification 
For such classification, we used either SVM or NB

Two types of dataset  
1. Labelled (features,label)  
2. Unlabelled (features)
Photograph of the class with the name and without names is an example to explain
             
   
Concept to understand before SVM
1. Linearly seperable data
2. Linearly Inseperable data 

Show image svm-01.png

Straight decission boundary seperates the data 
We can handle this throught Logistic Regression 

Show image svm-03.png
decission boundary just like Logistic Regression can linearly seperate data
This line is known as Hyperplane
Hyperplane is usually taken in Higher Dimension data
Hyperplane in 2D is simply a straight line
Support Vector is the nearest point to the line ( perpendicular distance is least)

How this line is drawn is based on a simple logic
Show image svm-02.png

As we had drawn a Best Fit Line in regression, whose residual was minimum

Our SVM draws the Best Fit Line, to linearly seperate this data
whose funtionaly margin is maximum

The nearest point are necessary when we draw this line
We need to keep the distance maximum, that line which helps in that is the decisison boundary
Best hyperplane to seperate, whose margin is maximum, if data is exactly seperable


For linearly non seperable data
Show image svm-03.png part 2
We can no doubt try to use straight line to seperate it, 
but classifications  would be wrong


How to classify such data 
To Solve this we can use SVM, 
SVM should not be used to classify linearly seperable data
but best is to use it to classify non linearly seperable data

How to create hyperplane ?
Assume it as a rubber sheet, the points which are plotted on 2D plane
Elastic pull the points in the centre.
Green points would be in the 2D Plane, Blue points 
Now data is coming in 3D, z axis
Now they seems to be seperable
Actually we are converting our 2D data into 3D data
Now cut the rubber with a A4 size paper(hyperplane)
and that will be the decission boundary

To summarise
So if we have linearly non seperable data, then
We need to convert into higher dimension data
After that our data becomes linearly seperable
Then we can cut and create a decission boundary

How to convert 2D to 3D or Low Dimension to Higher Dimension ?
SVM has some methods to do that and they are known as kernel function

There are a lot of kernel function.

SVM with polynomial kernel visualisation
https://www.youtube.com/watch?v=3liCbRZPrZA

Gaussian method will be used as a default kernel function, to convert 2D to 3D
Cut will create a ring in 3D
But the data is in 2D
Now project the ring with a torch on the 2D plane
Put torch to shadow on 2D

This is the way SVM works 

SVM Kernel Function / method 
    1 Polynomial
    2 Gaussian 
    3 RBF
    4 Hyperbolic
    5 Sigmoid
    6 Laplace
    7 Annova
    8 You can make your own customised also
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv("Match_Making.csv")

features = dataset.iloc[:, :-1].values
labels = dataset.iloc[:, -1].values

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size = 0.3, random_state = 0)


# Fitting Kernel SVM to the Training set
# kernels: linear, rbf and poly
# If you want you can make your own customized function to convert 2D to 3D
# Poly takes alot of time to create the visualisation 
# Linear will draw a straight line
# run the code 3 times with 3 different kernel function 

from sklearn.svm import SVC
# SVM ( SVC for classification and SVR for Regression )
classifier = SVC(kernel = 'poly', random_state = 0)
classifier.fit(features_train, labels_train)

# Predicting the Test set results
labels_pred = classifier.predict(features_test)

# Comparing the predicted and actual values
my_frame= pd.DataFrame(labels_pred, labels_test)
print(my_frame)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(labels_test, labels_pred)
print(cm)

# Model Score
print( (cm[0][0] + cm[1][1]) / (cm[0][0] + cm[1][1] + cm[0][1] + cm[1][0]))

# Model Score
score = classifier.score(features_test,labels_test)
print(score)



#Visualization Way New
x_min, x_max = features_train[:, 0].min() - 1, features_train[:, 0].max() + 1
y_min, y_max = features_train[:, 1].min() - 1, features_train[:, 1].max() + 1

xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                     np.arange(y_min, y_max, 0.1))
# Obtain labels for each point in mesh using the model.
# ravel() is equivalent to flatten method.
# data dimension must match training data dimension, hence using ravel
Z = classifier.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

# Plot the points
plt.plot(features_test[labels_test == 0, 0], features_test[labels_test == 0, 1], 'ro', label='Class 1')
plt.plot(features_test[labels_test == 1, 0], features_test[labels_test == 1, 1], 'bo', label='Class 2')
#plot the decision boundary
plt.contourf(xx, yy, Z, alpha=1.0)

plt.show()




# Add a code for SVR also 


"""
Code Challenges

Q1. (Create a program that fulfills the following specification.)

Program Specification:

Import breast_cancer.csv file.

This breast cancer database was obtained from the University of Wisconsin

Hospitals, Madison from Dr. William H. Wolberg.

Attribute Information: (class attribute has been moved to last column)

Sample Code Number(id number)----> represented by column A.

Clump Thickness (1 – 10) ----> represented by column B.
Uniformity of Cell Size(1 - 10)----> represented by column C.
Uniformity of Cell Shape (1 - 10)----> represented by column D.
Marginal Adhesion (1 - 10)----> represented by column E.
Single Epithelial Cell Size (1 - 10)----> represented by column F.
Bare Nuclei (1 - 10)----> represented by column G.
Bland Chromatin (1 - 10)----> represented by column H.
Normal Nucleoli (1 - 10)----> represented by column I.
Mitoses (1 - 10)----> represented by column J.
Class: (2 for Benign and 4 for Malignant)----> represented by column K.
 
A Benign tumor is not a cancerous tumor and Malignant tumor is a cancerous tumor.


Impute the missing values with the most frequent values.
Perform Classification on the given data-set to predict if the tumor is 
cancerous or not.
Check the accuracy of the model.
Predict whether a women has Benign tumor or Malignant tumor, 
if her Clump thickness is around 6, uniformity of cell size is 2, 
Uniformity of Cell Shape is 5, Marginal Adhesion is 3, 
Bland Chromatin is 9, Mitoses is 4, Bare Nuclei is 7, 
Normal Nuclei is 2 and Single Epithelial Cell Size is 2

(you can neglect the id number column as it doesn't seem  a predictor column)



Q2. This famous classification dataset first time used in Fisher’s classic 1936 paper, 
The Use of Multiple Measurements in Taxonomic Problems. 
Iris dataset is having 4 features of iris flower and one target class.

The 4 features are

SepalLengthCm
SepalWidthCm
PetalLengthCm
PetalWidthCm
The target class

The flower species type is the target class and it having 3 types

Setosa
Versicolor
Virginica
The idea of implementing svm classifier in Python is to use the iris 
features to train an svm classifier and use the trained svm model to predict 
the Iris species type. To begin with let’s try to load the Iris dataset.

"""


"""
 
https://www.youtube.com/watch?v=3liCbRZPrZA&feature=youtu.be
https://www.youtube.com/watch?v=1NxnPkZM9bc

https://monkeylearn.com/blog/introduction-to-support-vector-machines-svm/
https://monkeylearn.com/blog/practical-explanation-naive-bayes-classifier/
https://data-flair.training/blogs/svm-kernel-functions/
 
"""

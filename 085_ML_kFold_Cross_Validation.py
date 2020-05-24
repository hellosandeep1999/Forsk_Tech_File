# k-Fold Cross Validation
"""
k-Fold Cross validation 

Score Concept for Regression and Classification 
It is based on the test data

This is not full proof, since its based on test and train split 
and which is based on randonmly generated state value

if the randon state value is not set and 
if they all generate the score, they all will be different

Take an analogy of an external person coming in class and asking questions
randomly from Sandeep, but he is not able to answer it.
What will the external person think ?
Had he asked 5 qesstions from Sandeep would it not been a better evaluation
and similary he should ask from other persons also to evaluate the performance 
of the class.

To check the performance of the model we use new mechanics 

k fold Cross Validation, where we use different set of testing data 


Lets assume 
            dataset = [[1],[2],[3],[4],[5]] 
                            /   \
                           /     \
                          /       \
                    train          test
           [[1],[2],[3],[4]]        [[5]] 

Calculate Score = s1




            dataset = [[1],[2],[3],[4],[5]] 
                            /   \
                           /     \
                          /       \
                    train          test
           [[1],[2],[3],[5]]        [[4]] 

Calculate Score = s2


            dataset = [[1],[2],[3],[4],[5]] 
                            /   \
                           /     \
                          /       \
                    train          test
           [[1],[2],[4],[5]]        [[3]] 

Calculate Score = s3



            dataset = [[1],[2],[3],[4],[5]] 
                            /   \
                           /     \
                          /       \
                    train          test
           [[1],[5],[3],[4]]        [[2]] 

Calculate Score = s4



            dataset = [[1],[2],[3],[4],[5]] 
                            /   \
                           /     \
                          /       \
                    train          test
           [[5],[2],[3],[4]]        [[1]] 

Calculate Score = s5


                 s1+s2+s3+s4+s5
Average Score = ------------------
                       5

This would be a good score, here k=5 which is the fold or iterations


open
https://yihui.name/animation/example/cv-ani/

default k = 10
"""


# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('data/Social_Network_Ads_2.csv')
features = dataset.iloc[:, [2, 3]].values
labels = dataset.iloc[:, 4].values

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
features_train, features_test, labels_train, labels_test = \
train_test_split(features, labels, test_size = 0.25, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
features_train = sc.fit_transform(features_train)
features_test = sc.transform(features_test)

# Fitting Knn to the Training set
from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2)
classifier.fit(features_train, labels_train)

# Predicting the Test set results
labels_pred = classifier.predict(features_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(labels_test, labels_pred)
print(cm) # 93% (64+29/64+29+4+3)is the score
print( (cm[0][0] + cm[1][1]) / (cm[0][0] + cm[1][1] + cm[0][1] + cm[1][0]))



# Applying k-Fold Cross Validation
from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = classifier, X = features_train, y = labels_train, cv = 10)
print ("accuracies is ", accuracies)
print ("mean accuracy is",accuracies.mean())
#print ("std  accuracy is",accuracies.std())


print(features_train.shape)

print(features_test.shape)

"""
Our test or training data is randomly spread
traininig data = 300   ( features_train )
testing data   = 100   ( features_test  )
If we scatter these points on 2D, they would be far from each other

Its difficult to draw the decission boundary which states whether it falls
in state 1 or state 2

Had these points scattered as a dense network, then it would become easy to 
draw the decission boundary

How to generate the dense data set, 
since we dont have that much amount of data

To do that we first need to have the minimum and maximum values in x and y axis
"""

# Visualising the Training set results
# Plot the decision boundary. For that, we will assign a color to each


# Step 1 is to find the minimum and maximum of x and y 
# 0th column is the x values
x_min = features_train[:, 0].min() - 1
x_max = features_train[:, 0].max() + 1
print(x_min)
print(x_max)


# 1st column is the y values
y_min = features_train[:, 1].min() - 1
y_max = features_train[:, 1].max() + 1
print(y_min)
print(y_max)

# Minimum values are in negative and maximum values are positive

# Step 2
# We want to generate more points between these range only
# We need to give minimum and maximum and the difference 
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                     np.arange(y_min, y_max, 0.1))

print(xx.shape)
print(yy.shape)

# x set of values are in xx
# y set of values are in yy

# If v open and check, there is a pattern, 
# x axis values are changing since y = 0
print(xx)


# If v open and check, there is a pattern, 
# y axis values are changing since x = 0
print(yy)


# We need to take x values from first row of xx 
# and y values from the first row of yy 
# These two will make the points
# We want to predict for each points generated for drawing the decission boundary
# For prediction method i need to pass them as one set

# We need to flatten all the data of xx, that will come in one column
# 2D to 1D
xt = xx.ravel()
print(xt.shape)   # 60x62 = 3720
print(xt)

# Then we need to flatten all the data of yy, that will come in one column
# 2D to 1D
yt = yy.ravel()
print(yt.shape)   # 60x62 = 3720
print(yt)


# Need to make them as points now, similar to zip
pt = np.c_[xt,yt]   # similar to pt = zip(xt,yt) or np.concatenate
print(pt)

# To draw the decission boundaryi need to get the prediction
# whether it belongs to which category
# xx yy and Z should have the same shape, so we have to reshape it
Z = classifier.predict(pt)
print(Z.shape)


# We have to reshape the Z as xx and yy 
Z = Z.reshape(xx.shape)
print(Z.shape)
# Z stores the prediction wiht only 2 class 


# Now we need to plot xx , yy and Z, all 3 combination 
# Its a 3D data, but we plot only 2D data in matplotlib
# How to show 3D data into 2D ?
# We can use 2 colors and show one set of xx and yy in GREEN which has Z = 0
# and in RED which has Z = 1
# Such things are known as contours

# we are trying to plot a 3D data now, since we have xx, yy and Z also
# How to show 3D data into 2D form
# So we can use the color to represent the Z value

# Open contour_plot.png

"""
A contour plot is a graph that you can use to explore the potential 
relationship between three variables. 
Contour plots display the 3-dimensional relationship 
in two dimensions, with x- and y-factors (predictors) plotted on the 
x- and y-scales and response values represented by contours.
""" 


#plot the decission boundary
plt.contourf(xx, yy, Z, alpha=1.0)



# I have to overlays the points
# Plot the points

# class = 0 and x coordinate so 0 and y coordinate so 1
plt.plot(features_test[labels_test == 0, 0], features_test[labels_test == 0, 1], 'ro', label='Class 1')


# class = 1 and x coordinate so 0 and y coordinate so 1
plt.plot(features_test[labels_test == 1, 0], features_test[labels_test == 1, 1], 'bo', label='Class 2')


# U can see from the visual and compare it with cm, that 4 points were different
# and si milarly for 3 points 
plt.show()
print(cm)





"""

Q1.bank_note.csv

Program Specification

Suppose you are the manager of a bank and you have the problem of discriminating 
between genuine and counterfeit banknotes. 
You are measuring several distances on the banknote and the width and height of it.

Measuring these values of about 100 genuine and 100 counterfeit banknotes, 
Use the data set to set up a logical regression and is capable of discriminating 
between genuine and counterfeit money classification. (Import banknotes.csv)

(this data set contains data on Swiss francs currency; it has been obtained courtesy of H. Riedwyl )

Check the accuracy of your model using confusion matrix.

Then use k-fold cross validation to find actual mean accuracy of your model.


"""


"""
In K Fold cross validation, the data is divided into k subsets. 
Now the holdout method is repeated k times, such that each time, 
one of the k subsets is used as the test set/ validation set and 
the other k-1 subsets are put together to form a training set. 
The error estimation is averaged over all k trials to get total 
effectiveness of our model. As can be seen, every data point gets 
to be in a validation set exactly once, and gets to be in a 
training set k-1 times. T
his significantly reduces bias as we are using most of the data 
for fitting, and also significantly reduces variance as most of
 the data is also being used in validation set. Interchanging 
 the training and test sets also adds to the effectiveness of 
 this method. As a general rule and empirical evidence,
 K = 5 or 10 is generally preferred, but nothing’s fixed and 
 it can take any value.
 
 ANimation:
     https://yihui.name/animation/example/cv-ani/
"""


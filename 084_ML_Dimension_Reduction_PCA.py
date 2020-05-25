# PCA
# Show machine-learning-cheet-sheet-2.png

"""
1 Dimension  = 1 Feature  in the dataset  ( univariate )
n Dimension  = n Features in the dataset  ( multivariate )

What is PCA?
Dimensionality reduction technique
Concept is to reduce the number of features from the dataset 

There are 2 more techniques for Dimension Reduction 
    1. Forward Elimination
    2. Backward Elimination

We have used this concept earlier, to find the important features using 
the backward Elimination technique based on the p value concept > 5
Only experience feature was important to decide Salary 
and we had converted 4D to 1D

Forward Elimination is also a technique similar to Backward Elimination 
but include one feature by one in increment mode if it affects or has weightage 

There are 2 techniques for Forward Elimination 
    1. Factor Analysis ( LDA )
    2. PCA - Principal Component Analysis


                             Dimension Reduction
                                /           \
                               /             \
                              /               \
                 Backward Elimination   Forward Elimination
                                              /       \
                                             /         \
                                            /           \
                                           /             \ 
                                   Factor Analysis    Principal Component Analysis
                                       ( LDA )             (PCA)


In PCA only take Primary or principal features and remove others
where its assume m is the original dimension of the dataset 
and k is the reduced dimension of the dataset 
k < m

There is always loss when we convert the data from higher dimension to lower dimension 

It reduces the size of the space which improves the performance of the model

Reduces the risk of overfitting
Algo runs faster when dimension is less
Simplifies the dataset, facilitates description, visualisation and insight

PCA in everyday, we take photos/selfie from the camera, we are converting 
from 3D world to 2D printable photo

Give example of 2 eyes of human being to find the depth, since with one eye we 
can only get width and height

Explain the Webpage 
http://www.lauradhamilton.com/introduction-to-principal-component-analysis-pca


Lets scatter the  points on xy plane where x axis is feature 1 and y axis is feature 2
and lets denote with x1 and x2 respectively 

In Trignometry,
When you are walking on  x axis, where y value is zero, 
i.e on x axis there is only variance in x1 feature and no variance of x2 feature

When you are walking on  y axis, where x value is zero, 
i.e on y axis there is only variance in x2 feature and no variance of x1 feature

If we draw a line at 45 degree, then it represents the line which has 
collective max changes of x1 and x2 feature = 
So this is the line where you have the max_variance in x1 and x2 together

Lets draw a line at 45 degree from the origin

Lets draw a 90 degree projection of all the points on the max variance line

Focus on all the new points

Lets assume that the new line is new x' axis, then all points are on the x' axis 
and y' is zero, that is it has only x1 feature and no x2 feature

So now we have 1D data converted from 2D in a new coordinate system

There is a loss in the new coordinate system 

This axis/line is known as 1st Principal Component

The other axis/line is orthogonal to this axis

Since all dimension are orthogonal to each other, 
we draw a another line known as 2nd Principal Component

Then we again projects the points on the 2nd Principal Component

Now if we start considering PC1 and PC2
Now there is no loss, only change in the coordinate system
Earlier data was also 2D and now also its 2D

We have just rotated the lines for better view as coordinate system

So now there is no Dimension Reduction, since now also we have 2D
Dimension reduction will happen only when we reduce our data in PC1

So PCA is a powerful technique 

According to Mathematics
Eigen Vector is the 1st Principal Line and 2nd Prinipal Line
Eigen Values is the points that are shown in blue

"""



# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# Importing the dataset
dataset = pd.read_csv('data/Wine.csv')


# Explain the features
# label is the customer categorories ( 1,2,3) who will like the wine
features = dataset.iloc[:, 0:13].values
labels = dataset.iloc[:, 13].values

# If new wine is launched, which category of customer would like it
# We can visualise only 2D dataset, but we have 13D dataset.
# which would be difficult to visualize and draw the decission boundary
# Solution to it is convertion from 13D to 2D data


# df_features = pd.DataFrame(features)
# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
train_test_split(features, labels, test_size = 0.2, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()

features_train = sc.fit_transform(features_train)
features_test = sc.transform(features_test)


"""
13D Data to 2D dataset 
Convoluton of 13D data, if has not removed any features, 
but have created two new features PC1 and PC2 which has 
some weightage of all the 13 features
"""

# Applying PCA
from sklearn.decomposition import PCA
pca = PCA(n_components = 2)

features_train = pca.fit_transform(features_train)
features_test = pca.transform(features_test)

# How much is the loss and how much we are able to retain the information
explained_variance = pca.explained_variance_ratio_
print(explained_variance)
# first paramater (PC1) is holding 36% of the 13D data
# second parameter (PC2) is holding 19% of the 13D data

# Fitting Logistic Regression to the Training set
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state = 0)
classifier.fit(features_train, labels_train)

# Predicting the Test set results
labels_pred = classifier.predict(features_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(labels_test, labels_pred)
print(cm)
# 3 Segmentation of the Customers 
# With 56% reduced data, we are still able to get good score of prediction 


# After reduction of data, still there is good prediction 
# We should have compared this with 13D data
print( (cm[0][0] + cm[1][1]) / (cm[0][0] + cm[1][1] + cm[0][1] + cm[1][0]))



# Visualising the Test set results
x_min, x_max = features_train[:, 0].min() - 1, features_train[:, 0].max() + 1
y_min, y_max = features_train[:, 1].min() - 1, features_train[:, 1].max() + 1

xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01),
                     np.arange(y_min, y_max, 0.01))
# Obtain labels for each point in mesh using the model.
# ravel() is equivalent to flatten method.
# data dimension must match training data dimension, hence using ravel
Z = classifier.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

# Plot the points, we have three labels (1,2,3)
plt.plot(features_test[labels_test == 1, 0], features_test[labels_test == 1, 1], 'ro', label='Class 1')
plt.plot(features_test[labels_test == 2, 0], features_test[labels_test == 2, 1], 'go', label='Class 2')
plt.plot(features_test[labels_test == 3, 0], features_test[labels_test == 3, 1], 'bo', label='Class 3')

#plot the decision boundary
plt.contourf(xx, yy, Z, alpha=.5)

plt.show()
print(cm)


# How will i come to know, that in PC1 and PC2, which features from 13D
# has its percentage 

# Dump components relations with features:
df_features = pd.DataFrame(features)
df_pca =  pd.DataFrame(pca.components_,columns=df_features.columns,index = ['PC-1','PC-2'])
print(df_pca)








"""
Q1. Import Crime.csv File.
    Perform dimension reduction and group the cities using k-means based on 
    Rape, Murder and assault predictors.

"""

"""

Q2.The iris data set consists of 50 samples from each of three species of Iris 
flower (Iris setosa, Iris virginica and Iris versicolor).

Four features were measured from each sample: the length and the width 
of the sepals and petals, in centimetres (iris.data).
Import the iris dataset already in sklearn module using the following command


from sklearn.datasets import load_iris
iris = load_iris()
iris=iris.data

Reduce dimension from 4-d to 2-d and perform clustering to distinguish the 
3 species.
"""

"""
Q3 Data: "data.csv"

This data is provided by The Metropolitan Museum of Art Open Access
1. Visualize the various countries from where the artworks are coming.
2. Visualize the top 2 classification for the artworks
3. Visualize the artist interested in the artworks
4. Visualize the top 2 culture for the artworks
"""


# Skip from here onwards
"""
https://www.analyticsvidhya.com/blog/2016/03/practical-guide-principal-component-analysis-python/
http://sebastianraschka.com/Articles/2014_pca_step_by_step.html
https://plot.ly/ipython-notebooks/principal-component-analysis/
http://blog.districtdatalabs.com/principal-component-analysis-with-python
http://support.minitab.com/en-us/minitab/17/topic-library/modeling-statistics/multivariate/principal-components-and-factor-analysis/what-is-pca/
https://www.analyticsvidhya.com/blog/2015/07/dimension-reduction-methods/
https://en.wikipedia.org/wiki/Dimensionality_reduction
http://www.lauradhamilton.com/introduction-to-principal-component-analysis-pca
http://setosa.io/ev/principal-component-analysis/

http://setosa.io/ev/principal-component-analysis/
http://www.lauradhamilton.com/introduction-to-principal-component-analysis-pca
https://stats.stackexchange.com/questions/229092/how-to-reverse-pca-and-reconstruct-original-variables-from-several-principal-com
http://jotterbach.github.io/2016/03/24/Principal_Component_Analysis/
https://stackoverflow.com/questions/22984335/recovering-features-names-of-explained-variance-ratio-in-pca-with-sklearn




//Challenges with high dimensional data

Datasets that have a large number features pose a unique challenge for machine
 learning analysis. We know that machine learning models can be used to 
 classify or cluster data in order to predict future events. 
 However, high-dimensional datasets add complexity to certain
 machine learning models (i.e. linear models) and, as a result, 
 models that train on datasets with a large number features are
 more prone to producing error due to bias.

Principal Component Analysis (PCA) is a dimensionality reduction technique 
used to transform high-dimensional datasets into a dataset with fewer variables,
 where the set of resulting variables explains the maximum variance within 
 the dataset. PCA is used prior to unsupervised and supervised machine learning
 steps to reduce the number of features used in the analysis, thereby 
 reducing the likelihood of error.
"""
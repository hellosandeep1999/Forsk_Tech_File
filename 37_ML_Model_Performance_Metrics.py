"""
Todays focus is on the Performance of the Algorithm
Whether it is GOOD or BAD, if it is BAD, what measures we have to take
"""

# How to measure the performance of a Linear Regression Algo
# We use to draw a best fit line, whose residual was minimum

#Importing Libraries
import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  

#imports the CSV dataset using pandas
dataset = pd.read_csv('student_scores.csv')  


#explore the dataset
print (dataset.shape)
print (dataset.ndim)
print (dataset.head())
print (dataset.describe())

# Finding missing data
dataset.isnull().any(axis=0)

# Check for range of features and label
plt.boxplot(dataset.values)


# let's plot our data points on 2-D graph to eyeball our dataset 
# and see if we can manually find any relationship between the data. 
# It seems to be a POSITIVE Corelationship between Hours and Scores
# Since the Hours are increasing there is a positive increase in Scores

dataset.plot(x='Hours', y='Scores', style='o')  
plt.title('Hours vs Percentage')  
plt.xlabel('Hours Studied')  
plt.ylabel('Percentage Score')  
plt.show()

#prepare the data to train the model
features = dataset.iloc[:, :-1].values  
labels = dataset.iloc[:, 1].values 


from sklearn.model_selection import train_test_split  
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.2, random_state=0)  

#train the algo
from sklearn.linear_model import LinearRegression  
regressor = LinearRegression()  
regressor.fit(features_train, labels_train)  

#To see the value of the intercept and slop calculated by the linear regression algorithm for our dataset, execute the following code.
print(regressor.intercept_)  
print (regressor.coef_)

"""
Defination of Coefficient
This means that for every one unit of change in hours studied ( x axis), 
the change in the score(y axis)  is about 9.91%. 
"""

#making predictions
#To make pre-dictions on the test data, execute the following script:

labels_pred = regressor.predict(features_test) 

#To compare the actual output values for features_test with the predicted values, execute the following script 
df = pd.DataFrame({'Actual': labels_test, 'Predicted': labels_pred})  
print ( df )


#Visualize the best fit line
import matplotlib.pyplot as plt

# Visualising the Test set results
plt.scatter(features_test, labels_test, color = 'red')
plt.plot(features_train, regressor.predict(features_train), color = 'blue')
plt.title('Study Hours and Exam Score')
plt.xlabel('Study Hours')
plt.ylabel('Marks')
plt.show()

"""
Evaluate the Algorithm

We want a metric or paramter now, which tells us how GOOD or BAd our model is

The best fit line should minimise the residual for us

We use to minimise it with the following formula, that is known as
MSE= Mean Square Error  = 
cost function = (d1)**2 + (d2)**2 + (d3)**2 .... + (dn)**2
                ------------------------------------------
                                    n

If we take a square root of MSE then it is known as
RMSE = Root Mean Square Error = 
SQRT ( MSE)

Sometimes we take the absolute values, then

Mean Absolute Error ( MAE ) 
              = |d1| + |d2| +  |d3|  +  ... + |dn|
                -----------------------------------
                               n

If any point is far from the best fit line
then its MAE would not be big, with comparision to MSE or RMSE

Usually we focus on the RMSE

"""


# Evaluate the Algorithm 
from sklearn import metrics  
print('Mean Absolute Error:', 
      metrics.mean_absolute_error(labels_test, labels_pred))  
print('Mean Squared Error:', 
      metrics.mean_squared_error(labels_test, labels_pred))  
print('Root Mean Squared Error:', 
      np.sqrt(metrics.mean_squared_error(labels_test, labels_pred))) 


"""
We have taken our all the 3 values of MAE, MSE, RMSE
But how to compare these values, 
since we dont have a benchmark values for comparision 
We take out the mean values of the label and then do a comparision
i.e 5.14 ( 10% of the 51.48)



 
"""
print (np.mean(dataset.values[:,1])) # 51.48

"""
RMSE < np.mean (labels ) * 10%

You can see that the value of RMSE is 4.64, 
This means that our algorithm did a decent job, since it is less then 5.14
If the RMSE comes more than the 10% of mean of label, then the model is BAD
"""

"""
There is another way we use known as R Squared Score
Max value is 1, that mean your all predictions are same as actual
That means the residual is zero, which is an ideal condition 
We have calcuated the score on test and train data
"""

#Model accuracy ( you can swap features and labels passing)
print (regressor.score(features_test, labels_test))
print (regressor.score(features_train, labels_train))

print('R Squared Error:', 
      metrics.r2_score(labels_test, labels_pred) )



"""
Now lets talk about two terms - overfitting and underfitting the data

If the training score is POOR and test score is POOR then its underfitting

If the training score is GOOD and test score is POOR then its overfitting


"""



"""
# Underfitting = no padai

It means that the model does not fit the training data and therefore misses 
the trends in the data
this is usually the result of a very simple model (not enough predictors/independent variables).
"""
 


"""
# Overfitting = ratoo tota but concept is weak

This model will be very accurate on the training data but will probably be very 
not accurate on untrained or new data

This usually happens when the model is too complex (i.e. too many features/variables 
compared to the number of observations). 

It is because this model is not generalized 
Basically, when this happens, the model learns or describes the “noise” in the 
training data instead of the actual relationships between variables in the data.

"""


"""
Solution to Underfitting
    Increase the training data size
    Increase the Model Complexity from simpler to complex
    

Solution to Overfitting
    Simplify the model, not so complex
    Apply Regularisation to handle overfitting

    There are two types of regularization as follows:

    L1 Regularization or Lasso Regularization
    L2 Regularization or Ridge Regularization
    Elastic Net is hybrid of both L1 and L2
    
 
"""


"""
Metrics for Classification Problems ( Different from Regression Problem )
"""


# Logistic Regression ( Classification)


# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('data/Social_Network_Ads.csv')
features = dataset.iloc[:, :-1].values
labels = dataset.iloc[:, 2].values

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size = 0.25, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
features_train = sc.fit_transform(features_train)
features_test = sc.transform(features_test)

# Fitting Logistic Regression to the Training set
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression()
classifier.fit(features_train, labels_train)

# Predicting the Test set results
labels_pred = classifier.predict(features_test)


# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(labels_test, labels_pred)
print(cm)


"""
Actual Values
|
|
\/
    |   NO  |  YES  | Predicted values--->
  +++++++++++++++++++++
  NO|   TN  |  FP   |
  +++++++++++++++++++++
 YES|   FN  |  TP   |
  +++++++++++++++++++++
    |       |       | 
    
    
    --              --
   | TN           FP  |
   |                  |
   | FN           TP  |
    --              --

"""



"""
Model Score
    1. Accuracy Score / Confusion Matrix
    2. Precission Score
    3. Recall 
    4. F1 Score
"""


"""
Define Accuracy Score / Confusion Matrix
            TP + TN 
 CM =    ------------------
          TP + TN + FP + FN 
"""
# Accuracy Score / Confusion Matrix
from sklearn.metrics import accuracy_score  
print (accuracy_score(labels_test, labels_pred))  
# can be calcuated from cm as well 
# 65 + 24 / ( 65 + 24 + 3 + 8) = .89


"""
Define precision Score

given that the classifier predicted a sample as positive, 
what’s the probability of the sample being indeed positive?

So, Precision should be HIGH for a model


pos_label = 0 ( 0 is positive according to us)
pos_label = 1 ( 1 is positive according to us)

                                TP 
Precission Score = ----------
                              TP + FP

https://developers.google.com/machine-learning/crash-course/classification/precision-and-recall
"""


from sklearn.metrics import precision_score
 
# Take turns considering the positive class either 0 or 1
print (precision_score(labels_test, labels_pred, pos_label=0)  )
print (precision_score(labels_test, labels_pred, pos_label=1)  )




"""
Define  Recall Score/Sensitivity
given a positive sample, what is the probability that our system will properly 
identify it as positive?

                     TP 
         Recall = ----------
                   TP + FN
https://developers.google.com/machine-learning/crash-course/classification/precision-and-recall
"""
from sklearn.metrics import recall_score

# Take turns considering the positive class either 0 or 1
print (recall_score(labels_test, labels_pred, pos_label=0)  )
print (recall_score(labels_test, labels_pred, pos_label=1)  )


# Recall and Precission should come GOOD for a model
# So we need to have a new score which uses both


"""
Define  f1 Score

A measure that combines the precision and recall metrics is called F1-score. 
This score is, in fact, the harmonic mean of the precision and the recall. 
Here’s the formula for it:
2 / (1 / Precision + 1 / Recall)


F1 Score  = Harmonic mean of Precission and Recall 

                  2
F1 Score =--------------------
             1          1 
            ----   +   ----
             PS         RS 
https://en.wikipedia.org/wiki/F1_score
 
"""
from sklearn.metrics import f1_score

# Take turns considering the positive class either 0 or 1
print (f1_score(labels_test, labels_pred, pos_label=0)  )
print (f1_score(labels_test, labels_pred, pos_label=1)  )

"""
A convenient shortcut in scikit-learn for obtaining a readable digest of all 
the metrics is metrics.classification_report
"""
from sklearn.metrics import classification_report

print (classification_report(labels_test, labels_pred, target_names=['NO', 'YES']))

# The support is the number of samples of the true response that lie 
# in that class.


"""
Code Challenges
Code Challenge 01: (Prostate Dataset) Prostate_Cancer.csv

This is the Prostate Cancer dataset. Perform the train test split before you apply the model.




Code Challenge 02:(pros.dat.csv)

Load the dataset from given link:
pd.read_csv("http://www.stat.cmu.edu/~ryantibs/statcomp/data/pros.dat", delimiter =' ')

(a) Can we predict lpsa from the other variables?
      (1) Train the unregularized model (linear regressor) and calculate the mean squared error.
      (2) Apply a regularized model now - Ridge regression and lasso as well and check the mean squared error.

(b) Can we predict whether lpsa is high or low, from other variables?
"""


# Skip from here onwards









#http://setosa.io/ev/ordinary-least-squares-regression/
# https://medium.com/@ml.at.berkeley/machine-learning-crash-course-part-1-9377322b3042

#Show the animation using learning rate, cost functions and best fit line
#https://towardsdatascience.com/epoch-vs-iterations-vs-batch-size-4dfb9c7ce9c9

# best reference available is 
# https://medium.com/towards-data-science/train-test-split-and-cross-validation-in-python-80b61beca4b6


#Show the animation using learning rate, cost functions and best fit line
#https://towardsdatascience.com/epoch-vs-iterations-vs-batch-size-4dfb9c7ce9c9


"""
Regression Notes
https://blog.minitab.com/blog/adventures-in-statistics-2/regression-analysis-how-do-i-interpret-r-squared-and-assess-the-goodness-of-fit
https://blog.minitab.com/blog/how-to-choose-the-best-regression-model
"""

"""
https://www.listendata.com/2017/03/partial-correlation.html
"""
"""
#Industry applications of the Linear Regression
#The two primary uses for regression in business are forecasting and optimization. In addition to helping managers predict such things as future demand for their products, regression analysis helps fine-tune manufacturing and delivery processes.
https://smallbusiness.chron.com/application-regression-analysis-business-77200.html
"""

"""
https://medium.com/usf-msds/choosing-the-right-metric-for-machine-learning-models-part-1-a99d7d7414e4
https://medium.com/usf-msds/choosing-the-right-metric-for-evaluating-machine-learning-models-part-2-86d5649a5428
https://blog.exsilio.com/all/accuracy-precision-recall-f1-score-interpretation-of-performance-measures/
"""

"""
https://www.dataquest.io/blog/understanding-regression-error-metrics/
"""
"""
https://www.myaccountingcourse.com/financial-ratios/r-squared
"""

"""
# how to calculate the MAE
from sklearn import linear_model
lm = linear_model.LinearRegression()
lm.fit(X, sales)

mae_sum = 0
for sale, x in zip(sales, X):
    prediction = lm.predict(x)
    mae_sum += abs(sale - prediction)
mae = mae_sum / len(sales)

print(mae)


"""

"""
#Calculatiing the MSE

mse_sum = 0
for sale, x in zip(sales, X):
    prediction = lm.predict(x)
    mse_sum += (sale - prediction)**2
mse = mse_sum / len(sales)

print(mse)

"""

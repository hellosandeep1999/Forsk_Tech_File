"""
DbSCAN ( Density Based and not centroid based )
"""
#Density-based spatial clustering of applications with noise 


"""
Open the Webpage
https://www.naftaliharris.com/blog/visualizing-k-means-clustering/
How to pick the initial centroids?  == Randomly
What kind of data would you like?   == Smiley Face
Take clusters as 3 
Follow all the steps to update the centroid

Data in not uniformly distributed, there should be 4 clusters, 
but kMeans will give different clusters

kMeans is good when the data is uniformly distributed

DBSCAN is good for non uniformly distributed data. 
It does not uses centroid concept, but uses density based concept



https://www.naftaliharris.com/blog/visualizing-dbscan-clustering/
Explain the animation for minimum_samples and epsilon, 
There should be minimum samples in the circle drawn with epsilon radius
Apply recursion for the points within the circle and the proces goes on...
Noise are those points which are not part of any cluster, it gives -1


Now the actual explanation of the algorithm !!
https://www.naftaliharris.com/blog/visualizing-dbscan-clustering/
Uniform points

DbSCAN is a recursive type of algorithm
[ within radius = 1(epsilion) and has minpoints = 4 ]
It has shown a lot of rings, but only those rings are RED when is satisfying
the condition of radius = 1 and minpoints = 4

It start randomly from any point
Then it decides at what minimum points should i decide its a cluster now
Lets assume we have set the minimum points as 4
Within certain area if there are 4 points, then there will be a cluster

For the distance we use another parameter epsilion radius
Within the radius of 1 otherwise it will not be cluster
It is showing in RED only those rings which are stasifying our both conditoins

For each point in the RED ... 
it tries to calcuate the next cluster within our 2 conditions 

This recursion goes on
"""

import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Generate sample data
centers = [[1, 1], [-1, -1], [1, -1]]  # 3 ---> 0 1 2 

# make_blobs generates random points from any point from a list
# by default it gives 2 features, 
features, labels = make_blobs(n_samples=750, centers=centers, cluster_std=0.4,
                            random_state=0)

print(features)

print(labels)

#Scatter all these data points on the matplotlib
plt.scatter(features[:,0], features[:,1])
plt.show()



features = StandardScaler().fit_transform(features)

#Scatter all these data points on the matplotlib
plt.scatter(features[:,0], features[:,1])
plt.show()


# Compute DBSCAN
db = DBSCAN(eps=0.3, min_samples=10).fit(features)
#core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
#core_samples_mask[db.core_sample_indices_] = True

labels_pred = db.labels_ # belongs to which cluster id

print(labels_pred)



# Plot result
import matplotlib.pyplot as plt


plt.scatter(features[labels_pred == 0,0], features[labels_pred == 0,1],c='r', marker='+' )
plt.scatter(features[labels_pred == 1,0], features[labels_pred == 1,1],c='g', marker='o' )
plt.scatter(features[labels_pred == 2,0], features[labels_pred == 2,1],c='b', marker='s' )
plt.scatter(features[labels_pred == -1,0],features[labels_pred == -1,1],c='y', marker='*' )


#measure the performance of the dbscan

"""
# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)
print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(labels_true, labels))
print("Adjusted Mutual Information: %0.3f"
      % metrics.adjusted_mutual_info_score(labels_true, labels))
print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(X, labels))

"""

# Remmbering how to read data from datasets

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset boston dataset 
from sklearn.datasets import load_iris
iris = load_iris()

dataset = iris.data

##Noise 


# Code Challenges
"""
Q1. (Create a program that fulfills the following specification.)
deliveryfleet.csv


Import deliveryfleet.csv file

Here we need Two driver features: mean distance driven per day (Distance_feature) 
and the mean percentage of time a driver was >5 mph over the speed limit (speeding_feature).

Perform K-means clustering to distinguish urban drivers and rural drivers.
Perform K-means clustering again to further distinguish speeding drivers 
from those who follow speed limits, in addition to the rural vs. urban division.
Label accordingly for the 4 groups.




Q2. (Create a program that fulfills the following specification.)
tshirts.csv


T-Shirt Factory:

You own a clothing factory. You know how to make a T-shirt given the height 
and weight of a customer.

You want to standardize the production on three sizes: small, medium, and large. 
How would you figure out the actual size of these 3 types of shirt to better 
fit your customers?

Import the tshirts.csv file and perform Clustering on it to make sense out of 
the data as stated above.



Q.3. Code Challenge - 
 This is a pre-crawled dataset, taken as subset of a bigger dataset 
 (more than 4.7 million job listings) that was created by extracting data 
 from Monster.com, a leading job board.
 
 monster_com-job_sample.csv
 
 Remove location from Organization column?
 Remove organization from Location column?
 
 In Location column, instead of city name, zip code is given, deal with it?
 
 Seperate the salary column on hourly and yearly basis and after modification
 salary should not be in range form , handle the ranges with their average
 
 Which organization has highest, lowest, and average salary?
 
 which Sector has how many jobs?
 Which organization has how many jobs
 Which Location has how many jobs?
"""

# Skip from here onwards




# Hands On with Solution for IRIS Data

"""
# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
from sklearn.datasets import load_iris
iris = load_iris()

from sklearn.cluster import DBSCAN
dbscan = DBSCAN()

print (dbscan)




#DBSCAN(eps=0.5, metric='euclidean', min_samples=5,random_state=111)

dbscan.fit(iris.data)

dbscan.labels_

# Visualising the clusters 
# as data is in 3d space, we need to apply PCA for 2d ploting
from sklearn.decomposition import PCA
pca = PCA(n_components=2).fit(iris.data)
pca_2d = pca.transform(iris.data)


#alternative way, fit_transform
#pa = PCA(n_components = 2)
#pca_2d =  pca.fit_transform(iris.data)

for i in range(0, pca_2d.shape[0]):
    if dbscan.labels_[i] == 0:
        c1 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='r', marker='+')
    elif dbscan.labels_[i] == 1:
        c2 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='g',
                        marker='o')
    elif dbscan.labels_[i] == -1:
        c3 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='b',
                        marker='*')
    
    
plt.legend([c1, c2, c3], ['Cluster 1', 'Cluster 2','Noise'])
plt.title('DBSCAN finds 2 clusters and noise')
plt.savefig("dbscan.jpg")
plt.show()


pca.components_

for i in range(0, pca_2d.shape[0]):
    if iris.target[i] == 0:
        c1 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='r', marker='+')
    elif iris.target[i] == 1:
        c2 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='g',
                        marker='o')
    elif iris.target[i] == 2:
        c3 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='b',
                        marker='*')
    
plt.legend([c1, c2, c3], ['Cluster 1', 'Cluster 2','Noise'])
plt.title('DBSCAN finds 2 clusters and noise')

plt.savefig("classifier.jpg")
plt.show()


# Using the elbow method to find the optimal number of clusters
from sklearn.cluster import KMeans
# Fitting K-Means to the dataset
kmeans = KMeans(n_clusters = 3, init = 'k-means++', random_state = 0)
y_kmeans = kmeans.fit_predict(iris.data)
for i in range(0, pca_2d.shape[0]):
    if y_kmeans[i] == 0:
        c1 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='r', marker='+')
    elif y_kmeans[i] == 1:
        c2 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='g',
                        marker='o')
    elif y_kmeans[i] == 2:
        c3 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='b',
                        marker='*')
    
plt.legend([c1, c2, c3], ['Cluster 1', 'Cluster 2','Noise'])
plt.title('DBSCAN finds 2 clusters and noise')
plt.savefig("kmeans.jpg")

plt.show()

"""



#http://www.sthda.com/english/wiki/print.php?id=246
"""
//pickle files
It is used for serializing and de-serializing a Python object structure. 
Any object in python can be pickled so that it can be saved on disk. 
What pickle does is that it “serialises” the object first before writing it to file. 
Pickling is a way to convert a python object (list, dict, etc.) into a character stream. 
The idea is that this character stream contains all the information necessary to 
reconstruct the object in another python script.
Methods to save the scikit learn models

The modern ways to save the trained scikit learn models is using the packages like

Pickle (Python Object Serialization Library)
Joblib (One of the scikit-learn Method)

What is Pickle?

Pickle is one of the Python standard libraries. Which is so powerful and the 
best choice to perform the task like

Serialization
Marshalling
The above two functionalities are popularly known as  Pickling and Unpickling

Pickling
Pickling is the process converting any Python object into a stream of bytes by 
following the hierarchy of the object we are trying to convert.

Unpickling
Unpickling is the process of converting the pickled (stream of bytes) back into 
to the original Python object by following the object hierarchy

Ref: http://dataaspirant.com/2017/02/13/save-scikit-learn-models-with-python-pickle/
http://scikit-learn.org/stable/modules/model_persistence.html
--------------------------------------------------
//Dataset Sources
1. https://www.kaggle.com/datasets
2. http://archive.ics.uci.edu/ml/index.php
3. 

---------------------------
Supervised Machine Learning

The majority of practical machine learning uses supervised learning.

Supervised learning is where you have input variables (x) and an output variable (Y) 
and you use an algorithm to learn the mapping function from the input to the output.

Y = f(X)

The goal is to approximate the mapping function so well that when you have new 
input data (x) that you can predict the output variables (Y) for that data.
------------------------------------------------------------------------------------------

//Unsupervised learning

Unsupervised learning is where you only have input data (X) and no corresponding output variables.

The goal for unsupervised learning is to model the underlying structure or
 distribution in the data in order to learn more about the data.

These are called unsupervised learning because unlike supervised learning above 
there is no correct answers and there is no teacher. 
Algorithms are left to their own devises to discover and present the interesting structure in the data.

Unsupervised learning problems can be further grouped into clustering and association problems.

Clustering: A clustering problem is where you want to discover the inherent 
groupings in the data, such as grouping customers by purchasing behavior.

Association:  An association rule learning problem is where you want to discover 
rules that describe large portions of your data, such as people that buy X also tend to buy Y.

Some popular examples of unsupervised learning algorithms are:

k-means for clustering problems.
Apriori algorithm for association rule learning problems.
----------------------------------------------------
Semi-Supervised Machine Learning

Problems where you have a large amount of input data (X) and only some of the data is labeled (Y) 
are called semi-supervised learning problems.

These problems sit in between both supervised and unsupervised learning.

A good example is a photo archive where only some of the images are labeled, 
(e.g. dog, cat, person) and the majority are unlabeled.

--------------------------------------------------------------------------------------
//Clustering

//k-means alogo
//Animation - http://shabal.in/visuals/kmeans/1.html
//https://www.naftaliharris.com/blog/visualizing-k-means-clustering/
[show the demo using above link]
//k-means details
The algorithm then proceeds in two alternating parts: 
In the Reassign Points step, we assign every point in the data to the cluster 
whose centroid is nearest to it. In the Update Centroids step, we recalculate each 
centroid's location as the mean (center) of all the points assigned to its cluster. 
We then iterate these steps until the centroids stop moving, or equivalently until 
the points stop switching clusters.
//random initialization trap - selection of initial centroids can change the final outcome

// Selecting the right number of clusters - how many number of clusters would be better - methods used is elbow method

//

//k-means++ is solution for this trap
// which employes elbow method which calculates wcss
//wcss - within cluster sum of squares
//aim is to figure out optimal number of clusters where elbow is created.

//There are other methods for finding the right number of clusters,
//http://www.sthda.com/english/articles/29-cluster-validation-essentials/96-determining-the-optimal-number-of-clusters-3-must-know-methods/

Compute clustering algorithm (e.g., k-means clustering) for different values of k. For instance, by varying k from 1 to 10 clusters.

For each k, calculate the total within-cluster sum of square (wss).

Plot the curve of wss according to the number of clusters k.

The location of a bend (knee) in the plot is generally considered 
as an indicator of the appropriate number of clusters.




https://towardsdatascience.com/unsupervised-learning-with-python-173c51dc7f03






Very important about noise points
You can see that DBSCAN produced three groups. 
Note, however, that the figure closely resembles a two-cluster 
solution: It shows only 17 instances of label – 1. 
That’s because it’s a two-cluster solution; the third group (–1)
 is noise (outliers). You can increase the distance parameter 
 (eps) from the default setting of 0.5 to 0.9, and it will 
 become a two-cluster solution with no noise.

The distance parameter is the maximum distance an 
observation is to the nearest cluster. The greater the value 
for the distance parameter, the fewer clusters are found 
because clusters eventually merge into other clusters. The –1 
labels are scattered around Cluster 1 and Cluster 2 in a few 
locations:

Near the edges of Cluster 2 (Versicolor and Virginica classes)

Near the center of Cluster 2 (Versicolor and Virginica classes)





DBSCAN Details

https://towardsdatascience.com/how-dbscan-works-and-why-should-i-use-it-443b4a191c80

https://www.dummies.com/programming/big-data/data-science/how-to-create-an-unsupervised-learning-model-with-dbscan/


Animation
https://www.naftaliharris.com/blog/visualizing-dbscan-clustering/



eps: if the eps value chosen is too small, 
a large part of the data will not be clustered. 
It will be considered outliers because don’t 
satisfy the number of points to create a dense 
region. On the other hand, if the value that was 
chosen is too high, clusters will merge and the 
majority of objects will be in the same cluster.
The eps should be chosen based on the distance of 
the dataset (we can use a k-distance graph to find 
it), but in general small eps values are preferable.

minPoints: As a general rule, a minimum 
minPoints can be derived from a number of 
dimensions (D) in the data set, as minPoints ≥ D + 1.
Larger values are usually better for data sets 
with noise and will form more significant clusters.
The minimum value for the minPoints must be 3,
but the larger the data set, the larger the 
minPoints value that should be chosen.

"""





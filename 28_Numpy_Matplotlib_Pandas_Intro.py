# Panel Data Set
'''Import Python Libraries'''
import pandas as pd


'''Create a Series from ndarray'''


s = pd.Series(['a','b','c','d'])
print (type(s))
print (s)

# We did not pass any index, so by default, 
# it assigned the indexes ranging from 0 to len(data)-1, i.e., 0 to 3.


'''Customised Index value'''

s = pd.Series(['a','b','c','d'],index=[100,101,102,103])
print (s)


import pandas as pd
#Read csv file
df = pd.read_csv("Salaries.csv")

# Not a good technique to print the Data Frame
print (df)

df.info()

#number of dimensions
df.ndim   


#return a tuple representing the dimensionality
df.shape 


#number of elements
df.size 


#List first 5 records
df.head(10)


#Try to read the first 10, 20, 50 records;
#Can you guess how to view the last few records;


df.tail(5)


# Gives the row Indexes
df.index


#list the column names / column Indexes
df.columns 


#Check types for all the columns
df.dtypes


#numpyrepresentation of the data
df.values 



"""
Data Frames: method loc

If we need to select a range of rows, using their labels/index 
we can use method loc
"""

df.loc[:1]

df.loc[10:20,['rank','sex']]


"""
Data Frames: method iloc

If we need to select a range of rows and/or columns, 
using their positions we can use method iloc
"""
df.iloc[:2]

df.iloc[ 10:21 , [0,4] ]



#Select column rank and salary:
df[['rank','salary']]


# Find unique values in a Series / Column
df['rank'].unique()
df['discipline'].unique()
df['sex'].unique()
list1 = df['sex'].unique().tolist()




# intuition about a Rank Series
df['rank']
df['rank'].value_counts()

# to show in Percentage 
df['rank'].value_counts(normalize = True)


# To know the count of male and female candidates
df['sex'] 
df['sex'].value_counts()
df['sex'].value_counts(normalize = True)

# count missing values 
# ( It also counts the NaN Values in the Series/Column)
df['sex'].value_counts(dropna=False)

df['phd'].value_counts()
df['phd'].value_counts(dropna=False)

df['salary'].value_counts()
df['salary'].value_counts(dropna=False)


#calculate the basic statstics on the salary column
df['salary'].mean()
df['salary'].std()
df['salary'].describe()


#Find how many values in the salary column which are non NaN (use count method);
df['salary'].count()
df['phd'].count()


# Boolean Indexing
# Find those rows which has null values in salary/phd column
df['salary'].isnull()
df[df['salary'].isnull()]

df['phd'].isnull()
df[df['phd'].isnull()]
  
"""
Data Frames groupby method

Using "group by" method we can:
Split the data into groups based on some criteria
Calculate statistics (or apply a function) to each group
"""
#Group data using rank
df_rank= df.groupby(['rank'])

df_rank.size()
df_rank.count()
df_rank.groups
# Groups returns a dictionary object
df_rank.groups['AssocProf']
df_rank.groups['AssocProf'][0]

 
#group data using rank followed  by discipline and sex
df_rank=df.groupby(['rank', 'discipline','sex'])
df_rank.groups
df_rank.count()
 
#Calculate mean value for each numeric column per each group
df_rank.mean()


#Calculate mean salary for each type of professor rank:
df.groupby('rank')[['salary','phd']].min()
df.groupby('rank')[['salary','phd']].max()
df.groupby('rank')[['salary','phd']].mean()
        


"""
Data Frame: filtering

To subset the data we can apply Boolean indexing. 
This indexing is commonly known as a filter. 
For example if we want to subset the rows in which the salary
 value is greater than $120K:

"""

# Boolean Indexing in Pandas
# select only those professors who has salary more than 120000
df['salary'] > 120000
df_sub= df[(df['salary'] > 120000) ]
df_sub

#or

df.loc[df['salary'] > 120000]


# to display only the selected series/column
df.loc[df['salary'] > 120000,'salary']



#filter using multiple columns

df_sub= df[(df['salary'] > 120000) & \
           (df['phd'] > 10) & \
           (df['sex'] == 'Female' )
           ]
df_sub
# Or

df.loc[(df['salary'] > 120000) & \
           (df['phd'] > 10) & \
           (df['sex'] == 'Female' )]


"""
Missing Values


"""

df.info()

df[df['phd'].isnull()]

df[df['salary'].isnull()]


'''How to fix missing values'''

new_df2 = df.fillna(0)
new_df2.count()


# Fill All columns with missing values, with mean of that column
df = df.fillna(round(df.mean(),0))
df

# fill all the records with missing values, with mean of that column
df['phd'] = df['phd'].fillna(df['phd'].mean())

# fill all the records with missing values, with mean of that column
df['salary'] = df['salary'].fillna(df['salary'].median())


# How to drop columns
df.drop('discipline',axis=1, inplace=True)

df1 = df.dropna()
df1.count()


# Remove the $ Sign from the Salary Column and then converted the string field into numeric
df['salary'] = df['salary'].str.replace('INR','').str.replace(',','')
df['salary'] = pd.to_numeric(df['salary'])


# Creating a new Column based on some other columns values 
# Male == 0 and Female == 1
df["bool_sex"] = df["sex"].map(lambda x: 0 if x == 'Male' else 1 )
df


#Value Conversion using apply function 
# Male == 0 and Female == 1

df = pd.read_csv("data/Salaries.csv")

def gender_code(gender_string):  
    if (gender_string == "Male") :
        return 0
    elif (gender_string == "Female") :
        return 1   
#    if isinstance(gender_string, float) and math.isnan(gender_string):

df["sex"].value_counts(dropna=False)

df["sex"] = df["sex"].apply(gender_code)

df["sex"].value_counts(dropna=False)


# Create a new column called df.Child where the value is yes
# if df.age is greater than 50 and no if not
df['child'] = np.where(df['age']<18, 'yes', 'no')


# Iterating over rows 
for i, row in df.iterrows():
    print("Index {}".format(i))
    print("Row \n{}".format(row))

"""
Analysis of Salaries Data ( Hand On Activity )

1. Which Male and Female Professor has the highest and the lowest salaries
2. Which Professor takes the highest and lowest salaries.
3. Missing Salaries - should be mean of the matching salaries of those 
   whose service is the same
4. Missing phd - should be mean of the matching service 
5. How many are Male Staff and how many are Female Staff. 
   Show both in numbers and Graphically using Pie Chart.  
   Show both numbers and in percentage
6. How many are Prof, AssocProf and AsstProf. 
   Show both in numbers adn Graphically using a Pie Chart
7. Who are the senior and junior most employees in the organization.
8. Draw a histogram of the salaries divided into bin starting 
   from 50K and increment of 15K
"""




# Numerical Python 
'''Introduction to NumPy'''

a = [0,1,2,3,4,5,6,7,8]
print (type(a))
print (a)  
# it always prints the values with comma seperated , thats list


# Convert your list data to NumPy arrays
import numpy as np

x = np.array( a ) 
print (type(x))

print (x)
# it always prints the values WITHOUT comma seperated , thats ndarray


"""
Explain the ndarray data Structure Image
NumPy_NDArray_Data_Structure.png
"""

# to print the data type of the elements of array 
print (x.dtype)


# to print the dimension of the array 
print (x.ndim)

# to print the shape of the array 
# returns a tuple listing the length of the array along each dimension
# For a 1D array, the shape would be (n,) 
# where n is the number of elements in your array.
print (x.shape)


# Shows bytes per element 
print (x.itemsize)

# reports the entire number of elements in an array
print(x.size)

# returns the number of bytes used by the data portion of the array
print (x.nbytes)

print (x.strides)


# Array Indexing will always return the data type object 
print (x[0])
print (x[2])
print (x[-1])




"""
Reshaping is changing the arrangement of items so that shape of the array changes
Flattening, however, will convert a multi-dimensional array to a flat 1d array. And not any other shape.
"""

# Reshaping to 2 Dimensional Array - 3 Rows and 3 Columns
x = x.reshape(3,3)
print (x)


print (x.ndim)
print (x.shape)
print (x.strides)


# Due to reshaping .. none of the below has changed 
print (x.dtype)
print (x.itemsize)
print(x.size)
print (x.nbytes)


# Reshaping to 3 Dimensional Arry -  3 layers of 3 Rows and 3 Columns 
x = np.array( [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27] )
print(x)

print (x.ndim)
print (x.shape)
print (x.strides)

print (x.dtype)
print (x.itemsize)
print(x.size)
print (x.nbytes)


x = x.reshape(3,3,3)
 
print (x)
print (x.ndim)
print (x.shape)
print (x.strides)

print (x.dtype)
print (x.itemsize)
print(x.size)
print (x.nbytes)

       

"""
For 1D array, shape return a  tuple with only 1 component (i.e. (n,))
For 2D array, shape return a  tuple with only 2 components (i.e. (n,m))
For 3D array, shape return a  tuple with only 3 components (i.e. (n,m,k) )
"""


"""
There are a couple of mechanisms for creating arrays in NumPy:
 a. Conversion from other Python structures (e.g., lists, tuples).
 b. Built-in NumPy array creation (e.g., arange, ones, zeros, etc.).
 c. Reading arrays from disk, either from standard or custom formats 
     (e.g. reading from a CSV file).
"""
# Using the built in function arange 

# Arange function will generate array from 0 to size-1 
# arange is similar to range function but generates an array , 
# where in range gives you a list of elements

import numpy as np 

x = np.arange(20, dtype=np.uint8)
print (x)
print (x.ndim)
print (x.shape)
print (x.dtype)
print (x.itemsize)

# zeros(shape) -- creates an array filled with 0 values with the specified shape.
# The default dtype is float64.

x = np.zeros((3, ))
print (x)
print (x.ndim)
print (x.shape)
print (x.dtype)
print (x.itemsize)


x = np.zeros((3, 3))
print (x)
print (x.ndim)
print (x.shape)
print (x.dtype)


x = np.zeros((3, 3, 3))
print (x)
print (x.ndim)
print (x.shape)
print (x.dtype)




# ones(shape) -- creates an array filled with 1 values. 

import numpy as np 
x = np.ones((3, ), dtype=np.int8 )
print (x)
print (x.ndim)
print (x.shape)
print (x.dtype)
print (x.itemsize)

x = np.ones((3, 3), dtype=np.int8 )
print (x)
print (x.ndim)
print (x.shape)
print (x.dtype)


x = np.ones((3, 3, 3), dtype=np.int8 )
print (x)
print (x.ndim)
print (x.shape)
print (x.dtype)


# linspace() -- creates arrays with a specified number of elements, 
# and spaced equally between the specified beginning and end values.

import numpy as np 
x = np.linspace(1, 4, 10, dtype = np.float) # try with float16,float32,float64
print (x)
print (x.ndim)
print (x.shape)
print (x.dtype)
print (x.itemsize)


import numpy as np 
#random.random(shape) – creates arrays with random floats over the interval [0,1].
x = np.random.random((2,3))*100
print (x)
print (x.ndim)
print (x.shape)
print (x.dtype)


# np.identity() to create a square 2d array with 1's across the diagonal
print (np.identity(n = 5))      # Size of the array



# np.eye() to create a 2d array with 1's across a specified diagonal
np.eye(N = 3,  # Number of rows
       M = 5,  # Number of columns
       k = 1)  # Index of the diagonal (main diagonal (0) is default)




# NaN can be defined using the following constant
print (np.nan)
print(type(np.nan))
# Infinite value can be expressed using the following contant 
print (np.inf)
print(type(np.inf))


x = np.array( [1,2,3], dtype=np.float ) 
print (x)
print(x.dtype)


x[0] = np.nan
x[2] = np.inf
print (x)

print (np.isnan(x[0]))
print(np.isnan(x))

print (np.isinf(x[2]))
print(np.isinf(x))

"""
Arrays Operations - Basic operations apply element-wise. 
The result is a new array with the resultant elements.
Operations like *= and += will modify the existing array.
"""

import numpy as np
a = np.arange(5) 
print (a)

b = np.arange(5) 
print(b)


x= np.array(list(zip(a,b)))
print (x) 
print (x.ndim)
print (x.shape)
print (x.dtype)

x = a + b
print (x) 

x = a - b
print (x)

x = a**3
print (x)
 
x = a>3
print (x)
 
x= 10*np.sin(a)
print (x) 

x = a*b
print (x)


"""
Mean, Median, Mode

Let's create some fake income data, centered around 27,000 
with a normal distribution and standard deviation of 15,000, with 10,000 data points. 
Then, compute the mean (average)

"""

import numpy as np
                          #mean, sd, total
incomes = np.random.normal(27000, 15000, 10000)
#loc=150, scale=20, size=1000

print (type(incomes))
print(incomes.size)
print (incomes)
print (len(incomes))
print (incomes.ndim)
print (incomes.shape)
print (incomes.dtype)

print("Mean value is: ", np.mean(incomes))
print("Median value is: ", np.median(incomes))


from scipy import stats
print("Mode value is: ", stats.mode(incomes)[0])
 

print("Minimum value is: ", np.min(incomes))
print("Maximum value is: ", np.max(incomes))
print("Standard Deviation is: ", np.std(incomes))
#print("Correlation coefficient value is: ", np.corrcoef(incomes))



#We can segment the income data into 50 buckets, and plot it as a histogram:
import matplotlib.pyplot as plt
plt.hist(incomes, 20)
plt.show()


#box and whisker plot to show distribution
#https://chartio.com/resources/tutorials/what-is-a-box-plot/
plt.boxplot(incomes)

# Explain NumPy_boxplot.png


print("Mean value is: ", np.mean(incomes))
print("Median value is: ", np.median(incomes))

#Adding Bill Gates into the mix. income inequality!(Outliers)
incomes = np.append(incomes, [10000000000])

#Median Remains Almost SAME
print("Median value is: ", np.median(incomes))

#Mean Changes distinctly
print("Mean value is: ", np.mean(incomes))

      
# Give an example for bincount function
# num = np.bincount(incomes).argmax()


"""
Basics of Matplotlib
    Scatter Plot
    Line Plot
    Pie Chart
    Bar Chart
"""

import matplotlib.pyplot as plt

x = [1,2,3,4,5,6,7,8,9,10]

y = [1,2,3,4,5,6,7,8,9,10]


# Setting the title
plt.title("A Line Graph")

# Setting the X Label 
plt.xlabel("X")

# Setting the Y Label
plt.ylabel("Y")

# Displaying the Grid
plt.grid(True)

# Changing the x axes limits of the scale
plt.xlim(0, 10)

# Changing the y axes limits of the scale
plt.ylim(0, 10)

# Or
plt.axis([0, 10, 0, 10])


# Showing the points on the graph
plt.scatter(x, y)

# Simple Line plot
plt.plot(x, y)

plt.savefig("scatter.jpg")

plt.show()


# Changing the color of the line
plt.plot(x, y, color='green') # #000000
plt.plot(x, y, color="#FF0000") # #000000

# Changing the style of the line
plt.plot(x, y, linestyle='dashed') # solid dashed  dashdot dotted

# For Plotting Scatter Plot
plt.plot(x, y, 'd', color='red') # o  .  , x  +  v  ^  <  >  s d 

# Scatter Plot with scatter method 
plt.scatter(x, y, marker='.', color='black',label="marker='{0}'".format('.')); # o  .  , x  +  v  ^  <  >  s d 
plt.legend(numpoints=1)



"""
Pie chart, where the slices will be ordered and plotted counter-clockwise:
"""

labels = 'CSE', 'ECE', 'IT', 'EE'
sizes = [15, 30, 25, 10]
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
explode = (0.5, 0, 0, 0)  # explode 1st slice

#plt.pie(sizes, labels=labels, autopct='%.0f%%')

# or

plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.2f%%', shadow=True, startangle=180)


plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()

        

"""
Plotting a bar chart
"""

import matplotlib.pyplot as plt; 
 
objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
performance = [10,8,6,4,2,1]
 
plt.bar([0,1,2,3,4,5], performance, align='center', alpha=1.0)
plt.xticks([0,1,2,3,4,5], objects)
plt.ylabel('Usage')
plt.title('Programming Language Usage')
 
plt.show()


"""
Ramesh is the branch manager at a local bank. 
Recently, Ramesh’s been receiving customer feedback saying that the wait times 
for a client to be served by a customer service representative are too long. 
Ramesh decides to observe and write down the time spent by each customer on waiting.

Write down the wait times spent by 20 customers
[43.1,35.6,37.6,45.3,43.5,40.3,50.2,47.3,31.2,42.2,45.5,30.3,31.4,35.6,45.2,
54.1,45.6,36.5,43.1]

"""

import matplotlib.pyplot as plt
# Customers wait times in seconds ( n = 20 customers )
customerWaitTime = [43.1,35.6,37.6,45.3,43.5,40.3,50.2,47.3,31.2,42.2,45.5,30.3,31.4,35.6,45.2,54.1,45.6,36.5,43.1]

customerWaitTime.sort()
# [1 to 35]      30.3, 31.2, 31.4                     [3]
# [35 to 40]     35.6, 35.6, 36.5, 37.6               [4]
# [40 to 45]     40.3, 42.2, 43.1, 43.1, 43.5         [5]
# [45 to 50]     45.2, 45.3, 45.5, 45.6, 47.3         [5]
# [50 to 55]     50.2, 54.1                           [2]

#Ramesh can conclude that the majority of customers wait between 35.1 and 50 seconds.

print(customerWaitTime)
 
plt.hist(customerWaitTime,bins=[25,30,35,40,45,50,55]) 

plt.axis([25, 60, 0, 6]) 
plt.xlabel('Seconds')
plt.ylabel('Customers')

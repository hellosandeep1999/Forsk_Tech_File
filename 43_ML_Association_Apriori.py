# Apriori
"""

Association is related to Retail / E Commerce business

Give Example of Amazon / Flipkart / Myntra, NetFlix - 
Suggestion / Recommendations comes at the bottom, 
they are different to different users.


Define the keyword Transaction in Ecommerce 
People doing shopping on the website is a transaction 
The recommendation is given based on the past transactions
When person buys item X, they also buy item Y, 
that means that X is associated to Y

This is known as Association 
Market Basket Analysis is the right term for Association 

Small store owners can understand the association manually since its small.
But its difficult for big malls or shops or online to do that, 
for that we require some tool.


Lets understand Association of inventory items at the stores to increase the 
sales and revenue
When we go grocery shopping, we often have a standard list of things to buy. 
Each shopper has a distinctive list, depending on one’s needs and preferences. 
A housewife might buy healthy ingredients for a family dinner, 
while a bachelor might buy beer and chips. 
Understanding these buying patterns can help to increase sales in several ways. 
If there is a pair of items, X and Y, that are frequently bought together:

1. Both X and Y can be placed on the same shelf, 
   so that buyers of one item would be prompted to buy the other.
2. Promotional discounts could be applied to just one out of the two items.
3. Advertisements on X could be targeted at buyers who purchase Y.
4. X and Y could be combined into a new product, such as having Y in flavors of X.

While we may know that certain items are frequently bought together, 
the question is, how do we uncover these associations?

Besides increasing sales profits, association rules can also be used in other fields. 
It helps in targetted promotions


In medical diagnosis for instance, understanding which symptoms tend to co-morbid 
can help to improve patient care and medicine prescription.

If we have the inventory list of a store.
How to find the association within the products when we have a dataset ?
We have the Apriori Algorithm, which gives a list of associations

Apriori Algorithm generates the association, based on 3 things 
    1. Support
    2. Confidence
    3. Lift


Define ticket size for a transaction

Lets Assume there are two item X and Y in the inventory.
If a person is buying X, he is also buying Y

then
X is known as the Base Item 
Y is known as the Supported Item

Take and example of Bread and Eggs.


Support 

This says how popular an itemset is, 
as measured by the proportion of transactions in which an itemset appears. 

Show image1_Apriori.jpg

There are 8 transaction in the table

In Table, the support of {apple} is 4 out of 8, or 50%. 
Out of all transactions, how many times that item is there

The Support {beer} is 6 out of 8, or 75%

If Support is more, that means item is popular.
Support is the indication of the popularity of the item


Itemsets can also contain multiple items. 

For instance, the support of {apple, beer} is 3 out of 8, or 37.5%.

For instance, the support of {apple, beer, rice} is 2 out of 8, or 25%.

It does not worry for the quanity of the item


If you discover that sales of items beyond a certain proportion tend to have a 
significant impact on your profits, you might consider using that proportion as 
your support threshold. 
You may then identify itemsets with support values above 
this threshold as significant itemsets.


Confidence

show image2_apriori.jpg

This says how likely item Y is purchased when item X is purchased, 
expressed as {X -> Y}. 
This is measured by the proportion of transactions 
with item X, in which item Y also appears. 

//confidence_measure

                                                  support{apple,beer}
confidence{apple-->beer}   =     --------------------------------
                                                      support{apple}

In Table 1, the confidence of {apple -> beer} is 3 out of 4, or 75%.
  3/8
  ---- =  3/4
  4/8


If someone has bought apple 3 times, 
he has also bought beer 4 times



What if Y is a popular item, then this logic fails
75% confidence is very HIGH value. 
We will interpret that people are buying Y because of X, 
but thats not the case since Y itself is popular


One drawback of the confidence measure is that it might misrepresent the 
importance of an association. 


This is because it only accounts for how popular apples are, but not beers. 
If beers are also very popular in general, there will be a higher chance that a 
transaction containing apples will also contain beers, 
thus inflating the confidence measure. 
To account for the base popularity of both constituent items, 
we use a third measure called lift.


Lift
show image3_apriori

This says how likely item Y is purchased when item X is purchased, 
while controlling for how popular item Y is. 

In Table 1, 
the lift of {apple -> beer} is 1,which implies no association between items.    
( Neutral Association )
A lift value greater than 1 means that item Y is likely to be bought 
if item X is bought, ( Positive Assocition )
while a value less than 1 means that item Y is unlikely to be bought 
if item X is bought. ( Negative Association )

Lift == 1  ( Neutral Association )
Lift  > 1  ( Positive Association )
Lift  < 1  ( Negative Association )


                               support{apple,beer}
Lift{apple-->beer} =--------------------------------
                           support{apple} * support{beer}


Take example if Aman and Manas taking a decission to join Forsk for Summer Training

Where Manas is going, Aman does not care, then Neutral Association
Where Manas will go Aman will go, then Strong Association 
Where Manas is going Aman will not go, then Negative Association 

Our Apriori Algo uses Support, Confidence and Lift to find Association 




Apriori Algo is missing in the Sklearn library 
UCI Repository Introduction 

Where to download the library
https://pypi.python.org/pypi/apyori/1.1.1
https://pypi.org/project/apyori/1.1.1/

open apyori.py and show the apriori(transactions, **kwargs) function in it

apyori.py is the source code where the algo is implemented
and there is a function name apriori within that module which does that work
download and keep at the same place where you has the current source code

The first argument is the transaction, which is a Bigger list and contains smaller list 
Now write code to read all the data and create the list of list ( transaction ) 

**kwargs concept if key, 
value pairs for variable number of arguments for a function 

Arguments:
    100 bills generated every day 
    75 days 
    7500 bills = transaction 
    every transaction willhave multiple items
    
        transactions -- A transaction iterable object
                        (eg. [['A', 'B'], ['B', 'C']]).

Keyword arguments:
        min_support -- The minimum support of relations (float). (0.1)
        min_confidence -- The minimum confidence of relations (float).(0.0)
        min_lift -- The minimum lift of relations (float). (0.0)
        max_length -- The maximum length of the relation (integer).(None)
        

How to calculate min_support
min support - product is purchased atleast 3 times in a day
so support should be: (3*7)/7500 ~ .003

Similarly calculate if item is bought 5 times a day

How to calculate min_confidence
If item X is 100 times a day, then item Y is 25 times a day 

Similarly lift value should be HIGH 

Europe retail store data
open Market_Basket_Optimisation.csv and explain it
"""

# Importing the libraries
import pandas as pd
from apyori import apriori

# Data Preprocessing
# Column names of the first row is missing, header - None
dataset = pd.read_csv('Market_Basket_Optimisation.csv', header = None)

print([str(dataset.values[1,j]) for j in range(0, 20) ])

#type(dataset.iloc[1,0]) is float
#type(dataset.iloc[1,3]) is float
#print([str(dataset.values[1,j]) for j in range(0, 20) ])
#print([str(dataset.values[1,j]) for j in range(0, 20) if (type(dataset.values[1,j]) is not float )])

transactions = []
for i in range(0, 7501):
    #transactions.append(str(dataset.iloc[i,:].values)) #need to check this one
    transactions.append([str(dataset.values[i,j]) for j in range(0, 20)])


# Training Apriori on the dataset
rules = apriori(transactions, min_support = 0.003, min_confidence = 0.25, min_lift = 4)

print(type(rules))

# next(rules)

"""
Shortcut to write a generator

q = (i**2 for i in [1,2,3,4,5])
print(type(q))
next(q)
p = list(q)
print(p)
"""


# Visualising the results
results = list(rules)
print(len(results))

results[0]
results[0].items
results[0][0]


results[0].support 
results[0][1]  #--> support


results[0].confidence 
# at index = 2 we have ordered_statistics
results[0][2]
results[0][2][2]
results[0][2][0]
results[0][2][0][2]  #--> Confidence
results[0][2][0][3]  #--> Lift


for item in results:
    # first index of the inner list
    # Contains base item and add item
    pair = item[0] 
    items = [x for x in pair]
    print("Rule: " + items[0] + " -> " + items[1])

    #second index of the inner list
    print("Support: " + str(item[1]))

    #third index of the list located at 0th
    #of the third index of the inner list

    print("Confidence: " + str(item[2][0][2]))
    print("Lift: " + str(item[2][0][3]))
    print("=====================================")


"""
Code Challenge:
dataset: BreadBasket_DMS.csv

Q1. In this code challenge, you are given a dataset which has data 
and time wise transaction on a bakery retail store.
1. Draw the pie chart of top 15 selling items.
2. Find the associations of items where min support should be 0.0025, 
min_confidence=0.2, min_lift=3.
3. Out of given results sets, show only names of the associated 
item from given result row wise.



Code Challenge:
Dataset: Market_Basket_Optimization.csv
Q2. In today's demo sesssion, we did not handle the null values before 
fitting the data to model, 
remove the null values from each row and perform the associations once again.
Also draw the bar chart of top 10 edibles.

"""


# skip from here onwards
    



# Hands On with Solution with Large Data

import pandas as pd

df = pd.read_excel('http://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx')
df.head()

"""
There is a little cleanup, we need to do. 
First, some of the descriptions have spaces that 
need to be removed. We’ll also drop the rows that 
don’t have invoice numbers and remove the credit 
transactions (those with invoice numbers containing C).
"""

df['Description'] = df['Description'].str.strip()
df.dropna(axis=0, subset=['InvoiceNo'], inplace=True)
df['InvoiceNo'] = df['InvoiceNo'].astype('str')
df = df[~df['InvoiceNo'].str.contains('C')]

df.head()
"""
After the cleanup, we need to consolidate the 
items into 1 transaction per row with each
 product 1 hot encoded. For the sake of keeping
 the data set small, I’m only looking at sales 
 for France. However, in additional code below, 
 I will compare these results to sales from 
 Germany. Further country comparisons would 
 be interesting to investigate.
"""

basket = (df[df['Country'] =="France"]
          .groupby(['InvoiceNo', 'Description'])['Quantity']
          .sum().unstack().reset_index().fillna(0)
          .set_index('InvoiceNo'))

"""
There are a lot of zeros in the data but we also 
need to make sure any positive values are converted to 
a 1 and anything less the 0 is set to 0. This step will 
complete the one hot encoding of the data and remove the 
postage column (since that charge is not one we wish to 
explore):
"""
def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1

basket_sets = basket.applymap(encode_units)
basket_sets.drop('POSTAGE', inplace=True, axis=1)

"""
Now that the data is structured properly, 
we can generate frequent item sets that have a 
support of at least 7% (this number was chosen so that 
I could get enough useful examples):
"""

"""
The final step is to generate the rules with their corresponding support, confidence and lift:
"""
rules = apriori(basket_sets, min_support=0.07,min_confidence = 0.25, min_lift = 3)

results = list(rules)


"""
removing the null values from the dataframe
transactions = dataset.apply(lambda x: x.dropna().tolist(), axis=1).tolist()

"""


 







"""
Introduce the concept of Recommendation Engine ? 
Give example of Netflix
Tool - Collaborative Filtering
LightFm / Surprise Library 


https://stackabuse.com/association-rule-mining-via-apriori-algorithm-in-python/



https://pbpython.com/market-basket-analysis.html



Other examples

https://github.com/amitkaps/machine-learning/blob/master/cf_mba/notebook/2.%20Market%20Basket%20Analysis.ipynb

Get some sample data from below:
    
https://github.com/theankurkedia/market_basket/blob/master/sample_input.csv



https://www.kdnuggets.com/2016/04/association-rules-apriori-algorithm-tutorial.html/2
"""
"""
Implemetation Papers
http://adrem.uantwerpen.be/bibrem/pubs/mampaey-thesis06.pdf
https://www-users.cs.umn.edu/~kumar001/dmbook/ch6.pdf
"""

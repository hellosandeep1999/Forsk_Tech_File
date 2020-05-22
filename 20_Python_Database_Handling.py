"""
Database Handling ( sqlite, mysql, mysql online, mongodb and mongo atlas )
"""


"""
Database handling using sqlite 
"""

import sqlite3
from pandas import DataFrame


# File based database ( connects if exists or creates a new one if it does not exists ) 
conn = sqlite3.connect ( 'employee.db' )


# creating cursor
c = conn.cursor()

#Delete the table
c.execute("DROP TABLE employees")
conn.commit()

# STEP 1
# www.sqlite.org/datatype3.html
c.execute ("""CREATE TABLE employees(
          id INTEGER,
          first  TEXT,
          last TEXT, 
          pay INTEGER
          )"""
          )
conn.commit()


# STEP 2
c.execute("INSERT INTO employees VALUES (01,'Sylvester', 'Fernandes', 50000)")
c.execute("INSERT INTO employees VALUES (02,'Yogendra', 'Singh', 70000)")
c.execute("INSERT INTO employees VALUES (03,'Rohit', 'Mishra', 30000)")
c.execute("INSERT INTO employees VALUES (04,'Kunal', 'Vaid', 30000)")
c.execute("INSERT INTO employees VALUES (05,'Devendra', 'Shekhawat', 30000)")

conn.commit()


# STEP 3
c.execute("SELECT * FROM employees")
# "SELECT * FROM employees WHERE last = 'Fernandes' "



# STEP 4
# returns one or otherwise None as a tuple
print ( c.fetchone()) 

# returns one or otherwise None as a tuple
print ( c.fetchmany(2)) 

# returns a list of tuples
print ( c.fetchall() )


# Since now the cursor has read all the rows and we are at End
# So again fetching the records from the database
c.execute("SELECT * FROM employees")


# STEP 5
df = DataFrame(c.fetchall())  # putting the result into Dataframe
df.columns = ["id","first","last","pay"]
#df.to_csv("employee.csv")


# STEP 6
# closing the connection 
conn.close()



print ( c.fetchone()) 




"""
Database handling using MySQL on Local Machine
"""

"""
old technique
#use below command in anaconda prompt
# conda install mysql-connector
# pip install --upgrade pip 
# pip install -U setuptools
# pip install -U wheel
# pip install protobuf
# pip install mysql-connector-python-rf
#pip install argparse
"""

#use below command in anaconda prompt
# pip install mysql-connector-python


from pandas import DataFrame
import mysql.connector



# File based database ( connects if exists or creates a new one if it does not exists ) 
conn = mysql.connector.connect ( user='root', password='', host='localhost')
# database = '' can be used if we want to connect to already defined database


# creating cursor
c = conn.cursor()

# STEP 0 if exists
c.execute("DROP DATABASE IF EXISTS employee;")
conn.commit()

# STEP 1
c.execute("CREATE DATABASE employee;")
conn.commit()

# STEP 2
c.execute("USE employee;")
conn.commit()

# STEP 3
c.execute ("""CREATE TABLE employees(
          id INTEGER,
          first  TEXT,
          last TEXT,
          pay INTEGER
          )""")
conn.commit()


# STEP 4
c.execute("INSERT INTO employees VALUES (01,'Sylvester', 'Fernandes', 50000)")
c.execute("INSERT INTO employees VALUES (02,'Yogendra', 'Singh', 70000)")
c.execute("INSERT INTO employees VALUES (03,'Rohit', 'Mishra', 30000)")
c.execute("INSERT INTO employees VALUES (04,'Kunal', 'Vaid', 30000)")
c.execute("INSERT INTO employees VALUES (05,'Devendra', 'Shekhawat', 30000)")

conn.commit()

# c.execute("INSERT INTO employee VALUES ({},'{}', '{}', {})".format(idd, first,last,pay))


c.execute("SELECT * FROM employees")

# STEP 5
# returns one or otherwise None as a tuple
print ( c.fetchone()) 

# returns one or otherwise None as a tuple
print ( c.fetchmany(2)) 

# returns a list of tuples
print ( c.fetchall() )


# Since now the cursor has read all the rows and we are at End
# So again fetching the records from the database
c.execute("SELECT * FROM employees")



# STEP 6
df = DataFrame(c.fetchall())  # putting the result into Dataframe
df.columns = ["id","first","last","pay"]

# field_names = [i[0] for i in c.description]
# print field_names


conn.close()






"""
Database handling using MySQL on Cloud
Relational DB Vs NoSQL DB
"""


"""
https://www.db4free.net
https://www.db4free.net/phpMyAdmin/
MySQL Host Name : db4free.net
Port : 3306
MySQL database name:  forsk_test
MySQL username: forsk_root
MySQL user password: cooler2112 
Email address:  sylvester@forsk.in
MYSQL URL : mysql://forsk_root:cooler2112@db4free.net/forsk_test

"""


"""
https://www.db4free.net
https://www.db4free.net/phpMyAdmin/
MySQL Host Name : db4free.net
Port : 3306
MySQL database name:  forskdb
MySQL username: forsktech
MySQL user password: Forsk@123 
Email address:  pradeepnatani9@gmail.com
MYSQL URL : mysql://forsktech:Forsk@123@db4free.net/forskdb

"""

# !pip install mysql-connector-python


import mysql.connector 
# connect to  MySQL server along with Database name

conn = mysql.connector.connect(user='forsk_root', password='cooler2112',
                              host='db4free.net', database = 'forsk_test')
#database = 'forsk_test'

#creating cursor
c = conn.cursor()

# STEP 0
#c.execute("DROP DATABASE employee;")

# STEP 1
#c.execute("CREATE DATABASE employee;")

# STEP 2
c.execute("DROP Table employees;")

# STEP 3
c.execute ("""CREATE TABLE employees(
          id INTEGER,
          first  TEXT,
          last TEXT,
          pay INTEGER
          )""")


# STEP 4
c.execute("INSERT INTO employees VALUES (01,'Sylvester', 'Fernandes', 50000)")
c.execute("INSERT INTO employees VALUES (02,'Yogendra', 'Singh', 70000)")
c.execute("INSERT INTO employees VALUES (03,'Rohit', 'Mishra', 30000)")
c.execute("INSERT INTO employees VALUES (04,'Kunal', 'Vaid', 30000)")
c.execute("INSERT INTO employees VALUES (05,'Devendra', 'Shekhawat', 30000)")

# c.execute("INSERT INTO employee VALUES ({},'{}', '{}', {})".format(idd, first,last,pay))


c.execute("SELECT * FROM employees")


# STEP 5
# returns one or otherwise None as a tuple
print ( c.fetchone()) 

# returns one or otherwise None as a tuple
print ( c.fetchmany(2)) 

# returns a list of tuples
print ( c.fetchall() )


# Since now the cursor has read all the rows and we are at End
# So again fetching the records from the database
c.execute("SELECT * FROM employees")


# STEP 6
df = DataFrame(c.fetchall())  # putting the result into Dataframe
df.columns = ["id","first","last","pay"]

conn.close()





####################################################################
####################################################################
####################################################################
####################################################################
####################################################################













"""
Database handling using MongoDB locally
"""

#use below command in anaconda prompt or run with ! in the console
#pip install pymongo


from pymongo import MongoClient

client = MongoClient('localhost', 27017)

# create the database if does not exists
mydb = client.employee



# adding the employee in the employee collection
def add_employee(idd, first, last, pay):
    unique_employee = mydb.employees.find_one({"id":idd})
    if unique_employee:
        return "Employee already exists"
    else:
        mydb.employees.insert(
                {
                "id" : idd,
                "first" : first,
                "last" : last,
                "pay" : pay
                })
        return "Employee added successfully"

def fetch_all_employee():
    user = mydb.employees.find()
    for i in user:
        print (i)


#Drop a collection in Mongo
mydb.employees.drop()


#Insert data in collection
add_employee(1,'Sylvester', 'Fernandes', 50000)
add_employee(2,'Yogendra', 'Singh', 70000)
add_employee(3,'Rohit', 'Mishra', 30000)
add_employee(4,'Kunal', 'Vaid', 30000)
add_employee(5,'Devendra', 'Shekhawat', 30000)

fetch_all_employee()
    



"""
Database handling using MongoDB on Cloud -  Mongo Atlas
"""
#use below command in anaconda prompt or run with ! in the console
# !pip install pymongo
# !pip install dnspython


"""
pip install or conda install the libraries
Create Mongo Atlas Account and Verify it via the email
#https://cloud.mongodb.com

Create a cluster
Create Database
Give Database Access
Give Network Access
Create Collection 
Then Connect to get the python 3.4 sample code

# AWS N. Virginia Free Tier - MO Sandbox 
# Database Access - database access as Admin for new user with Read and Write Access
# Autopasssword generation should be used
# Security/Network Access - IP Whitelisting 0.0.0.0/0 ( Access from anywhere)

"""








#https://krypted.com/utilities/html-encoding-reference/


import pymongo

#client = pymongo.MongoClient("mongodb://K_Vaid:123chandu30%26@cluster0-shard-00-00-tofyu.mongodb.net:27017,cluster0-shard-00-01-tofyu.mongodb.net:27017,cluster0-shard-00-02-tofyu.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true")
#mydb = client.forsk_db

#client = pymongo.MongoClient("mongodb://forsktech:Forsk%40123@cluster0-shard-00-00-tdcf5.mongodb.net:27017,cluster0-shard-00-01-tdcf5.mongodb.net:27017,cluster0-shard-00-02-tdcf5.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true")
#mydb = client.forsk_db

#client = pymongo.MongoClient("mongodb://K_Vaid:123chandu30%26@cluster0-shard-00-00-tofyu.mongodb.net:27017,cluster0-shard-00-01-tofyu.mongodb.net:27017,cluster0-shard-00-02-tofyu.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true")
#mydb = client.sampledb

client = pymongo.MongoClient("mongodb+srv://sylvesterferns:cooler%21%40%23123@cluster0-t6mku.mongodb.net/test?retryWrites=true&w=majority")
mydb = client.forsk_db



def add_employee(idd, first, last, pay):
    unique_employee = mydb.forsk_coll.find_one({"id":idd})
    if unique_employee:
        return "Employee already exists"
    else:
        mydb.forsk_coll.insert_one(
                {
                "id" : idd,
                "first" : first,
                "last" : last,
                "pay" : pay
                })
        return "Employee added successfully"


def fetch_all_employee():
    user = mydb.forsk_coll.find()
    for i in user:
        print (i)




#Insert data in collection
add_employee(1,'Sylvester', 'Fernandes', 50000)
add_employee(2,'Yogendra', 'Singh', 70000)
add_employee(3,'Rohit', 'Mishra', 30000)
add_employee(4,'Kunal', 'Vaid', 30000)
add_employee(5,'Devendra', 'Shekhawat', 30000)

fetch_all_employee()



#Drop a collection in Mongo
mydb.forsk_coll.drop()

"""
Code Challenge 1
ICC cricket data base

"""


# Database handling using MongoDB on Cloud ( mLab )  OLD Technique 
# Steps to create DB and Account online mLab

import requests
import json
api_key = "65mczz6BHJHLMxUayNO2VXNYWedu11q4"
collection = "employee"
database = "employees"

data_dict = {}

# adding the employee in the employee collection
def add_employee(idd, first, last, pay):
  
  data_dict = {"id" : idd,"first" : first,"last" : last,"pay" : pay}
  add_data_to_mlab(data_dict)
        
        

res = ""
def add_data_to_mlab(data_dict):
    
    url = "https://api.mlab.com/api/1/databases/{}/collections/{}?apiKey={}".format(database,collection,api_key)
    response = requests.post(url, json =data_dict)
    
    res = response.status_code
    if res == 200:
        print ("data added successfully")
    else:
        print ("response is something else:")
        print (res)



    
def fetch_all_employee():
    
    url = "https://api.mlab.com/api/1/databases/{}/collections/{}?apiKey={}".format(database,collection,api_key)
    response = requests.get(url)
    
    res = json.loads(response.text)
    print (res)
    
    
    
    
add_employee(01,'Sylvester', 'Fernandes', 50000)
add_employee(02,'Yogendra', 'Singh', 70000)
add_employee(03,'Rohit', 'Mishra', 30000)
add_employee(04,'Kunal', 'Vaid', 30000)
add_employee(05,'Devendra', 'Shekhawat', 30000)

fetch_all_employee()





"""
There are numerous ORM implementations written in Python, including

    SQLAlchemy
    Peewee
    The Django ORM
    PonyORM
    SQLObject
    Tortoise ORM

"""

# Add code for SQL ALCHEMY ( object-relational mapper (ORM) )  and update the code for mlab


# -*- coding: utf-8 -*-
""" A program to implement database handling through sqlalchemy module """

# to create engine to through the database importing create_engine from sqlalchemy
# Impporting some methods required for creating a table
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey

# Importing declarative_base to create a base class to be inherited by other classes creating tables
from sqlalchemy.ext.declarative import declarative_base

# Importing sessionmaker to create session for exceuting various operations on our database
# sessionmaker allows to create a session factory
from sqlalchemy.orm import sessionmaker
# Initializing the base class
Base = declarative_base()

# Inintializing the class for employee table
class Employee_details(Base):
    # Initializing the table name
    __tablename__ ="Employee"

    # Creating our table field
    empid = Column('empid', Integer, primary_key=True)
    first = Column('first', String)
    last = Column ('last', String)
    pay = Column('pay', Integer)
# Using sqlite as dialect for database management
# dialect+driver :/// filename
# setting echo True will dump or show all the commands executed internally
engine = create_engine("sqlite:///employee.sqlite",echo=True)

# Creating our table schema bind to engine
Base.metadata.create_all(bind=engine)



# Initializing the values to be inseted in the table
ids = [1, 2, 3]
first_names = ['Sylvester', 'Yogendra', 'Kunal']
last_names =['Fernandes', 'Singh', 'Vaid']
salary = [50000, 70000, 30000]

# Ziping all the data in a single list
final_data = list(zip(ids,first_names,last_names,salary))



# CRUD operation - Create, read, update, delete
# Step-1
# Creating a function for adding data to the table
def add_data(c, var_0, var_1, var_2, var_3):

    # Creating a session factory bind to engine
    Session_c = sessionmaker(bind=engine)

    # Creating an object of table class
    emp_c = Employee_details()

    # Creating a session
    session_c = Session_c()

    # Inserting values in the employee table
    emp_c.empid = var_0
    emp_c.first = var_1
    emp_c.last = var_2
    emp_c.pay = var_3
    session_c.add(emp_c)
    # Commiting the changes made during the session
    session_c.commit()
    # closing the sesssion
    session_c.close()

# Step- 2
# Function to read data from employee database
def read_data():
    # To view our data stored in the table
    Session = sessionmaker(bind=engine)
    session = Session()
    empl = session.query(Employee_details)
    for var2 in empl:
        print(var2.empid, var2.first, var2.last, var2.pay)
    session.close()

# Step-3
# Function to update data in the employee database
def update_data(row_value, value):
    Session = sessionmaker(bind=engine)
    session = Session()
    emp_upd = session.query(Employee_details).filter(Employee_details.empid == row_value).update(value)
    session.commit()
    session.close()

# Step-4
# Function to delete data in the employee database
def delete_data(row_value):
    Session = sessionmaker(bind=engine)
    session = Session()
    emp_del = session.query(Employee_details).filter(Employee_details.empid == row_value).delete()
    session.commit()
    session.close()

# Initializing the count to create different session for adding multiple data
count = 0
# Function Call to add data
for var in final_data:
    # Function call for adding data
    add_data(count, var[0], var[1], var[2], var[3])

    # Increasing count after adding the data to the table
    count += 1

# Function call to read data
read_data()

# To update salary in the database of employee having empid==2
# 1.Initializing the column to be updated for that particular row with the new value.
col_upd = {'pay':100000}

# Function call to update data in the employee database
update_data(2, col_upd)

# Function call to delete the data from database having empid == 2
delete_data(2)





"""

Code Challenge 1
Write a python code to insert records to a mongo/sqlite/MySQL database named db_University for 10 students with fields like Student_Name, Student_Age, Student_Roll_no, Student_Branch.



Code Challenge 2

Perform similar steps as in the above code challenge but store the contents in an online mongo database named mLab.

https://mlab.com/home

https://docs.mlab.com/data-api/

"""

"""

Code Challenge 1
Write a python code to insert records to a sqlite
named db_University for 10 students with fields like 
Student_Name, Student_Age, Student_Roll_no, Student_Branch.



Code Challenge 2
Perform similar steps as in the above code challenge but store the contents in 
an online mongo atlas database.


Code Challenge 3
In the Bid plus Code Challenege 

          1. BID NO
          2. items
          3. Quantity Required
          4. Department Name And Address
          5. Start Date/Time(Enter date and time in different columns)
          6. End Date/Time(Enter date and time in different columns)

Store the information into a database mySQL Database on cloud 

"""


"""
# Best practice for making functions for INSERT, UPDATE, DELETE and SELECT and a class

Employee.py

class Employee :
"A sample Employee class"

def __init__(self, first, last, pay ) :
  self.first = first 
  self.last = last
  self.pay = pay

@property
def email(self) :
  return ‘{}.{}@email.com’.format(self.first,self.last)

@property
def fullname(self):
  return’{} {}’.format(self.first,self.last)

def __repr__(self):
  return “Employee(‘{}, ‘{}’, {})”.format(self.first,self.last,self.pay)


db.py

from employee import Employee 
emp_1 = Employee (‘John’, ‘Doe’, 80000)
emp_2 = Employee (‘Jane’, ‘Doe’, 90000)

print (emp_1.first)
print (emp_1.pay)
print (emp_1.last)

c.execute( “INSERT INTO employees VALUES ( ?, ?, ?)”, (emp_1.first,emp_1.last,emp_1.pay ) )

## or better way 

c.execute ("INSERT INTO employees VALUE (:first,:last,:pay)”, {‘first’:emp_1.first}, {‘last’:emp_1.last}, {‘pay’:emp_1.pay})

# we need a comma to specify it as tuple..it looks strange
c.execute(“SELECT * FROM employees WHERE last = ? ”, (’Schafer’, ) )

# or better way 
c.execute(“SELECT * FROM employees WHERE last = :last”,{‘last’:’Doe'} )


def insert_emp(emp):
  pass

def get_emps_by_name(lastname):
  pass

def update_pay ( emp, pay ):
  pass

def remove_emp(emp):
  pass

"""





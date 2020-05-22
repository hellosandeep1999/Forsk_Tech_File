"""

Code Challenge
  Name: 
    Student and Faculty JSON
  Filename: 
    student.json
    faculty.json
  Problem Statement:
    Create a student and Faculty JSON object and get it verified using jsonlint.com
    Write a JSON for faculty profile. 
    The JSON should have profile of minimum 2 faculty members. 
    The profile for each faculty should include below information atleast:

        First Name
        Last Name
        Photo (Just a random url)
        Department 
        Research Areas (can be multiple)
        Contact Details (should include phone number and email id and can have multiple )
   Hint:
       www.jsonlint.com
       
"""



"""
Code Challenge
  Name: 
    JSON Parser
  Filename: 
    json.py
  Problem Statement:
    Get me the other details about the city
        Latitude and Longitude
        Weather Condition
        Wind Speed
        Sunset Rise and Set timing
"""

"""
Code Challenge
  Name: 
    Currency Converter Convert  from USD to INR
  Filename: 
    currecncyconv.py
  Problem Statement:
    You need to fetch the current conversion prices from the JSON  
    using REST API
  Hint:
    http://free.currencyconverterapi.com/api/v5/convert?q=USD_INR&compact=ultra&apiKey=07ca862e0b339dd56245
    Check with http://api.fixer.io/latest?base=USD&symbol=EUR
    
"""

"""
Code Challenge
  Name: 
    Posting of Data
  Filename: 
    httpbin.py
  Problem Statement:
    Create a client REST API that sends and receives some information from 
    the Server by calling server's REST API.
    You are expected to create two functions each for Sending and 
    Receiving data.
    You need to make two api calls, one with POST method for sending data 
    and the other with GET method to receive data
    All the communication i.e. sending and receiving of data with the 
    server has to be in JSON format
  Hint:
    Host: httpbin.org
    Port :  80
    Protocol : POST
    URI : /post
    Content-Length: 32 

    firstname=Chris&language=English
"""


# Code Challenge

"""
Research the below wesbite and post some data on it
https://requestbin.com
"""


"""
Code Challenge
  Name: 
    Webscrapping ICC Cricket Page
  Filename: 
    icccricket.py
  Problem Statement:
    Write a Python code to Scrap data from ICC Ranking's 
    page and get the ranking table for ODI's (Men). 
    Create a DataFrame using pandas to store the information.
  Hint: 
    https://www.icc-cricket.com/rankings/mens/team-rankings/odi 
    
    
    #https://www.icc-cricket.com/rankings/mens/team-rankings/t20i
    #https://www.icc-cricket.com/rankings/mens/team-rankings/test 
    
"""



"""
Code Challenge
  Name: 
    Next Bus
  Filename: 
    nextbus.py
  Problem Statement:
    Write a Python code to find when will the next bus come
    Try to make the program generalised so that is in not hard wired for bus route 22 and stop id 14787
    Also try if you can take the arguments from the command line
    Also try if you can run the program as a script from comand line
    
  Sample:
      Route 22 and Stop 14787
      Route 0 and Stop 5037
    
  Hint: 
    http://ctabustracker.com/bustime/map/getStopPredictions.jsp?route=22&stop=14787 
    
"""


"""
Code Challenge:
  Name: 
    Bid Plus
  Filename: 
    bid_plus.py
  Problem Statement:
      USE SELENIUM
      Write a Python code to Scrap data and download data from given url.
      url = "https://bidplus.gem.gov.in/bidlists"
      Make list and append given data:
          1. BID NO
          2. items
          3. Quantity Required
          4. Department Name And Address
          5. Start Date/Time(Enter date and time in different columns)
          6. End Date/Time(Enter date and time in different columns)
          
          # Optional - Do not do this
          7. Name of the PDF file
          
     Make a csv file add all data in it.
      csv Name: bid_plus.csv
"""


"""
Code Challenge:
    
http://forsk.in/images/Forsk_logo_bw.png"

Download the image from the url above and store in your workking diretory with the same
name as the image name.

Do not hardcode the name of the image

Solution:
https://www.geeksforgeeks.org/downloading-files-web-using-python/


"""

""""

Logpuzzle exercise  ( logpuzzle.py)

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

import os
import re
import sys
import urllib



def read_urls(filename):
  Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order.
  # +++your code here+++
  

def download_images(img_urls, dest_dir):
  Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  
  # +++your code here+++
  

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()


"""
















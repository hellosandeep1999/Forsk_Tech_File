# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 13:27:28 2020

@author: user
"""


import gspread_dataframe as gd
import pandas as pd
import pandas
import numpy as np
import numpy
import os 
import time
from datetime import datetime
import glob
import platform
import logging
import gspread
from google.oauth2.service_account import Credentials
import urllib
from urllib.request import urlopen
import sys

#This line use for hiding all pandas warnings
pd.options.mode.chained_assignment = None

def is_internet():
    
    try:
        urlopen("https://www.google.com",timeout=1)
        return True
    except urllib.error.URLError as Error:
        print("Error 1 ",Error)
        return False

if is_internet():
    
    #This line use for hiding all pandas warnings
    pd.options.mode.chained_assignment = None
    
    try:
        Meeting_id = int(input("Please Enter your Meeting Id: "))  #taking input Meeting Id
    except:
        print("Error:  -->  Wrong Input in meeting id please Check again")
        sys.exit(1)
   
    
    
    #Making a directory by name Reports
    if not os.path.exists("Reports"):
        os.makedirs("Reports")
        
    #Creating the log file
    LOG_FILENAME = 'Reports/{}.log'.format(Meeting_id)
    logging.basicConfig(filename=LOG_FILENAME, filemode='w', format='%(asctime)s - %(name)s - %(lineno)d - %(message)s',level=logging.DEBUG)
    
    try:
        #define credentials and scope of Google sheets API for our script
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        credentials = Credentials.from_service_account_file('Creds.json', scopes=SCOPES)
        client = gspread.authorize(credentials)
    except FileNotFoundError as msg1:
        print("Error 2",msg1)
        sys.exit(1)
    
    
    
    #whats your system I want to know by platform.system()
    using_system = platform.system()
    
    
    logging.warning('logging file Starts from here')  #our logging file work start from here
    logging.warning('You entered Metting id  - %d',Meeting_id)
    logging.warning('Your Used platform - %s',using_system)
    
    
    #some address which we will define here and use in whole program
#    win_cloud_dir = "c:/Users/Cloud"                 #for windows
#    win_master_file = "c:/Users/Cloud/Master.csv"   #for windows
    
#    mac_cloud_dir = "/Users/sylvester/Cloud"                  #for mac
#    mac_master_file = "/Users/sylvester/Cloud/Master.csv"    #for mac
    
    
    Inside_report_excel = "Reports/{}.csv".format(Meeting_id)  #This is for Excel sheet which is inside in Report folder
    if os.path.exists("{}-pay.xlsx".format(Meeting_id)):
        excel_file_num = int(input("\n1. {}.xlsx\n2. {}-pay.xlsx\nBoth files are available which want to you choose (1 or 2): ".format(Meeting_id,Meeting_id)))
        if excel_file_num == 1:
            outside_excel = "{}.xlsx".format(Meeting_id)
        else:
            outside_excel = "{}-pay.xlsx".format(Meeting_id)
    else:
        outside_excel = "{}.xlsx".format(Meeting_id)                #outside excel sheet
    
    
    
    
    #you want to UI or not
    try:
        UI_run = input("Do you want to See UI: ")
    except:
        print("Error:  -->  Wrong Input in UI_run please Check again")
        sys.exit(1)

    
    
    
    
    #find all csv and excel files of our program 
    extension1 = 'csv'
    extension2 = 'xlsx'
    All_csv_files = glob.glob('*.{}'.format(extension1))  #this is for csv file
    All_excel_files = glob.glob('*.{}'.format(extension2))  #this is for excel file
    All_files = All_csv_files + All_excel_files
    
    
    check_file_count = 0
    for check_file in All_files:
        if str(Meeting_id) in check_file:
            check_file_count += 1
       
        
    All_files = [check1_file for check1_file in All_files if str(Meeting_id) in check1_file]
    All_files = sorted(All_files)
    logging.warning('Matching files with Meeting id - %s',All_files)
    
    
    #checking the condition for excel file in directory is available or not
    csv_avail = 0
    Excel_avail = 0
    for file1 in All_files:
        if ".csv" in file1:
            csv_avail = 1
        if ".xlsx" in file1:
            Excel_avail = 1
    
    
    #Main condition it will check that if all csv files and xlsx have same metting id than it will execute
    if csv_avail == 1 and Excel_avail == 1 and len(All_files) == check_file_count:
        
        
        #This Part for Reconciliation and it will check both Excel sheet if any new data than he will be update
        def Reconcilation_process():
           Inner_file = pd.read_csv("{}".format(Inside_report_excel))
           total_column2 = len(Inner_file.columns.tolist())
           Inner_file.dropna(thresh=total_column2-16,inplace=True)
           Inner_file.reset_index(inplace = True, drop = True)
           logging.warning('Inside of report meeting id file Shape - %s',Inner_file.shape)
           Inner_file['UTR No ( PhonePe)'] = Inner_file['UTR No ( PhonePe)'].fillna('')
           
           outer_file = pd.read_excel("{}".format(outside_excel)) 
           total_column1 = len(outer_file.columns.tolist())
           outer_file.dropna(thresh=total_column1-8,inplace=True)
           outer_file.reset_index(inplace = True, drop = True)
           logging.warning('Outer of report meeting id file Shape - %s',outer_file.shape)
           
           
           mail_id_column_name = []
           for column_name in outer_file.columns.tolist():
               if "MAIL" in column_name.upper():
                   mail_id_column_name.append(column_name)
                   break
           
           Inner_file_Email_list = Inner_file["Email ID"].values.tolist()
           outer_file_Email_list = outer_file[mail_id_column_name[0]].values.tolist()
        
        
           for out_Email_index,out_Email in enumerate(outer_file_Email_list):
               if out_Email in Inner_file_Email_list:
                   INNa_index = Inner_file[Inner_file["Email ID"] == str(out_Email)].index[0]
                   if Inner_file['UTR No ( PhonePe)'][INNa_index] == '':
                       Reconcil_columns_list = []
                       double_time_name = []
                       def make_Reconcil_columns_list(column_n1):
                            run_last_if_cond = 0
                            for column_name2 in outer_file.columns.tolist():
                                if column_name2 not in double_time_name:
                                    if column_n1 in column_name2.upper():
                                        double_time_name.append(column_name2)
                                        Reconcil_columns_list.append(outer_file[column_name2][out_Email_index])
                                        run_last_if_cond = 1
                                        break
                            if run_last_if_cond == 0:
                                Reconcil_columns_list.append(np.nan)
                                
                        
                       check_list1_ = ["TIMESTAMP","UTR","TITLE","NAME","DESIGNATION",'MAIL','MOBILE','GENDER','COLLEGE',
                                      "WHATSAPP","DEPARTMENT","SEM","CITY","STATE","STATUS",'MODE','PAYEE','CALLING']
                        
                       for check_list_name1 in check_list1_:
                            make_Reconcil_columns_list(check_list_name1)  
                       
                       for fill_Reconcil_index,fill_Reconcil_data in enumerate(Inner_file.columns.tolist()[:-3]):
                           Inner_file.loc[INNa_index,[fill_Reconcil_data]] = Reconcil_columns_list[fill_Reconcil_index]
                    
               else:
                   Reconcil_columns_list = []
                   double_time_name = []
                   def make_Reconcil_columns_list(column_n1):
                        run_last_if_cond = 0
                        for column_name2 in outer_file.columns.tolist():
                            if column_name2 not in double_time_name:
                                if column_n1 in column_name2.upper():
                                    double_time_name.append(column_name2)
                                    Reconcil_columns_list.append(outer_file[column_name2][out_Email_index])
                                    run_last_if_cond = 1
                                    break
                        if run_last_if_cond == 0:
                            Reconcil_columns_list.append(np.nan)
                    
                   check_list1_ = ["TIMESTAMP","UTR","TITLE","NAME","DESIGNATION",'MAIL','MOBILE','GENDER','COLLEGE',
                                  "WHATSAPP","DEPARTMENT","SEM","CITY","STATE","STATUS",'MODE','PAYEE','CALLING']
                    
                   for check_list_name1 in check_list1_:
                        make_Reconcil_columns_list(check_list_name1)
                    
                   dictionary1 = {'Timestamp' : Reconcil_columns_list[0],
                                  'UTR No ( PhonePe)' : Reconcil_columns_list[1],
                                  'Title' : Reconcil_columns_list[2],
                                  'Registered Name' : Reconcil_columns_list[3],
                                  'Designation' : Reconcil_columns_list[4],
                                  'Email ID' : Reconcil_columns_list[5],
                                  'Mobile No.' : Reconcil_columns_list[6],
                                  'Your Gender' : Reconcil_columns_list[7],
                                  'College Name' : Reconcil_columns_list[8],
                                  'Whatsapp No ' : Reconcil_columns_list[9],
                                  'Branch/ Department' : Reconcil_columns_list[10],
                                  'Current Semester' : Reconcil_columns_list[11],
                                  'College City' : Reconcil_columns_list[12],
                                  'State' : Reconcil_columns_list[13],
                                  'Status' : Reconcil_columns_list[14],
                                  'Mode' : Reconcil_columns_list[15],
                                  'Payee Name/New ID' : Reconcil_columns_list[16],
                                  'Calling Responses' : Reconcil_columns_list[17]
                                  }
                   Inner_file = Inner_file.append(dictionary1, ignore_index=True)
           Inner_file.drop_duplicates(subset=['Email ID'], keep='first', inplace=True)
           Inner_file.reset_index(inplace = True, drop = True) 

           Reconcil_dataframe = Inner_file
           return Reconcil_dataframe
           
       
        
        
        
        
        #here we will execute our reconcilation function
        try:
            if not os.path.exists("{}".format(Inside_report_excel)):
               Inside_report_csv = pd.DataFrame(columns=["Timestamp","UTR No ( PhonePe)","Title","Registered Name",
                             "Designation","Email ID","Mobile No.",'Your Gender',"College Name",
                             'Whatsapp No ',"Branch/ Department","Current Semester","College City","State",
                             'Status','Mode','Payee Name/New ID','Calling Responses',
                              'Zoom id','Matched', 'Zoom Name']) 
               Inside_report_csv.to_csv("{}".format(Inside_report_excel), index = False)
               Reconcil_dataframe = Reconcilation_process()
               Reconcil_dataframe.to_csv("{}".format(Inside_report_excel), index = False)
            else:
               Reconcil_dataframe = Reconcilation_process()
               Reconcil_dataframe.to_csv("{}".format(Inside_report_excel), index = False)
                
        except:
            print("Error 5:  Reconcilation Problem")
            sys.exit(1)
            
            
        
        #this is just for count that how many students are registered for perticuler season
        consolated_dataframe = Reconcil_dataframe.copy()
        consolated_dataframe_email_column = []
        for column_name_ in consolated_dataframe.columns.tolist():
            if "MAIL" in column_name_.upper():
                consolated_dataframe_email_column.append(column_name_)
                break
        consolated_dataframe = consolated_dataframe.rename(columns={consolated_dataframe_email_column[0]: 'Email'})
        consolated_dataframe.drop_duplicates(subset=['Email'], keep='first', inplace=True)
        consolated_dataframe.reset_index(inplace = True, drop = True) 
        print("\nTotal Registered for this Season: ",len(consolated_dataframe),'\n')
        
        
    
        #here we will make our connection with our google sheet
        try:
            print('Please wait we are reading master sheet...')
            sheet = client.open("Master").sheet1
        except:
            print('Error 3 : Reading Sheet from Client Problem')
            sys.exit(1)                                                                                      
            
                                                                                              
        #this section will be for Master sheet which have all data
             
        def mac_check_make_Master(): #function for mac and linux c drive cheking and make a master sheet
            try:
                if sheet.acell('A1').value == '':
                    Master_sheet_columns_list = ["Timestamp","UTR No ( PhonePe)","Title","Registered Name",
                             "Designation","Email ID","Mobile No.",'Your Gender',"College Name",
                             'Whatsapp No ',"Branch/ Department","Current Semester","College City","State",
                             'Status','Mode','Payee Name/New ID','Calling Responses',
                              'Zoom id','Matched', 'Zoom Name','Meeting ID']
                    for Master_sheet_columns_index,Master_sheet_columns_name in enumerate(Master_sheet_columns_list):
                        Master_sheet_columns_ind = Master_sheet_columns_index + 1
                        sheet.update_cell(1,Master_sheet_columns_ind,Master_sheet_columns_name)
                Master_sheet_dict = sheet.get_all_values()
                Master_sheet = pd.DataFrame(Master_sheet_dict)
                Master_sheet.columns = Master_sheet.iloc[0]
                Master_sheet.drop(Master_sheet.index[0],inplace=True)
                Master_sheet.reset_index(inplace = True, drop = True) 
                return Master_sheet
            except:
                print("Error 4")
                sys.exit(1)
        
        #according to our system function will be run
        #if Mac or linux or windows our system    
        if using_system == 'Darwin' or using_system == 'Linux' or using_system == 'Windows':                         
            Master_sheet = mac_check_make_Master()
        
    
    
       
        
        try:
            if os.path.exists("{}".format(Inside_report_excel)):
                df4 = Reconcil_dataframe.copy()
                df4.drop_duplicates(subset=[consolated_dataframe_email_column[0]], keep='first', inplace=True)
                df4.reset_index(inplace = True, drop = True)
                df4_copy = df4.copy()
                df4_copy_columns_lst = df4_copy.columns.tolist()

        except:
            print("Error 5:  Registered Excel sheet giving problem.")
            sys.exit(1)      

            
        
        #files_name is just a copy for all csv files
        All_csv_files2 = [check2_file for check2_file in All_csv_files if str(Meeting_id) in check2_file]
        All_csv_files2 = sorted(All_csv_files2)
        logging.warning('After sorted all csv files - %s',All_csv_files2)
        files_name = All_csv_files2
    
            
        
        #here we are choose column names which are usefull for our script
        try:
            df4_column_list = [] 
            def make_main_df4_column_list(df4_column1):
                for column_name in df4.columns.tolist():
                    if df4_column1 in column_name.upper():
                        if column_name not in df4_column_list:
                            df4_column_list.append(column_name)
                            break
                else:
                    df4[df4_column1] = np.nan
                    df4_column_list.append(df4_column1)
                    
            check_list1 = ['NAME','MAIL','GENDER','COLLEGE','WHATSAPP']
            for check_list1_name in check_list1:
                        make_main_df4_column_list(check_list1_name)
        except:
            print("Error 6:  Excel sheet have column problem Please check columns of Excel sheet")
            sys.exit(1)       
        logging.warning('Choosed column list of main meeting id sheet - %s',df4_column_list)
          
        
        
        df4 = df4[df4_column_list]  #set columns which we want
        
        
        df4_column_list2 = df4_column_list.copy()    
            
        df4.columns = ["Name", "Email", "Gender", "College Name", "WhatsApp No."] 
        
        df4_copy.rename(columns = {df4_column_list[0]:'Name',
                                   df4_column_list[1]:'Your Gmail ID',
                                   df4_column_list[2]:'Gender',
                                   df4_column_list[3]:'College Name',
                                   df4_column_list[4]:'WhatsApp No.'}, inplace = True)
        
        df4_column_list = ['Name','Your Gmail ID','Gender','College Name','WhatsApp No.']
        
        #this list contains all days original names
        reports_days_name_list = []  
        
        #for full.csv 
        dataframe_name = []  
            
        #Before updated sheet
        before_updated_day = [] 
        
        
        prt_to_reg = pd.DataFrame(columns=['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.','Zoom id'])
          
        t2 = pd.DataFrame(columns=['Name', 'Email', 'Gender', 'College Name', 'WhatsApp No.'])
    
        
        
    #Main for loop start from here making daywise csv files
        

        file_index = 0
        for file_name in files_name: #main daywise for loop
            
            
              
            File_Name = file_name
            
            file_number = File_Name[4]
            try:
                df1 = pd.read_csv("{}".format(File_Name))
                df1.dropna(axis=1, how='all',inplace=True)
                df1.dropna(how='all',inplace=True)
                df1.reset_index(inplace = True, drop = True)
                df1 = df1[df1.columns.tolist()]
                df1_column_length = len(df1.columns.tolist())
            except:
                print("Error 7:  Daywise file reading Problem occure")
                sys.exit(1)  
            
            if df1_column_length == 3:
                df1.columns = ["Name", "Email", "Time"]
                logging.warning('Day{} Participants data Shape - %s'.format(file_index),df1.shape)
                
            elif df1_column_length == 7:
                if len(df1) > 2:
                    new_header = df1.iloc[1] #grab the first row for the header
                    df1 = df1[2:]#take the data less the header row
                    df1.dropna(axis=1, how='all',inplace=True)
                    df1.columns = list(new_header[:-2])
                    df1.reset_index(inplace = True, drop = True)
                    df1.columns = ["Name","Email","Join","Leave","Time"]
                else:
                    continue
                
            else:
                continue
           
            
            
            
            #this for choosing real participants file where we will do work.
            day_original_name_index = File_Name.index("participants") - 1
            day_original_name = File_Name[:day_original_name_index]
            reports_days_name_list.append(day_original_name)
              
            
            #dataframe set by coosing files
            dataframe_a = "data"+str(file_index)
            dataframe_name.append(dataframe_a)
            
            
            #Before updated sheet by choosing files
            before_updated_day.append(day_original_name)
            
            
            if df1_column_length == 3:
                prt_to_reg = pd.DataFrame(columns=['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.','Zoom id'])
            elif df1_column_length == 7:
                prt_to_reg = pd.DataFrame(columns=['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.','Zoom id','Join','Leave'])
            
            
            def removing(list1):
                SYMBOLS = '{}()[].,:;+-*/&|<>=~' 
                list2 = []
                for element in list1:
                    temp = ""
                    for ch in element:
                        if ch not in SYMBOLS:
                            temp += ch
                
                    list2.append(temp)
                return list2
            
            
            
            df1['Name'] = [name.upper() for name in df1['Name'].tolist()]
            data_list = df1['Name'].tolist()
            df1['Name'] = removing(data_list)
            
            
            
            df1.drop_duplicates(subset='Email',keep='last', inplace=True)
            df1.reset_index(inplace = True, drop = True)
            
            
            df4['Name'] = [name.upper() for name in df4['Name'].tolist()]
            data_list = df4['Name'].tolist()
            df4['Name'] = removing(data_list)
    
            
            
            prt_to_reg["Zoom id"] = np.nan
            
            
            try:
                #Update sheet using master sheet (By Registered Email id)
                Master_sheet_Email_list2 = Master_sheet["Email ID"].values.tolist()
                df4_copy_email_list2 = df4_copy[df4_column_list[1]].values.tolist()
                for df4_copy_email2_index,df4_copy_email2 in enumerate(df4_copy_email_list2):
                    for Master_sheet_Email_index,Master_sheet_Email in enumerate(Master_sheet_Email_list2):
                        if str(df4_copy_email2).upper().strip() in str(Master_sheet_Email).upper().strip():
                            if Master_sheet["Matched"][Master_sheet_Email_index] == 'TRUE':
                                df4_copy.loc[df4_copy_email2_index,"Zoom id"] = Master_sheet["Zoom id"][Master_sheet_Email_index]
                                df4_copy.loc[df4_copy_email2_index,"Matched"] = True
                                df4_copy.loc[df4_copy_email2_index,"Zoom Name"] = Master_sheet["Zoom Name"][Master_sheet_Email_index]
                                break
        #                    else:
        #                        df4_copy.loc[df4_copy_email2_index,"Matched"] = False
        #                        break
                
                #Update sheet using master sheet (By Zoom Email id)
                Master_sheet_zoom_Email_list2 = Master_sheet["Zoom id"].values.tolist()
                df4_copy_email_list3 = df4_copy[df4_column_list[1]].values.tolist()
                for df4_copy_email3_index,df4_copy_email3 in enumerate(df4_copy_email_list3):
                    for Master_zoom_Email_index,Master_zoom_Email in enumerate(Master_sheet_zoom_Email_list2):
                        if str(df4_copy_email3).upper().strip() in str(Master_zoom_Email).upper().strip():
                            df4_copy.loc[df4_copy_email3_index,"Zoom id"] = Master_sheet["Zoom id"][Master_zoom_Email_index]
                            df4_copy.loc[df4_copy_email3_index,"Matched"] = True
                            df4_copy.loc[df4_copy_email3_index,"Zoom Name"] = Master_sheet["Zoom Name"][Master_zoom_Email_index]
                            break
       
            except:
                print("Error 8:  Comparision to Master sheet and inside Report csv Problem")
                sys.exit(1) 
            
            
            zoom_list = df1['Name'].values.tolist()
            zoom_Email_list = df1['Email'].values.tolist()
            data1_list = df4['Name'].values.tolist()
            data1_Email_list = df4['Email'].values.tolist()
            
            
            
            
            #This for our registration data indexing
            store = []
            zoom_store = []
            suspence_store = []
            
            
            
            
            data1_list_filter = list(map(lambda x: x.split(),data1_list))
        
            data1_list_ = []
            for i in data1_list_filter:
                  data1_list_.append(list(filter(lambda x : len(x)>2, i)))
        
            data1_list_filter = list(map(lambda x: " ".join(x),data1_list_))
            
            #this function will check the name from participant to registered data
            def name_checking_func(zoom_name,zoom_index):
                name = zoom_name.split()
                set1 = []
                set2 = []
                n = 0
                while n < len(name):
                    if len(name[n]) > 2:
                        for data1_index, data1_name in enumerate(data1_list):
                            data1_name = data1_name.split() 
                            if name[-1] in data1_name:
                                set2.append(data1_index)
                            if name[n] in data1_name:
                                set1.append(data1_index)
                        break
                    else:
                        n += 1
                set3 = set(set1)
                set4 = set(set2)
                set_intersection = set3.intersection(set4)
                
                if len(set_intersection) > 0:
                    change_list = list(set_intersection)
                    store.append(change_list[0])
                    zoom_store.append(zoom_index)
    #                        f["Zoom id"][zoom_index] = df4["Email"][change_list[0]]
    #                        df4_copy["Zoom id"][change_list[0]] = f['Email'][zoom_index]
                else:
                   suspence_store.append(zoom_index) 
                
            try:
            #data checking from participants to registered.
                for zoom_index, zoom_name in enumerate(zoom_list):
                    counter = 0
                    if "." in str(zoom_Email_list[zoom_index]):
                        for data1_Email_index,data1_Email in enumerate(data1_Email_list):
                            if str(zoom_Email_list[zoom_index]).upper().strip() == str(data1_Email).upper().strip():
                                counter += 1
                                zoom_name = zoom_name.split()
                                zoom_name = " ".join(list(filter(lambda x : len(x)>2, zoom_name)))
                                
                                if data1_list_filter.count(zoom_name) > 1:
                                    suspence_store.append(zoom_index)
                                    break
                                else:
                                    store.append(data1_Email_index)
                                    zoom_store.append(zoom_index)
            #                        f["Zoom id"][zoom_index] = data1_Email
            #                        df4_copy["Zoom id"][data1_Email_index] = data1_Email
                                    break
                        if counter == 0:
                            if str(zoom_Email_list[zoom_index]) in df4_copy['Zoom id'].values.tolist():
                                df_copy_index = df4_copy['Zoom id'].values.tolist().index(str(zoom_Email_list[zoom_index]))
                                store.append(df_copy_index)
                                zoom_store.append(zoom_index)               
                            else:
                                zoom_name = zoom_name.split()
                                zoom_name = " ".join(list(filter(lambda x : len(x)>2, zoom_name)))
                                
                                if data1_list_filter.count(zoom_name) > 1:
                                        suspence_store.append(zoom_index)
                                        
                                else:
                                    name_checking_func(zoom_name,zoom_index)
                                    
            
                                    
                                    
                              
                    else:
                        name_checking_func(zoom_name,zoom_index)
            
            except:
                print("Error 9:  Matching data Participants to Registration file issue.")
                sys.exit(1)
                
                
        
            #If data is matched than student will get present. 
            
            try:
                if df1_column_length == 3:
                    j = 0
                    for i in store:
                        while j < len(zoom_store):
                            value = zoom_store[j]
                            prt_to_reg = prt_to_reg.append({'Zoom Name': df1['Name'][value], 
                                                            'Email': df1['Email'][value], 
                                                            'Time': df1['Time'][value],
                                                            'Registered Name': df4['Name'][i],
                                                            'Gender': df4['Gender'][i],
                                                            'College Name': df4['College Name'][i],
                                                            'WhatsApp No.': df4['WhatsApp No.'][i],
                                                            'Zoom id': df4['Email'][i]}, ignore_index=True)
                            
                            j += 1
                            break
                elif df1_column_length == 7: 
                    j = 0
                    for i in store:
                        while j < len(zoom_store):
                            value = zoom_store[j]
                            prt_to_reg = prt_to_reg.append({'Zoom Name': df1['Name'][value], 
                                                            'Email': df1['Email'][value], 
                                                            'Time': df1['Time'][value],
                                                            'Registered Name': df4['Name'][i],
                                                            'Gender': df4['Gender'][i],
                                                            'College Name': df4['College Name'][i],
                                                            'WhatsApp No.': df4['WhatsApp No.'][i],
                                                            'Zoom id': df4['Email'][i],
                                                            'Join': df1['Join'][value],
                                                            'Leave': df1['Leave'][value]}, ignore_index=True)
                            
                            j += 1
                            break
                    
                prt_to_reg.drop_duplicates(subset='Email',keep='last', inplace=True)
            
            except:
                print("Error 10:  Something is wrong when we are fill the present data.")
                sys.exit(1)
            
            
            
            #code for update excel sheet
            prt_to_reg_zoom_id_list = prt_to_reg["Zoom id"].tolist()
            prt_to_reg_Email_list = prt_to_reg["Email"].tolist()
            df4_copy_email_list = df4_copy[df4_column_list[1]].tolist()
            
            for prt_to_reg_zoom_id_index,prt_to_reg_zoom_id_email in enumerate(prt_to_reg_zoom_id_list):
                for df4_copy_email_index,df4_copy_email in enumerate(df4_copy_email_list):
                    if prt_to_reg_zoom_id_email == df4_copy_email:
                        df4_copy.loc[df4_copy_email_index,"Zoom id"] = prt_to_reg["Email"][prt_to_reg_zoom_id_index]
                        df4_copy.loc[df4_copy_email_index,"Matched"] = True
                        df4_copy.loc[df4_copy_email_index,"Zoom Name"] = prt_to_reg["Zoom Name"][prt_to_reg_zoom_id_index]
                        break
            
          
            
            try:
            
                suspence_t1 = []
                
                for index in suspence_store:
                    suspence_t1.append(df1.iloc[index,])
                
                suspence_t1 = pd.DataFrame(suspence_t1)
                suspence_t1 = suspence_t1.sort_values("Time", ascending = False)
                suspence_t1.reset_index(inplace = True, drop = True)
                
                #work for all suspence data
                if  file_index == 0:
                    t1 = suspence_t1
                else:
                    t1 = t1.merge(right = suspence_t1, how = "outer", on = "Email", suffixes=('', '_Reg{}'.format(file_index)) )
                
            except:
                print("Error 11:  suspense t1 by participants to registration.")
                sys.exit(1)
            
            #===============================================================
            
            
            
            #Now work for check data excel to participants and finding t2 suspence data 
            
            data1_list = df4['Name'].values.tolist()
            data1_Email_list = df4['Email'].values.tolist()
            zoom_list = df1['Name'].values.tolist()
            zoom_Email_list = df1['Email'].values.tolist()
            
            
            
            #filtering the zoom data 
            zoom_list_filter = list(map(lambda x: x.split(),zoom_list))
            zoom_list_ = []
            for i in zoom_list_filter:
                  zoom_list_.append(list(filter(lambda x : len(x)>2, i)))
            zoom_list_filter = list(map(lambda x: " ".join(x),zoom_list_))
            
            
            try:
            
                suspence_store_t2 = []
                
                def name_cheking_t2(data1_name,name_cheking_t2):
                    data1_name = data1_name.split()
                    data1_name = " ".join(list(filter(lambda x : len(x)>2, data1_name)))
                    if zoom_list_filter.count(data1_name) > 1:
                        suspence_store_t2.append(data1_index)
                            
                    else:
                        name = data1_name.split()
                        set1 = []
                        set2 = []
                        n = 0
                        while n < len(name):
                            if len(name[n]) > 2:
                                for zoom_index, zoom_name in enumerate(zoom_list):
                                    zoom_name = zoom_name.split() 
                                    if name[-1] in zoom_name:
                                        set2.append(zoom_index)
                                    if name[n] in zoom_name:
                                        set1.append(zoom_index)
                                break
                            else:
                                n += 1
                        set3 = set(set1)
                        set4 = set(set2)
                        set_intersection = set3.intersection(set4)
                        
                        if len(set_intersection) > 0:
                            pass
        
                        else:
                           suspence_store_t2.append(data1_index) 
                                   
                def data1_name_func(data1_name):
                    data1_name = data1_name.split()
                    data1_name = " ".join(list(filter(lambda x : len(x)>2, data1_name)))
                    return data1_name
                
                for data1_index, data1_name in enumerate(data1_list):
                    if "." in str(data1_Email_list[data1_index]):
                        for zoom_Email_index,zoom_Email in enumerate(zoom_Email_list):
                            if str(data1_Email_list[data1_index]).upper().strip() == str(zoom_Email).upper().strip():
                                data1_name = data1_name_func(data1_name)
                                
                                if zoom_list_filter.count(data1_name) > 1:
                                    suspence_store_t2.append(data1_index)
                                    break
                                else:
        
                                    break
                                      
                        else:
                            suspence_store_t2.append(data1_index) 
                            
                    else:
                        name_cheking_t2(data1_name,name_cheking_t2)
                
                
                
                
                #making dataframe for t2
                suspence_t2 = []
                
                for index in suspence_store_t2:
                    suspence_t2.append(df4.iloc[index,])
                
                suspence_t2 = pd.DataFrame(suspence_t2)
                suspence_t2.reset_index(inplace = True, drop = True)  
            
            except:
                print("Error 12:  suspense t2 by registration to participants to problem.")
                sys.exit(1)
            
            
            try:
            #daywise suspence data
                def suspence_merge_data():
                    if df1_column_length == 3:
                        merge = pd.merge(suspence_t1, suspence_t2, how='outer', on='Email')
                        merge = merge[['Name_x', 'Email', 'Time', 'Name_y', 'Gender', 'College Name', 'WhatsApp No.']]
                        merge.columns = ['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.']
                        merge["Zoom id"] = np.nan
                        return merge
                    elif df1_column_length == 7:
                        merge = pd.merge(suspence_t1, suspence_t2, how='outer', on='Email')
                        merge = merge[['Name_x', 'Email', 'Time', 'Name_y', 'Gender', 'College Name', 'WhatsApp No.','Join','Leave']]
                        merge.columns = ['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.','Join','Leave']
                        merge["Zoom id"] = np.nan
                        merge = merge[['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.','Zoom id','Join','Leave']]
                        return merge
            
            except:
                print("Error 13:  Union of both suspence t1 and suspence t2 part occure.")
                sys.exit(1)
        
            try:
            #Daywise present data
                def present_data(prt_to_reg):
                    prt_to_reg = prt_to_reg.sort_values("Time", ascending = False)
                    prt_to_reg.reset_index(inplace = True, drop = True) 
                    
                    prt_to_reg = prt_to_reg.append(pd.Series("nan"), ignore_index=True)
                    prt_to_reg = prt_to_reg.drop([0],axis=1) 
                    new_row={"Zoom Name":"Suspense","Email":"Data"}
                    prt_to_reg = prt_to_reg.append(new_row,ignore_index=True)   
                    return prt_to_reg
            except:
                print("Error 14: taking Present data from daywise problem.")
                sys.exit(1)
            
            
            try:
            #for full.csv
                my_copy = present_data(prt_to_reg)[:-2].copy()
                dataframe_name[file_index] = my_copy
                dataframe_name[file_index] = dataframe_name[file_index][["Zoom Name","Zoom id","Time"]]
                dataframe_name[file_index].columns = ["Name", "Zoom id", "Time"]
                dataframe_name[file_index].loc[:,"Date"] = file_index+1
            except:
                print("Error 15: taking Present data from daywise problem.")
                sys.exit(1)
            
            
            frame=[present_data(prt_to_reg),suspence_merge_data()]
            result=pd.concat(frame)
            result.reset_index(inplace = True, drop = True)
            logging.warning('Day{} shape(present & suspence) - %s'.format(file_index),result.shape)
            #Now we will just store the result data in --> before_updated_day
            before_updated_day[file_index] = result
            file_index += 1
         
                 
           
        df4_copy["Matched"] = df4_copy["Matched"].fillna(False)
            
        
        #Now code for creating daywise file and seprate the absent section
        create_daywise = [] 
        
        for day_index in range(len(reports_days_name_list)):
            null_index1 = before_updated_day[day_index][before_updated_day[day_index]["Zoom Name"].isnull()].index.tolist()[0]
            null_index2 = before_updated_day[day_index][before_updated_day[day_index]["Zoom Name"].isnull()].index.tolist()[1]
            
            try:
            #Present data
                def only_present_data(day_index,null_index1):
                    present_data = before_updated_day[day_index].iloc[:null_index1,]
                    present_data.drop_duplicates(subset=["Zoom id"], keep='first', inplace=True)
                    present_data.reset_index(inplace = True, drop = True)
                    for emp_email_index in range(len(present_data)):
                        if type(present_data["Email"][emp_email_index]) == float:
                            present_data["Email"][emp_email_index] = present_data["Zoom id"][emp_email_index]
                    present_data = present_data.append(pd.Series("nan"), ignore_index=True)
                    present_data = present_data.drop([0],axis=1) 
                    new_row={"Zoom Name":"Suspense","Email":"Data"}
                    present_data = present_data.append(new_row,ignore_index=True)
                    return present_data
                present_data = only_present_data(day_index,null_index1)
            
            except:
                print("Error 16: Selecting all Present data problem.")
                sys.exit(1)
            
            logging.warning('Day{} only present data shape- %s'.format(day_index),present_data.shape)
            
            try:
                #unregistered section
                t1_suspence = before_updated_day[day_index].iloc[null_index1+2 : null_index2,]
                t1_suspence.dropna(subset=['Zoom Name', 'Email','Time'],inplace=True)
                t1_suspence.drop_duplicates(subset=["Email"], keep='first', inplace=True)
                t1_suspence = t1_suspence.sort_values("Time", ascending = False)
                t1_suspence.reset_index(inplace = True, drop = True)
                column_length = len(t1_suspence.columns.tolist())
                
                #with this data we will seprate absent data
                t2_suspence = before_updated_day[day_index].iloc[null_index2 : ,]
                
                
                df4_copy_Email_list = df4_copy[df4_column_list[1]].values.tolist()
                t2_suspence_Email_list = t2_suspence['Email'].values.tolist() 
                
                t2_real_suspence = []
                t2_absent = []
                
                for t2_suspence_index,t2_suspence_Email in enumerate(t2_suspence_Email_list):
                    if str(t2_suspence_Email) not in present_data["Zoom id"].values.tolist():
                        for df4_copy_index,df4_copy_Email in enumerate(df4_copy_Email_list):
                            if t2_suspence_Email == df4_copy_Email:
                                if df4_copy["Matched"][df4_copy_index] == True:
                                    t2_absent.append(t2_suspence.iloc[t2_suspence_index,])
                                else:
                                    t2_real_suspence.append(t2_suspence.iloc[t2_suspence_index,])
            
                #this for suspence_t2
                
                if len(t2_real_suspence) == 0:
                    if column_length == 8:
                        t2_real_suspence = pd.DataFrame(columns=['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.','Zoom id'])
                        t2_real_suspence.reset_index(inplace = True, drop = True)
                    elif column_length == 10:
                        t2_real_suspence = pd.DataFrame(columns=['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.','Zoom id','Join','Leave'])
                        t2_real_suspence.reset_index(inplace = True, drop = True)
                else:
                    t2_real_suspence = pd.DataFrame(t2_real_suspence)
                    t2_real_suspence.drop_duplicates(subset=["Email"], keep='first', inplace=True)
                    t2_real_suspence.reset_index(inplace = True, drop = True)
            
                #copy of t2_real_suspence for all suspence
                t2_real_suspence_copy = t2_real_suspence.copy()
            
            
                #daywise suspence data
                def real_suspence_data_merge():
                    merge = pd.merge(t1_suspence, t2_real_suspence, how='outer', on='Email')
                    if column_length == 8:
                        merge = merge[['Zoom Name_x', 'Email', 'Time_x', 'Registered Name_y', 'Gender_y', 'College Name_y', 'WhatsApp No._y','Zoom id_y']]
                        merge.columns = ['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.','Zoom id']
                    elif column_length == 10:
                         merge = merge[['Zoom Name_x', 'Email', 'Time_x', 'Registered Name_y', 'Gender_y', 'College Name_y', 'WhatsApp No._y','Zoom id_y','Join_x','Leave_x']]
                         merge.columns = ['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.','Zoom id','Join','Leave']
                  
                        
                    #add a nun row for absent data
                    merge = merge.append(pd.Series("nan"), ignore_index=True)
                    merge = merge.drop([0],axis=1) 
                    new_row={"Zoom Name":"Absent","Email":"Data"}
                    merge = merge.append(new_row,ignore_index=True)
                    return merge
                logging.warning('Day{} only Suspence data shape- %s'.format(day_index),real_suspence_data_merge().shape)
            
           
            
                #this for Absent data
                def t2_absent_func(t2_absent):
                    t2_absent = pd.DataFrame(t2_absent)
                    t2_absent.reset_index(inplace = True, drop = True)
                    t2_absent["Zoom Name"] = np.nan
                    t2_absent["Time"] = np.nan
                    t2_absent.drop_duplicates(subset=["Email"], keep='first', inplace=True)
                    t2_absent.reset_index(inplace = True, drop = True)
                    return t2_absent
                
                if len(t2_absent) == 0:
                    if column_length == 8:
                        t2_absent = pd.DataFrame(columns=['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.','Zoom id'])
                    elif column_length == 10:
                        t2_absent = pd.DataFrame(columns=['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.','Zoom id','Join','Leave'])
                else:
                    t2_absent = t2_absent_func(t2_absent)
                
            except:
                print("Error 17: Distributed Real suspence data and absent data daywise error.")
                sys.exit(1)
            
            try:
                logging.warning('Day{} only Absent data shape- %s'.format(day_index),t2_absent_func(t2_absent).shape)
                #work for all suspence data
                real_suspence = t2_real_suspence_copy[['Registered Name', 'Email', 'Gender', 'College Name', 'WhatsApp No.']]   
                real_suspence.columns = ['Name','Email','Gender','College Name','WhatsApp No.']
                t2 = t2.append(real_suspence) 
                                   
            
                daywise_frame = [present_data,real_suspence_data_merge(),t2_absent]
                daywise_result = pd.concat(daywise_frame)
                daywise_result.reset_index(inplace = True, drop = True)
                
                create_daywise.append(reports_days_name_list[day_index])
                dfff_index = daywise_result[daywise_result["Registered Name"].isnull()].index.tolist()[0]
                create_daywise[day_index] = daywise_result.iloc[:dfff_index,]

                daywise_result = daywise_result[['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.','Zoom id']]
                
            except:
                print("Error 18: Concatenating of present data, suspence data and absent data daywise.")
                sys.exit(1)
            #this number will print on daywise file name
            
#            daynumber = (int(file_number) - int(File_Total)) + (day_index+1)
            
            daywise_result.to_csv("Reports/{}.csv".format(reports_days_name_list[day_index]), index = False)
        
      
        
        
    #till here we have completed our daywise data 
    #=============================================================
    #from here we will generate 4 extra details files
        
    
             
        #code for suspence data
        try:
            t1.dropna(subset=['Email'], inplace=True)
            t1.reset_index(inplace = True, drop = True) 
            
            def unique_name_list():
                t1_name_column = []
                for t1_name in t1.columns.tolist():
                    if "Name" in t1_name:
                        t1_name_column.append(t1_name)
                
                name_list = []
                for i in range(t1.shape[0]):    
                     a = t1.loc[i,t1_name_column].tolist()   
                     cleanedList = [x for x in a if str(x) != 'nan']
                     name_list.append(cleanedList[0])
                return name_list
            
            
            name_list = unique_name_list() #using function unique_name_list()
        
        except:
                print("Error 19(part 1): Generating all Suspnce data error")
                sys.exit(1)
                
         
        try:
        #t1 function columns
            def columns_name_list(name_list):
                t1["Name_column"] = name_list
                t1_name_column2 = ["Name_column"]
                
                t1_name_column2.append("Email")
                t1_time_column = []
                for t1_time in t1.columns.tolist():
                    if "Time" in t1_time:
                        t1_time_column.append(t1_time)
                
                t1_column = t1_name_column2+t1_time_column
                return t1_column,t1_time_column
            
            t1_column,t1_time_column = columns_name_list(name_list)  #used the function columns_name_list(name_list)
            
            t1 = t1[t1_column] 
            t1["Total"] = np.nan
            t1 = t1.fillna(0)
        
        except:
                print("Error 19(part 2): Generating all Suspnce data error")
                sys.exit(1)
        
        try:
        #now we will count that how many days exist our scipt
            def days_count_func():
                day_count = ["Zoom Name","Email"]
                for day_index in range(len(t1_time_column)):
                    day_count.append("{}".format(reports_days_name_list[day_index]))
                
                day_count.append("Total")
                return day_count
            t1.columns = days_count_func()
            
            
            
            t1["Total"] = 0
            for daywise_index in range(len(t1_time_column)):
                time_integer  = [(lambda x: int(x))(x) for x in t1["{}".format(reports_days_name_list[daywise_index])].tolist()]
#                t1["{}".format(reports_days_name_list[daywise_index])] = list(lambda a: int(a),t1["{}".format(reports_days_name_list[daywise_index])].tolist())
#                t1["{}".format(reports_days_name_list[daywise_index])] =pd.Series(time_integer) 
                t1["Total"] += pd.Series(time_integer)
            
            t1 = t1.sort_values("Total", ascending = False)
            t1.dropna(subset=['Email'],inplace=True)
            t1.reset_index(inplace = True, drop = True)
            
            
            t2.drop_duplicates(subset=["Email"], keep='first', inplace=True)
        
        except:
                print("Error 19(part 3): Generating all Suspnce data error")
                sys.exit(1)
        
        try:        
            #using this function we will generate all suspence entries and use every section
            def all_suspence_data(t1,t2):
                suspence_merge = pd.merge(t1,t2, how='outer', on='Email')
                suspence_merge_list = ['Name', 'Gender', 'College Name', 'WhatsApp No.','Zoom Name','Email']
                suspence_merge_list = suspence_merge_list + t1.columns.tolist()[2:]
                suspence_merge = suspence_merge[suspence_merge_list]  #now we will add this data into everyday and atleast present
                return suspence_merge    
            
            suspence_merge = all_suspence_data(t1,t2)  #using all_suspence_data(t1,t2) function
        except:
                print("Error 19(part 4): Generating all Suspnce data error")
                sys.exit(1)
                
        logging.warning('Total suspence shape- %s',suspence_merge.shape) 
        
        
        
        
        
        
        
        #========================
        #work start for full.csv
        
        
        
            
        df4 = df4.rename(columns={'Email': 'Zoom id'})
        
        
        
        try:
            #every day present
            def make_zoom(dataframe_name):
                zoom = pd.concat(dataframe_name)
                #Deleting the columns with no value
                zoom = zoom.dropna(how = "all")
                zoom.reset_index(inplace = True, drop = True)     
                return zoom
            
            zoom = make_zoom(dataframe_name) #using make_zoom(dataframe_name) function here
                
            emails = zoom["Zoom id"].tolist()
        
        except:
                print("Error 20(part 1): Generating Everyday present data error")
                sys.exit(1)
        
        try:
            def Dates_indexing():
                ats = []
                for at_index in range(1,(len(reports_days_name_list)+1)):
                    b = "at" + str(at_index)
                    ats.append(b)
                return ats
            
            ats = Dates_indexing()
                
            index = 0
            while index < len(reports_days_name_list):
                ats[index] = [0] * len(emails)
                index += 1
            
            
            
            zoom_names = zoom["Name"].tolist()
            zoom_durations = zoom["Time"].tolist()
            zoom_dates = zoom["Date"].tolist()
            
            
            for dates_index in range(1,(len(reports_days_name_list)+1)):
                for index,name in enumerate(zoom_names): 
                    for zindex, zname in enumerate(zoom_names):
                        if str(name) in str(zname):
                            if zoom_dates[zindex] == dates_index:
                                ats[(dates_index-1)][index] = zoom_durations[zindex]
                
            
                   
            
            total = [0] * len(zoom_names)
            
            
            
            for index,name in enumerate(zoom_names):
                  index_at = 0
                  while index_at < len(reports_days_name_list):
                       if index_at == 0:
                            total[index] = int(ats[index_at][index]) 
                       elif index_at > 0:
                            total[index] += int(ats[index_at][index])
                       index_at += 1
             
                      
            
            ats.insert(0, zoom_names)
            ats.insert(1, emails)
            cal = 2 + len(reports_days_name_list)
            ats.insert(cal, total)
            #z is a dataframe which have our compelete days total time (we need to transpose of dataset here)
            z = pd.DataFrame(ats)
        
        except:
                print("Error 20(part 2): Generating Everyday present data error")
                sys.exit(1)
        
        
        try:
            #transpose of our dataset
            def datafram_transpose(z):
                z = z.T  #transpose the dataframe
                return z
            
            z = datafram_transpose(z) #using datafram_transpose(z) function
            
            
            #z dataframe not have column names so we will give here names
            def z_columns_list():
                column_list = ["Zoom Name", "Email"]
                for column_list_index in range(len(reports_days_name_list)):
                    day_name = "{}".format(reports_days_name_list[column_list_index])
                    column_list.append(day_name)
                
                column_list.append("Total")
                return column_list
            
            z.columns = z_columns_list()  #using z_columns_list() function
            
            
            z.drop_duplicates(inplace = True) #z dataframe have a lot of duplicate queries so we need to remove it
            z.reset_index(inplace = True, drop = True)    #reset the rows indexing
               
            
             
            z = z.rename(columns={'Email': 'Zoom id'})
            #final dataframe have more matching detail of participants
            final = z.merge(right = df4, how = "left", on = "Zoom id", suffixes=('', 'Registered'))
        
        except:
                print("Error 20(part 3): Generating Everyday present data error")
                sys.exit(1)
        
        try:
            def final_dataframe_column_list():
                final_list = ['Name', 'Gender', 'College Name', 'WhatsApp No.','Zoom Name', 'Zoom id']
                for final_list_index in range(len(reports_days_name_list)):
                    day_name = "{}".format(reports_days_name_list[final_list_index])
                    final_list.append(day_name)
                
                final_list.append("Total")
                return final_list
            
            
            final = final[final_dataframe_column_list()]
            
            final = final.sort_values("Total", ascending = False) #sorting of total column
            
            final_copy = final.copy()  #this copy will be most use for "Reports/Not_present_any_day.csv"
         
        except:
                print("Error 20(part 4): Generating Everyday present data error making final dataframe")
                sys.exit(1)  
            
        
        
        
        
        try:
            #atleast one day present data
            def prepare1_Atleast_one_day():  #step1
                Atleast_one_day = final.copy()  
                Atleast_one_day.drop_duplicates(subset=["Zoom id"], keep='first', inplace=True)
                Atleast_one_day.reset_index(inplace = True, drop = True) 
                
                Atleast_one_day = Atleast_one_day.rename(columns={'Zoom id': 'Email'})
                Atleast_one_day = Atleast_one_day.rename(columns={'Name': 'Original_Name'})
                return Atleast_one_day
            
            Atleast_one_day = prepare1_Atleast_one_day()
            logging.warning('prepare1_Atleast_one_day shape- %s',Atleast_one_day.shape)
        
        except:
                print("Error 21(part 1): Generating Atleast One Day data error")
                sys.exit(1) 
         
        try:
            #here we will make second step for Atleast_one_day
            def prepare2_Atleast_one_day(Atleast_one_day):   #step2
                original_copy = df4_copy.copy()   #this is for original name
                original_copy = original_copy.rename(columns={df4_column_list[1]: 'Email'})
                Atleast_one_day = Atleast_one_day.merge(right = original_copy, how = "inner", on = "Email", suffixes=('', '_Reg') )
                return Atleast_one_day
            
            Atleast_one_day = prepare2_Atleast_one_day(Atleast_one_day)
            logging.warning('prepare2_Atleast_one_day shape- %s',Atleast_one_day.shape)
            
            def Atleast_one_day_column_list():
                Atleast_one_day_list = ['{}'.format(df4_column_list[0]), 'Gender', 'College Name', 'WhatsApp No.','Zoom Name', 'Email']
                for Atleast_list_index in range(len(reports_days_name_list)):
                    At_day_name = "{}".format(reports_days_name_list[Atleast_list_index])
                    Atleast_one_day_list.append(At_day_name)
                
                Atleast_one_day_list.append("Total")
                return Atleast_one_day_list
            logging.warning('Atleast one day column list - %s',Atleast_one_day_column_list())    
            
            #choose columns according to our need
            Atleast_one_day = Atleast_one_day[Atleast_one_day_column_list()] #using Atleast_one_day_column_list() function 
          
        except:
                print("Error 21(part 2): Generating Atleast One Day data error")
                sys.exit(1)
        
        try:
            #Now we will add suspence section in atleast one day
            def prepare3_Atleast_one_day(Atleast_one_day): #step3 
                Atleast_one_day=Atleast_one_day.append(pd.Series("nan"), ignore_index=True)
                Atleast_one_day=Atleast_one_day.drop([0],axis=1) 
                new_row={df4_column_list[0]:"Suspense","Gender":"Data"}
                Atleast_one_day = Atleast_one_day.append(new_row,ignore_index=True) 
                
                Atleast_one_day = Atleast_one_day.rename(columns={df4_column_list[0]:'Name'})
                return Atleast_one_day
            
            logging.warning('Complete_Atleast_one_day shape- %s',prepare3_Atleast_one_day(Atleast_one_day).shape)
            
            frame2 = [prepare3_Atleast_one_day(Atleast_one_day),suspence_merge] #using prepare3_Atleast_one_day(Atleast_one_day) function 
            Atleast_one_day = pd.concat(frame2)
            Atleast_one_day.reset_index(inplace = True, drop = True)
        
        except:
                print("Error 21(part 3): Generating Atleast One Day data error")
                sys.exit(1)
                
        Atleast_one_day.to_csv("Reports/Atleast_one_day_present.csv", index = False)    
            
         
             
        
        
        
        try:     
            #code for everyday present who are register and join every day  
            def everyday_present(final):   
                #This line use for hiding all pandas warnings
                pd.options.mode.chained_assignment = None
                for last_index in range(len(reports_days_name_list)):
                    final.reset_index(inplace = True, drop = True)
                    time_integer2  = [(lambda x: int(x))(x) for x in final["{}".format(reports_days_name_list[last_index])].tolist()]
                    final = final[(pd.Series(time_integer2) > 0)]
                    final.reset_index(inplace = True, drop = True)
                    
                final.drop_duplicates(subset=["Zoom id"], keep='first', inplace=True)
                final.reset_index(inplace = True, drop = True)    
                    
                final = final.rename(columns={'Zoom id': 'Email'})
                
                #Now we will add suspence section in every daya present
                final = final.append(pd.Series("nan"), ignore_index=True)
                final = final.drop([0],axis=1) 
                new_row = {'Name':"Suspense","Gender":"Data"}
                final = final.append(new_row,ignore_index=True) 
                return final
            logging.warning('Everyday present data shape- %s',everyday_present(final).shape)
            
            frame3 = [everyday_present(final),suspence_merge]  #using everyday_present(final) here
            final = pd.concat(frame3)
            final.reset_index(inplace = True, drop = True)
            
        except:
                print("Error 22 : creating file of Every day present problem")
                sys.exit(1)
        final.to_csv("Reports/Full_data_present_everyday.csv", index = False)    
            
            
            
            
            
            
            
        #Code start for No_present.csv 
        def prepare1_not_present(): #step1
            final_copy.drop_duplicates(subset=["Zoom id"], keep='first', inplace=True) 
            final_work = final_copy.merge(right = df4, how = "outer", on = "Zoom id", suffixes=('', '_Reg') )
            final_work = final_work[final_work['Zoom Name'].isnull()]
            return final_work
        logging.warning('prepare1 not present Any day Shape - %s',prepare1_not_present().shape)
        
        final_work = prepare1_not_present()
        
        
        #choose the column names according to our need
        def not_present_column_list():
            final_work_list = ['Name_Reg','Gender_Reg', 'College Name_Reg', 'WhatsApp No._Reg','Zoom Name','Zoom id']
            for final_list_index in range(len(reports_days_name_list)):
                final_day_name = "{}".format(reports_days_name_list[final_list_index])
                final_work_list.append(final_day_name)
            final_work_list.append("Total")
            return final_work_list
        logging.warning('Column names of Not present data - %s',not_present_column_list())
        
        final_work = final_work[not_present_column_list()]
        
        #we need to rename our column names
        final_work = final_work.rename(columns={'Name_Reg': 'Name',
                                                'Gender_Reg': 'Gender',
                                                'College Name_Reg': 'College Name',
                                                'WhatsApp No._Reg': 'WhatsApp No.',
                                                'Name_Reg': 'Name',
                                                'Zoom id': 'Email'})
        
        def prepare2_not_present(final_work):
            final_work = final_work.append(pd.Series("nan"), ignore_index=True)
            final_work = final_work.drop([0],axis=1) 
            new_row = {'Name':"Suspense","Gender":"Data"}
            final_work = final_work.append(new_row,ignore_index=True) 
            return final_work
        logging.warning('Complete data not present Any day Shape - %s',prepare2_not_present(final_work).shape)
        
        frame4 = [prepare2_not_present(final_work),suspence_merge]
        final_work = pd.concat(frame4)
        final_work.reset_index(inplace = True, drop = True)
        final_work.to_csv("Reports/Not_present_any_day.csv", index = False) #not present ant dat dataframe 
        
        
        
        
        #updated excel sheet
        if os.path.exists("{}".format(Inside_report_excel)):
            df4_copy.columns = df4_copy_columns_lst
        else:
            df4_copy.columns = df4_copy_columns_lst + ['Zoom id','Matched','Zoom Name']
        df4_copy.to_csv("{}".format(Inside_report_excel), index = False)
        df4_copy.rename(columns = {df4_column_list2[0]:'Name',
                                   df4_column_list2[1]:'Your Gmail ID',
                                   df4_column_list2[2]:'Gender',
                                   df4_column_list2[3]:'College Name',
                                   df4_column_list2[4]:'WhatsApp No.'}, inplace = True)
        
        
        
        
        #this part for true entris which are true in df4_copy but false in master sheet
        upper_list3 = [x.upper().strip() if type(x) == str else x for x in Master_sheet["Email ID"].values.tolist()]
        df4_copy_email_upper = [y.upper().strip() if type(y) == str else y for y in df4_copy[df4_column_list[1]].values.tolist()]
        df4_copy_zoom_upper = [r.upper().strip() if type(r) == str else r for r in df4_copy["Zoom id"].values.tolist()]
        for upper_list3_index,upper_list3_email in enumerate(upper_list3):
            if Master_sheet['Matched'][upper_list3_index] == 'FALSE':
                if upper_list3_email in df4_copy_email_upper:
                    match_index1 = df4_copy_email_upper.index(upper_list3_email)
                    if df4_copy["Matched"][match_index1] == True:
                        Master_sheet['Zoom id'][upper_list3_index] = df4_copy["Zoom id"][match_index1]
                        Master_sheet['Matched'][upper_list3_index] = True
                        Master_sheet['Zoom Name'][upper_list3_index] = df4_copy["Zoom Name"][match_index1]
                elif upper_list3_email in df4_copy_zoom_upper:
                    match_index1 = df4_copy_zoom_upper.index(upper_list3_email)
                    if df4_copy["Matched"][match_index1] == True:
                        Master_sheet['Zoom id'][upper_list3_index] = df4_copy["Zoom id"][match_index1]
                        Master_sheet['Matched'][upper_list3_index] = True
                        Master_sheet['Zoom Name'][upper_list3_index] = df4_copy["Zoom Name"][match_index1]
        
        
    
        #if utr no or payment details are in df4_copy and we want in master sheet 
        for upper_list3_index,upper_list3_email in enumerate(upper_list3):
                if upper_list3_email in df4_copy_email_upper:
                    match_index1 = df4_copy_email_upper.index(upper_list3_email)
                    if df4_copy["UTR No ( PhonePe)"][match_index1] != '':
                        for df4_copy_UTR_index,df4_copy_UTR_column in enumerate(df4_copy.columns.tolist()):
                            Master_sheet[Master_sheet.columns.tolist()[df4_copy_UTR_index]][upper_list3_index] = df4_copy[df4_copy_UTR_column][match_index1]
                        
                elif upper_list3_email in df4_copy_zoom_upper:
                    match_index1 = df4_copy_zoom_upper.index(upper_list3_email)
                    if df4_copy["UTR No ( PhonePe)"][match_index1] != '':
                        for df4_copy_UTR_index,df4_copy_UTR_column in enumerate(df4_copy.columns.tolist()):
                            Master_sheet[Master_sheet.columns.tolist()[df4_copy_UTR_index]][upper_list3_index] = df4_copy[df4_copy_UTR_column][match_index1]
                        
    
        #Master sheet                  
        #Add the data in Master sheet (if we have new data)
        Matching_data = df4_copy.copy()
        Matching_data.reset_index(inplace = True, drop = True)
        Matching_data_email_list = Matching_data[df4_column_list[1]].values.tolist()
        upper_list = [x.upper().strip() if type(x) == str else x for x in Master_sheet["Email ID"].values.tolist()]
        upper_list2 = [z.upper().strip() if type(z) == str else z for z in Master_sheet["Zoom id"].values.tolist()]
        row_inc = 0
        for Matching_data_email_index,Matching_data_email in enumerate(Matching_data_email_list):
            if Matching_data["Matched"][Matching_data_email_index] == True:
                if str(Matching_data_email).upper().strip() not in upper_list and str(Matching_data_email).upper().strip() not in upper_list2 and str(Matching_data["Zoom id"][Matching_data_email_index]).upper().strip() not in upper_list and str(Matching_data["Zoom id"][Matching_data_email_index]).upper().strip() not in upper_list2:                                                                       
                    
                    Master_columns_list = []
                    def make_Master_columns_list(column_n):
                        for column_name1 in df4_copy.columns.tolist():
                            if column_n in column_name1.upper():
                                Master_columns_list.append(Matching_data[column_name1][Matching_data_email_index])
                                break
                        else:
                            Master_columns_list.append(np.nan)
                    
                    check_list_ = ["TIMESTAMP","UTR","TITLE","NAME","DESIGNATION",'MAIL','MOBILE','GENDER','COLLEGE',
                                  "WHATSAPP","DEPARTMENT","SEM","CITY","STATE","STATUS",'MODE','PAYEE','CALLING',
                                  'ZOOM ID','MATCHED','ZOOM NAME']
                    for check_list_name in check_list_:
                        make_Master_columns_list(check_list_name)
                    
                    dictionary = {'Timestamp' : Master_columns_list[0],
                                  'UTR No ( PhonePe)' : Master_columns_list[1],
                                  'Title' : Master_columns_list[2],
                                  'Registered Name' : Master_columns_list[3],
                                  'Designation' : Master_columns_list[4],
                                  'Email ID' : Master_columns_list[5],
                                  'Mobile No.' : Master_columns_list[6],
                                  'Your Gender' : Master_columns_list[7],
                                  'College Name' : Master_columns_list[8],
                                  'Whatsapp No ' : Master_columns_list[9],
                                  'Branch/ Department' : Master_columns_list[10],
                                  'Current Semester' : Master_columns_list[11],
                                  'College City' : Master_columns_list[12],
                                  'State' : Master_columns_list[13],
                                  'Status' : Master_columns_list[14],
                                  'Mode' : Master_columns_list[15],
                                  'Payee Name/New ID' : Master_columns_list[16],
                                  'Calling Responses' : Master_columns_list[17],
                                  'Zoom id' : Master_columns_list[18],
                                  'Matched' : Master_columns_list[19],
                                  'Zoom Name' : Master_columns_list[20],
                                  'Meeting ID' : ''
                                  }
                    Master_sheet = Master_sheet.append(dictionary, ignore_index=True)
            else:
                if str(Matching_data_email).upper().strip() not in upper_list and str(Matching_data_email).upper().strip() not in upper_list2:                                                                       
                
                    Master_columns_list = []
                    def make_Master_columns_list(column_n):
                        for column_name1 in df4_copy.columns.tolist():
                            if column_n in column_name1.upper():
                                Master_columns_list.append(Matching_data[column_name1][Matching_data_email_index])
                                break
                        else:
                            Master_columns_list.append(np.nan)
                    
                    check_list_ = ["TIMESTAMP","UTR","TITLE","NAME","DESIGNATION",'MAIL','MOBILE','GENDER','COLLEGE',
                                  "WHATSAPP","DEPARTMENT","SEM","CITY","STATE","STATUS",'MODE','PAYEE','CALLING',
                                  'ZOOM ID','MATCHED','ZOOM NAME']
                    for check_list_name in check_list_:
                        make_Master_columns_list(check_list_name)
                    
                    dictionary = {'Timestamp' : Master_columns_list[0],
                                  'UTR No ( PhonePe)' : Master_columns_list[1],
                                  'Title' : Master_columns_list[2],
                                  'Registered Name' : Master_columns_list[3],
                                  'Designation' : Master_columns_list[4],
                                  'Email ID' : Master_columns_list[5],
                                  'Mobile No.' : Master_columns_list[6],
                                  'Your Gender' : Master_columns_list[7],
                                  'College Name' : Master_columns_list[8],
                                  'Whatsapp No ' : Master_columns_list[9],
                                  'Branch/ Department' : Master_columns_list[10],
                                  'Current Semester' : Master_columns_list[11],
                                  'College City' : Master_columns_list[12],
                                  'State' : Master_columns_list[13],
                                  'Status' : Master_columns_list[14],
                                  'Mode' : Master_columns_list[15],
                                  'Payee Name/New ID' : Master_columns_list[16],
                                  'Calling Responses' : Master_columns_list[17],
                                  'Zoom id' : '',
                                  'Matched' : Master_columns_list[19],
                                  'Zoom Name' : '',
                                  'Meeting ID' : ''
                                  }
                    Master_sheet = Master_sheet.append(dictionary, ignore_index=True)
                    
        
        
        
        #we will fill the meeting id also of every student
        def fill_meeting_id1(Matching_data_email):
            match_index = upper_list.index(str(Matching_data_email).upper().strip())
            if str(Meeting_id) not in Master_sheet["Meeting ID"][match_index]:
                if Master_sheet["Meeting ID"][match_index] == '':
                    Master_sheet["Meeting ID"][match_index] = str(Meeting_id)
                else:
                    Master_sheet["Meeting ID"][match_index] = Master_sheet["Meeting ID"][match_index] + " , " + str(Meeting_id)
            
        def fill_meeting_id2(Matching_data_email):
            match_index = upper_list2.index(str(Matching_data_email).upper().strip())
            if str(Meeting_id) not in Master_sheet["Meeting ID"][match_index]:
                if Master_sheet["Meeting ID"][match_index] == '':
                    Master_sheet["Meeting ID"][match_index] = str(Meeting_id)
                else:
                    Master_sheet["Meeting ID"][match_index] = Master_sheet["Meeting ID"][match_index] + " , " + str(Meeting_id)
        
        
        upper_list = [x.upper().strip() if type(x) == str else x for x in Master_sheet["Email ID"].values.tolist()]
        upper_list2 = [z.upper().strip() if type(z) == str else z for z in Master_sheet["Zoom id"].values.tolist()]
        
    
        for Matching_data_email_index,Matching_data_email in enumerate(Matching_data_email_list):
            if Matching_data["Matched"][Matching_data_email_index] == True:
                if str(Matching_data_email).upper().strip() in upper_list:
                    fill_meeting_id1(Matching_data_email)
                elif str(Matching_data_email).upper().strip() in upper_list2:
                    fill_meeting_id2(Matching_data_email)
                elif Matching_data["Zoom id"][Matching_data_email_index].upper().strip() in upper_list:
                    fill_meeting_id1(Matching_data["Zoom id"][Matching_data_email_index])
                elif Matching_data["Zoom id"][Matching_data_email_index].upper().strip() in upper_list2:
                    fill_meeting_id2(Matching_data["Zoom id"][Matching_data_email_index])
            else:
                if str(Matching_data_email).upper().strip() in upper_list:
                    fill_meeting_id1(Matching_data_email)
                elif str(Matching_data_email).upper().strip() in upper_list2:
                    fill_meeting_id2(Matching_data_email)
                                                                             
                
        
        
        #If in any zoom id empty than we will fill that
        for Master_sheet_empty_index,Master_sheet_empty in enumerate(Master_sheet["Email ID"].values.tolist()):
            if Master_sheet["Matched"][Master_sheet_empty_index] == 'TRUE' or Master_sheet["Matched"][Master_sheet_empty_index] == True:
                if Master_sheet["Zoom id"][Master_sheet_empty_index] == '' or type(Master_sheet["Zoom id"][Master_sheet_empty_index]) == float:
                    Master_sheet["Zoom id"][Master_sheet_empty_index] = Master_sheet_empty
    
        #Upload the complete master sheet   
        Master_sheet.drop_duplicates(subset=["Email ID"], keep='first', inplace=True)
        Master_sheet.reset_index(inplace = True, drop = True)
        gd.set_with_dataframe(sheet, Master_sheet)        
                
    
    
        
        
        
        
        
        
            
        """
        
        
        ++++++++++++++++++++++++++++
            
        #UI Part
            
        ++++++++++++++++++++++++++++
         
            
        
        """
        
        
        
        
        
        
        
         #we start from here our UI part
        if UI_run.upper() == 'Y' or UI_run.upper() == 'YES':
        
            import io
            import flask
            import dash
            import dash_core_components as dcc
            import dash_html_components as html
            from dash.dependencies import Input, State, Output
            import pandas as pd
            import plotly.graph_objects as go
            import plotly.express as px
            import dash_table as dt
            import dash_table
            import dash_bootstrap_components as dbc
            import webbrowser
            from threading import Timer
            import math
            import datetime
            
            #open browser automatically
            def open_browser():
                  webbrowser.open_new('http://127.0.0.1:8050/')
              
            #use external css for making our UI more interactive    
            external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']
            
            app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
            
            
            
            
            
            #This is Mark down text which will printed by softcoded.
            
            if os.path.exists("{}.txt".format(Meeting_id)):  #first we will check that our txt file available or not
                markdown_list = []
                
                try:
                    f= open("{}.txt".format(Meeting_id), 'r')
                    while True:
                        # read line
                        line = f.readline()
                        markdown_list.append(line)
                        # check if line is not empty
                        if not line:
                            break
                except (IOError, ValueError, EOFError) as e:
                  print(e)
                f.close()
                
                
                all_lines = "\n".join(markdown_list)[:-1]
                
                
                markdown_text = '''
                {}
                '''.format(all_lines)
            else:
                markdown_text = '''
                
                '''
    
            
            
            
            
            
            #Daylist for Dropdown
            list1 = []
            for d_index in range(len(reports_days_name_list)):
                day_number = (int(file_number) - int(len(reports_days_name_list))) + (d_index+1)
                list1.append("Day{}".format(day_number))
            
            
            
            
            
            list2 = ["Registered Name","Email ID",'Your Gender',"College Name",'Whatsapp No ', 'Zoom Name', 'Zoom id']
            
            
            Suspence_day_list = ['Zoom Name', 'Email', 'Time', 'Registered Name', 'Gender','College Name', 'WhatsApp No.', 'Zoom id']
            
            
            
            #this for all Full datapresent (Who are present everyday)
            Full_data_present = pd.read_csv("Reports/Full_data_present_everyday.csv")
            Full_dat_index = Full_data_present[(Full_data_present["Name"].isnull())].index[0]
            Full_data_present1 = Full_data_present.iloc[:Full_dat_index,]
            present_count = len(Full_data_present1)
            
            Full_data_present1.rename(columns={'Total':'Total Time(Minutes)','Name':'Registered Name'}, inplace = True )
            Full_data_list1 = ['Registered Name','Gender','College Name','Email','WhatsApp No.']
            Full_data_list2 = Full_data_present.columns.tolist()[6:-1]
            Full_data_list = Full_data_list1 + Full_data_list2
            
            
            fig1 = px.bar(Full_data_present1, y ='Total Time(Minutes)',x = 'Registered Name',
                            text='Total Time(Minutes)',
                            hover_data=Full_data_list,
                            height=450,
                         )
            
            
            
            
            
            Not_Present_any_col_list = ['Name','Email','Gender','College Name','WhatsApp No.']
            
            
            
            
            
            
            
            #Atleast One Day Present Students
            Atleast_present_col_list = Atleast_one_day.columns.tolist()
            Atleast_one_day_copy = Atleast_one_day.copy()
            Atleast_one_day_index = Atleast_one_day[(Atleast_one_day["Email"].isnull())].index[0]
            Atleast_one_day_copy = Atleast_one_day_copy.iloc[ : Atleast_one_day_index,]
         
            
            
            
            
            
            
            
            
            
            #Consolidated graph which will be permanent below which tells us atleast one day graph
            consolidated_dataframe2 = df4.copy()
            consolidated_dataframe2 = consolidated_dataframe2.rename(columns={'Zoom id': 'Email'})
            consolidated_dataframe2.drop_duplicates(subset=["Email"], keep='first', inplace=True)
            consolidated_dataframe2.reset_index(inplace = True, drop = True) 
            consolidated_count = len(consolidated_dataframe2)
            consolidated_dataframe3 = pd.merge(consolidated_dataframe2, Atleast_one_day_copy, how='left', on=['Email'])
            consolidated_dataframe3.drop(consolidated_dataframe3.iloc[:, 5:10], inplace = True, axis = 1)
            
            consolidated_dataframe3 = consolidated_dataframe3.rename(columns={'Name_x': 'Name',
                                                                              'Gender_x': 'Gender',
                                                                              'College Name_x': 'College Name',
                                                                              'WhatsApp No._x':'WhatsApp No.'})
            consolidated_dataframe3.rename(columns={'Total':'Total Time(Minutes)','Name':'Registered Name'}, inplace = True )
            consolidated_dataframe3_day_list = consolidated_dataframe3.columns.tolist()[5:]
            for consolidated_dataframe3_day_list_name in consolidated_dataframe3_day_list:
                    consolidated_dataframe3[consolidated_dataframe3_day_list_name].fillna(0, inplace=True)
            consolidated_dataframe3 = consolidated_dataframe3.sort_values("Total Time(Minutes)", ascending = False)
            consolidated_dataframe3.reset_index(inplace = True, drop = True)
            
            consolidated_data_list1 = ['Registered Name','Email','Gender','College Name','WhatsApp No.']
            consolidated_data_list = consolidated_data_list1 + consolidated_dataframe3_day_list
            
            consolidated_fig = px.bar(consolidated_dataframe3, y ='Total Time(Minutes)',x = 'Registered Name',
                            text='Total Time(Minutes)',
                            hover_data=consolidated_data_list,
                            height=450,
                         )
            
            #difference of absent list
            diff_day_list = []
            l = 0
            for diff_index,diff_name in enumerate(reports_days_name_list):
                if diff_index == 0:
                    diff_days = "Registered" + " - " + diff_name
                    diff_day_list.append(diff_days)
#                    change_day1 = diff_name
                if diff_index == l + 1:
                    l += 1
                    change_day2 = diff_name
                    diff_days = reports_days_name_list[l-1] + " - " + change_day2
                    diff_day_list.append(diff_days)
                    
            
            
            
            colors = {
                'background': '#111111',
                'text': '#7FDBFF',
                'color1': 'white',
                'color2': 'blue'
            }
            
            #It will show the meeting on title
            app.title = str(Meeting_id)
            
            PAGE_SIZE = 10
            
            app.layout = html.Div(
            html.Div([
                    dbc.Container(
                    html.Div(
                    [
                    html.Img(
                        src="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSriyJq1c35TlZ9DIJQrV4ELxG914tFyXLVKQ&usqp=CAU",
                        className='three columns',
                        style={
                            'height': '15%',
                            'width': '26%',
                            'float': 'center',
                            'position': 'relative',
                            'padding-top': 0,
                            'margin-left': 360,
                            'textAlign': 'center'
                            },
                        ),
                    ], className="row"
                ),
            ),
            html.Div( children=[
                    
                html.H1(
                    children='Forsk Coding School',
                    style={
                        'textAlign': 'center',
                        'color': colors['color1'],
                        'backgroundColor': colors['color2'],
                        'borderRadius': '5px',
                        'margin': '20px',
                        'padding': '10px',
                        'margin-bottom':'-6px',
                        'font-size': '40px',
                        'margin-top':'10px'
                        
                    }
                ),
                html.H3(
                    children=' Student Attendence Analysis ',
                    style={
                        'textAlign': 'center',
                        'color': colors['color1'],
                        'backgroundColor': colors['color2'],
                        'borderRadius': '5px',
                        'margin': 'auto',
                        'margin-right':'20px',
                        'margin-left':'20px',
                        'font-size': '18px',
                        'padding': '10px',
                    }
                ),
                
                #Markdown (details of Prime)
                html.Div([dcc.Markdown(children=markdown_text)],
                          style={
                        'textAlign': 'center',
                        'font-size': '23px',
                        'font-family': "Comic Sans MS",
                    }
                ),
                
                
                #dropdown (Days)
                dbc.Container(
                html.Div([dcc.Dropdown(id='dd',
                    options=[{'label': c , 'value': c} for c in reports_days_name_list],
                    value=reports_days_name_list[0])],
                style={
                        'width':'40%',
                        'padding':40,
                        'justify-content': 'center',
                        'margin-left':220
                    }
                ),
                ),
                
                
                
                
                #Daily trends Graph:-
             
                html.Div([
                        html.Div(
                                    [
                                        html.H3(
                                            children='Daily Trends',
                                            style={
                                                'textAlign': 'Right',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '28px',
                                                'margin-bottom':'0px',
                                                'font': '28px Arial, sans-serif',
                                                'margin-right':'20px',
                                                
                                            }
                                        ),
                                        ],className='seven columns',
                                    style={'padding-top': '30px'}
                        ),
                       html.Div(
                                    [
                                        html.H3(
                                            children='Max Count: ',
                                            style={
                                                'textAlign': 'Right',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '25px',
                                                'margin-bottom':'0px',
                                                'font': '20px Arial, sans-serif',
                                                
                                            }
                                        ),
                                    ],
                                    className='three columns',
                                    style={'padding-top': '30px'}
                                ),
                        html.Div(
                                    [
                                        html.H3(
                                            id = 'check_count_Daily_Trends',
                                            style={
                                                'textAlign': 'Left',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '25px',
                                                'margin-bottom':'0px',
                                                'font': '20px Arial, sans-serif',
                                                
                                            }
                                        ),
                                    ],
                                    className='two columns',
                                    style={'padding-top': '30px'}
                                )
                    ],className = 'row'
                ),
            
                
                html.H3(
                id = 'reg3',
                style={
                    'textAlign': 'center',
                    'color': 'black',
                    'margin': 'auto',
                    'font-size': '25px',
                    'margin-bottom':'0px',
                    'font': '20px Arial, sans-serif',
                    
                }
                ),                    
                
                #graph1
                dcc.Graph(id = 'graph_daily_trends'),
              
                
                
                
                
                
                
                #Present Registered student
                dbc.Container(
                html.Div([
                        html.Div(
                        [
                                    html.A(
                                    html.Button('Export', id='download-button_daywise_present'), 
                                    id='my-link_daywise_present'),
                                    
                                    ],className='two columns',
                                   style={'padding-top': '30px'}
                        ),
                        html.Div(
                                    [
                                        html.H3(
                                            children='Registered & Present Students',
                                            style={
                                                'textAlign': 'Right',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '28px',
                                                'margin-bottom':'0px',
                                                'font': '28px Arial, sans-serif',
                                                
                                            }
                                        ),
                                        ],className='six columns',
                                    style={'padding-top': '30px'}
                        ),
                       html.Div(
                                    [
                                        html.H3(
                                            children='Count: ',
                                            style={
                                                'textAlign': 'Right',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '25px',
                                                'margin-bottom':'0px',
                                                'font': '20px Arial, sans-serif',
                                                
                                            }
                                        ),
                                    ],
                                    className='three columns',
                                    style={'padding-top': '30px'}
                                ),
                        html.Div(
                                    [
                                        html.H3(
                                            id = 'check_count_present',
                                            style={
                                                'textAlign': 'Left',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '25px',
                                                'margin-bottom':'0px',
                                                'font': '20px Arial, sans-serif',
                                                
                                            }
                                        ),
                                    ],
                                    className='one columns',
                                    style={'padding-top': '30px'}
                                )
                    ],className = 'row'
                ),
                ),
                                    
                                    
                html.H3(
                id = 'reg',
                style={
                    'textAlign': 'center',
                    'color': 'black',
                    'margin': 'auto',
                    'font-size': '25px',
                    'margin-bottom':'0px',
                    'font': '20px Arial, sans-serif',
                    
                }
                ),
                #graph1
                dcc.Graph(id = 'graph'),
                
                
                
                
                #Absent Students
                dbc.Container(
                html.Div([
                        html.Div(
                        [
                                    html.A(
                                    html.Button('Export', id='download-button_daywise_Absent'), 
                                    id='my-link_daywise_Absent'),
                                    
                                    ],className='two columns',
                                   style={'margin': 'auto','margin-bottom':'5px',
                                                'margin-top':'85px'}
                        ),
                        html.Div(
                                    [
                                        html.H3(
                                            children='Registered & Absent Students Table',
                                            style={
                                                'textAlign': 'Right',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '28px',
                                                'margin-bottom':'8px',
                                                'margin-top':'70px',
                                                'font': '28px Arial, sans-serif',
                                                
                                            }
                                        ),
                                        ],className='seven columns',
                                    style={'padding-top': '30px'}
                        ),
                       html.Div(
                                    [
                                        html.H3(
                                            children='Count: ',
                                            style={
                                                'textAlign': 'Right',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '25px',
                                                'margin-bottom':'8px',
                                                'margin-top':'70px',
                                                'font': '20px Arial, sans-serif',
                                                
                                            }
                                        ),
                                    ],
                                    className='two columns',
                                    style={'padding-top': '30px'}
                                ),
                        html.Div(
                                    [
                                        html.H3(
                                            id = 'check_count_absent',
                                            style={
                                                'textAlign': 'Left',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '25px',
                                                'margin-bottom':'8px',
                                                'margin-top':'70px',
                                                'font': '20px Arial, sans-serif',
                                                
                                            }
                                        ),
                                    ],
                                    className='one columns',
                                    style={'padding-top': '30px'}
                                )
                    ],className = 'row'
                ),
                ),                    
                                    
                html.H3(
                id = 'reg1',
                style={
                    'textAlign': 'center',
                    'color': 'black',
                    'margin': 'auto',
                    'font-size': '25px',
                    'margin-bottom':'30px',
                    'font': '20px Arial, sans-serif',
                    
                }
                ),
                
                
                #Absent student Table
                dbc.Container(
                html.Div(
                        [
                                
                            dash_table.DataTable(
                            id='datatable-paging',
                            columns=[
                                {"name": i, "id": i} for i in list2],
                           css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
                           page_current=0,
                           page_size=PAGE_SIZE,
                           page_action='custom',
                           style_table={'overflowX': 'auto'},
                           style_cell={'height': 'auto',
                                       'textAlign': 'left',
                                       'minWidth': '200px', 'width': '210px', 'maxWidth': '200px',
                                       'whiteSpace': 'normal'}, 
                           style_data={ 'border': '1px solid blue' ,
                                       'margin-left':'20px',
                                       'margin-right':'20px',
                                       'whiteSpace': 'normal',
                                        'height': 'auto',
                                        'lineHeight': '15px'},
                            style_header={
                              'backgroundColor': 'rgb(230, 230, 230)',
                              'fontWeight': 'bold'
                        },

                          
                            ),
                            
                            
                        ], className = 'row'
                    ),className="p-5",
                ),
                                    
                                    
                                    
                                    
                #Suspense Students
                dbc.Container(
                 html.Div([
                        html.Div(
                        [
                                    html.A(
                                    html.Button('Export', id='download-button_daywise_Suspence'), 
                                    id='my-link_daywise_Suspence'),
                                    
                                    ],className='two columns',
                                   style={'margin': 'auto','margin-bottom':'5px',
                                                'margin-top':'85px'}
                        ),
                        html.Div(
                                    [
                                        html.H3(
                                            children='Suspense Students(Daywise)',
                                            style={
                                                'textAlign': 'Right',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '28px',
                                                'margin-bottom':'8px',
                                                'margin-top':'70px',
                                                'font': '28px Arial, sans-serif',
                                                
                                            }
                                        ),
                                        ],className='six columns',
                                    style={'padding-top': '30px'}
                        ),
                       html.Div(
                                    [
                                        html.H3(
                                            children='Count: ',
                                            style={
                                                'textAlign': 'Right',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '25px',
                                                'margin-bottom':'8px',
                                                'margin-top':'70px',
                                                'font': '20px Arial, sans-serif',
                                                
                                            }
                                        ),
                                    ],
                                    className='three columns',
                                    style={'padding-top': '30px'}
                                ),
                        html.Div(
                                    [
                                        html.H3(
                                            id = 'check_count_suspence',
                                            style={
                                                'textAlign': 'Left',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '25px',
                                                'margin-bottom':'8px',
                                                'margin-top':'70px',
                                                'font': '20px Arial, sans-serif',
                                                
                                            }
                                        ),
                                    ],
                                    className='one columns',
                                    style={'padding-top': '30px'}
                                )
                    ],className = 'row'
                ),
                 ),                   
                                    
                html.H3(
                id = 'reg2',
                style={
                    'textAlign': 'center',
                    'color': 'black',
                    'margin': 'auto',
                    'font-size': '25px',
                    'margin-bottom':'30px',
                    'font': '20px Arial, sans-serif',
                    
                }
                ),
                
                #Suspence Data Table
                dbc.Container(
                html.Div(
                        [
                                
                            dash_table.DataTable(
                            id='suspence_daywise',
                            columns=[
                                {"name": i, "id": i} for i in Suspence_day_list],
                           css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
                           page_current = 0,
                           page_size = PAGE_SIZE,
                           page_action = 'custom',
                           style_table={'overflowX': 'auto'},
                           style_cell={'height': 'auto',
                                       'textAlign': 'left',
                                       'minWidth': '200px', 'width': '230px', 'maxWidth': '240px',
                                       'whiteSpace': 'normal'}, 
                           style_data={ 'border': '1px solid blue' ,
                                       'margin-left':'20px',
                                       'margin-right':'20px',
                                       'whiteSpace': 'normal',
                                        'height': 'auto',
                                        'lineHeight': '15px'},
                            style_header={
                              'backgroundColor': 'rgb(230, 230, 230)',
                              'fontWeight': 'bold'
                        },
                   
                          
                            ),
                            
                            
                        ], className = 'row'
                    ),className="p-5",
                ),
                
                
                
                #A horizontal line:
                html.H1(
                    children='',
                    style={
                        'textAlign': 'center',
                        'color': colors['color1'],
                        'backgroundColor': 'black',
                        'borderRadius': '5px',
                        'margin': '20px',
                        'padding': '2px',
                        'margin-bottom':'30px',
                        'font-size': '10px',
                        'margin-top':'120px'
                        
                    }
                ),
                
                
                
                #Present Everyday
                dbc.Container(
                html.Div([
                        html.Div(
                        [
                                    html.A(
                                    html.Button('Export', id='download-button_All_day_present'), 
                                    id='my-link_All_day_present',
                                    href = '/dash/urlToDownload_All_day_present?value=Full_data_present_everyday'),
                                    ],className='two columns',
                                   style={'margin-bottom':'5px',
                                          'margin-top':'85px',}
                        ),
                        html.Div(
                                    [
                                        html.H3(
                                            children='All Day Present Students',
                                            style={
                                                'textAlign': 'Right',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '28px',
                                                'margin-bottom':'8px',
                                                'margin-top':'70px',
                                                'font': '28px Arial, sans-serif',
                                                
                                            }
                                        ),
                                        ],className='six columns',
                                    style={'padding-top': '30px'}
                        ),
                       html.Div(
                                    [
                                        html.H3(
                                            children='Count: ',
                                            style={
                                                'textAlign': 'Right',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '25px',
                                                'margin-bottom':'8px',
                                                'margin-top':'70px',
                                                'font': '20px Arial, sans-serif',
                                                
                                            }
                                        ),
                                    ],
                                    className='three columns',
                                    style={'padding-top': '30px'}
                                ),
                        html.Div(
                                    [
                                        html.H3(
                                            children = present_count,
                                            style={
                                                'textAlign': 'Left',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '25px',
                                                'margin-bottom':'8px',
                                                'margin-top':'70px',
                                                'font': '20px Arial, sans-serif',
                                                
                                            }
                                        ),
                                    ],
                                    className='one columns',
                                    style={'padding-top': '30px'}
                                )
                    ],className = 'row'
                ),
                ),                    
                
                #graph4           
                dcc.Graph(figure=fig1),
                
                
                
                
                #Not present any day student Table
                dbc.Container(
                html.Div([
                        html.Div(
                        [
                                    html.A(
                                    html.Button('Export', id='download-button_Not_present'), 
                                    id='my-link_Not_present',
                                    href = '/dash/urlToDownload_Not_present?value=Not_present_any_day'),
                                    ],className='two columns',
                                   style={'margin-bottom':'25px',
                                          'margin-top':'85px',}
                        ),
                        html.Div(
                                    [
                                        html.H3(
                                            children='Not Present Any Day Students Table',
                                            style={
                                                'textAlign': 'Right',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '28px',
                                                'margin-bottom':'30px',
                                                'margin-top':'70px',
                                                'font': '28px Arial, sans-serif',
                                                
                                            }
                                        ),
                                        ],className='seven columns',
                                    style={'padding-top': '30px'}
                        ),
                       html.Div(
                                    [
                                        html.H3(
                                            children='Count: ',
                                            style={
                                                'textAlign': 'Right',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '25px',
                                                'margin-bottom':'30px',
                                                'margin-top':'70px',
                                                'font': '20px Arial, sans-serif',
                                                
                                            }
                                        ),
                                    ],
                                    className='two columns',
                                    style={'padding-top': '30px'}
                                ),
                        html.Div(
                                    [
                                        html.H3(
                                            id = 'not_present_count',
                                            style={
                                                'textAlign': 'Left',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '25px',
                                                'margin-bottom':'30px',
                                                'margin-top':'70px',
                                                'font': '20px Arial, sans-serif',
                                                
                                            }
                                        ),
                                    ],
                                    className='one columns',
                                    style={'padding-top': '30px'}
                                )
                    ],className = 'row'
                    ),
                ),
                                    
                 dbc.Container(
                 html.Div(
                    [
                                
                            dash_table.DataTable(
                            id='not_present_table',
                            columns=[
                                {"name": i, "id": i} for i in Not_Present_any_col_list], 
                           css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
                           page_current=0,
                           page_size=PAGE_SIZE,
                           page_action='custom',
                           style_table={'overflowX': 'auto'},
                           style_cell={'height': 'auto',
                                       'textAlign': 'left',
                                       'minWidth': '200px', 'width': '230px', 'maxWidth': '240px',
                                       'whiteSpace': 'normal'}, 
                           style_data={ 'border': '1px solid blue' ,
                                       'margin-left':'20px',
                                       'margin-right':'20px',
                                       'whiteSpace': 'normal',
                                        'height': 'auto',
                                        'lineHeight': '15px'},
                            style_header={
                              'backgroundColor': 'rgb(230, 230, 230)',
                              'fontWeight': 'bold'
                        },
                 
                          
                            ),
                            
                            
                        ], className = 'row'
                    ),className="p-5",
                ),
                   
            
            
            
            
            
            
                             
                #Atleast One Day Present Table
                dbc.Container(
                html.Div([
                         html.Div(
                         [
                                    html.A(
                                    html.Button('Export', id='download-button_Atleast_one_day'), 
                                    id='my-link_Atleast_one_day',
                                    href = '/dash/urlToDownload_Atleast_one_day?value=Atleast_one_day_present'),
                                    ],className='two columns',
                                   style={'margin-bottom':'15px',
                                          'margin-top':'85px',}
                        ),
                        html.Div(
                                    [
                                        html.H3(
                                            children='Atleast One Day Present Students Table',
                                            style={
                                                'textAlign': 'Right',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '28px',
                                                'margin-bottom':'30px',
                                                'margin-top':'70px',
                                                'font': '28px Arial, sans-serif',
                                                
                                            }
                                        ),
                                        ],className='seven columns',
                                    style={'padding-top': '30px'}
                        ),
                       html.Div(
                                    [
                                        html.H3(
                                            children='Count: ',
                                            style={
                                                'textAlign': 'Right',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '25px',
                                                'margin-bottom':'30px',
                                                'margin-top':'70px',
                                                'font': '20px Arial, sans-serif',
                                                
                                            }
                                        ),
                                    ],
                                    className='two columns',
                                    style={'padding-top': '30px'}
                                ),
                        html.Div(
                                    [
                                        html.H3(
                                            id = 'Atleast_present_count',
                                            style={
                                                'textAlign': 'Left',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '25px',
                                                'margin-bottom':'30px',
                                                'margin-top':'70px',
                                                'font': '20px Arial, sans-serif',
                                                
                                            }
                                        ),
                                    ],
                                    className='one columns',
                                    style={'padding-top': '30px'}
                                )
                    ],className = 'row'
                ),
                ),
                
                     dbc.Container(
                     html.Div(
                        [
                                
                            dash_table.DataTable(
                            id='Atleast_present_Data',
                            columns=[
                                {"name": i, "id": i} for i in Atleast_present_col_list], 
                           css=[{'selector': 'table', 'rule': 'table-layout: fixed'}], 
                           page_current=0,
                           page_size=PAGE_SIZE,
                           page_action='custom',
                           style_table={
                        'overflowX': 'auto'},
                           style_cell={'height': 'auto',
                                       'textAlign': 'left',
                                       'minWidth': '200px', 'width': '230px', 'maxWidth': '240px',
                                       'whiteSpace': 'normal'}, 
                           style_data={ 'border': '1px solid blue' ,
                                       'margin-left':'20px',
                                       'margin-right':'20px',
                                       'whiteSpace': 'normal',
                                        'height': 'auto',
                                        'lineHeight': '15px'},
#                            style_cell_conditional=[
#                                        {'if': {'column_id': 'College Name'},
#                                              'width': '15%'},
#                                        {'if': {'column_id': 'Email'},
#                                               'width': '18%'},
#                                        {'if': {'column_id': 'WhatsApp No.'},
#                                               'width': '8%'},
#                            ],
                            style_header={
                              'backgroundColor': 'rgb(230, 230, 230)',
                              'fontWeight': 'bold'
                        },
                   
                          
                            ),
                            
                            
                        ], className = 'row'
                    ),className="p-10",
                ),                    
                    
              
                
                
                
                #Suspence Data Table of All Day
                dbc.Container(
                html.Div([
                        html.Div(
                         [
                                    html.A(
                                    html.Button('Export', id='download-button_All_day_suspence'), 
                                    id='my-link_All_day_suspence',
                                    href = '/dash/urlToDownload_All_day_suspence?value=Atleast_one_day_present'),
                                    ],className='two columns',
                                   style={'margin-bottom':'15px',
                                          'margin-top':'85px',}
                        ),
                        html.Div(
                                    [
                                        html.H3(
                                            children='All Suspense Data Table',
                                            style={
                                                'textAlign': 'Right',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '28px',
                                                'margin-bottom':'30px',
                                                'margin-top':'70px',
                                                'font': '28px Arial, sans-serif',
                                                
                                            }
                                        ),
                                        ],className='six columns',
                                    style={'padding-top': '30px'}
                        ),
                       html.Div(
                                    [
                                        html.H3(
                                            children='Count: ',
                                            style={
                                                'textAlign': 'Right',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '25px',
                                                'margin-bottom':'30px',
                                                'margin-top':'70px',
                                                'font': '20px Arial, sans-serif',
                                                
                                            }
                                        ),
                                    ],
                                    className='three columns',
                                    style={'padding-top': '30px'}
                                ),
                        html.Div(
                                    [
                                        html.H3(
                                            id = 'Suspence_present_count',
                                            style={
                                                'textAlign': 'Left',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '25px',
                                                'margin-bottom':'30px',
                                                'margin-top':'70px',
                                                'font': '20px Arial, sans-serif',
                                                
                                            }
                                        ),
                                    ],
                                    className='one columns',
                                    style={'padding-top': '30px'}
                                )
                    ],className = 'row'
                ),
                 ),                   
                                    
                     dbc.Container(
                     html.Div(
                        [
                                
                            dash_table.DataTable(
                            id='Suspence_present_data',
                            columns=[
                                {"name": i, "id": i} for i in Atleast_present_col_list], 
                           css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
                           page_current=0,
                           page_size=PAGE_SIZE,
                           page_action='custom',
                           style_table={'overflowX': 'auto'},
                           style_cell={'height': 'auto',
                                       'textAlign': 'left',
                                       'minWidth': '200px', 'width': '230px', 'maxWidth': '240px',
                                       'whiteSpace': 'normal'}, 
                           style_data={ 'border': '1px solid blue' ,
                                       'margin-left':'20px',
                                       'margin-right':'20px',
                                       'whiteSpace': 'normal',
                                        'height': 'auto',
                                        'lineHeight': '15px'},
#                            style_cell_conditional=[
#                                        {'if': {'column_id': 'Email'},
#                                               'width': '18%'},
#                            ],
                            style_header={
                              'backgroundColor': 'rgb(230, 230, 230)',
                              'fontWeight': 'bold'
                        },
                    
                          
                            ),
                            
                            
                        ], className = 'row'
                    ),className="p-5",
                ),
               
                          
                 
                    
            
            
            #Consoleted final graph 
            dbc.Container(
                 html.Div([
                         html.Div(
                         [
                                    html.A(
                                    html.Button('Export', id='download-button_Consolidated_Analysis'), 
                                    id='my-link_Consolidated_Analysis',
                                    href = '/dash/urlToDownload_Consolidated_Analysis'),
                                    ],className='two columns',
                                   style={'margin-bottom':'15px',
                                          'margin-top':'85px',}
                        ),
                        html.Div(
                                    [
                                        html.H3(
                                            children='Consolidated Analysis',
                                            style={
                                                'textAlign': 'Right',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '28px',
                                                'margin-bottom':'8px',
                                                'margin-top':'70px',
                                                'font': '28px Arial, sans-serif',
                                                
                                            }
                                        ),
                                        ],className='six columns',
                                    style={'padding-top': '30px'}
                        ),
                       html.Div(
                                    [
                                        html.H3(
                                            children='Count: ',
                                            style={
                                                'textAlign': 'Right',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '25px',
                                                'margin-bottom':'8px',
                                                'margin-top':'70px',
                                                'font': '20px Arial, sans-serif',
                                                
                                            }
                                        ),
                                    ],
                                    className='three columns',
                                    style={'padding-top': '30px'}
                                ),
                        html.Div(
                                    [
                                        html.H3(
                                            children = consolidated_count,
                                            style={
                                                'textAlign': 'Left',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '25px',
                                                'margin-bottom':'8px',
                                                'margin-top':'70px',
                                                'font': '20px Arial, sans-serif',
                                                
                                            }
                                        ),
                                    ],
                                    className='one columns',
                                    style={'padding-top': '30px'}
                                )
                    ],className = 'row'
                ),
                ),                    
                
                #graph4           
                dcc.Graph(figure=consolidated_fig),
                


                #A horizontal line:
                html.H1(
                    children='',
                    style={
                        'textAlign': 'center',
                        'color': colors['color1'],
                        'backgroundColor': 'black',
                        'borderRadius': '5px',
                        'margin': '20px',
                        'padding': '2px',
                        'margin-bottom':'100px',
                        'font-size': '10px',
                        'margin-top':'120px'
                        
                    }
                ),
                
                
                
                #search data
                html.Div([
                    dcc.Store(id = 'memory'),
                    html.H3(
                            children='Details of Particular Student',
                            style={
                                'textAlign': 'Center',
                                'color': colors['color2'],
                                'margin': 'auto',
                                'font-size': '33px',
                                'margin-bottom':'20px',
                                'margin-top':'10px',
                                'font': '33px Arial, sans-serif',
                                
                            }
                        ),
                    
                    dbc.Container(
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.P('Search by:'),
                                    dcc.Dropdown(
                                            id = 'filter_x',
                                            options=[
                                                {'label': 'No filter', 'value': 0},
                                                {'label': 'Name', 'value': 1},
                                                {'label': 'Email id', 'value': 2},
                                                {'label': 'Mobile No.', 'value': 3},
                                                {'label': 'College Name', 'value': 4}
                                            ],
                                            value='0'
                                         ),
                                ],
                                className='three columns',
                                style={'margin-top': '10'}
                            ),
                            html.Div(
                                [
                                    html.P('Select one:'),
                                    dcc.Dropdown(
                                            id = 'filter_z',
                                            options=[
                                                {'label': 'No filter', 'value': 0},
                                                {'label': 'Start With', 'value': 1},
                                                {'label': 'Ends With', 'value': 2}
                                            ],
                                            value='0'
                                         ),
                                ],
                                className='three columns',
                                style={'margin-top': '10'}
                            ),
                            html.Div(
                                [
                                    html.P('Search From Here: '),
                                    dcc.Input(
                                              id = 'filter_y',
                                              placeholder='Enter a value...',
                                              value=''
                                          )  ,
                                ],
                                className='four columns',
                                style={'margin-top': '10','padding-left': '70px'}
                            ),
                            html.Div(
                                [
                                    html.Button(children='Search Data', id='button_chart',n_clicks=0)
                                ],
                                className='two columns',
                                style={'padding-top': '30px'}
                            )             
                        ],
                        className='row'
                    ),
                    ),
                            
                    dbc.Container(
                     html.Div(
                        [
                              
                                
                            dash_table.DataTable(
                            id='table',
                            columns=[
                                {"name": i, "id": i} for i in consolidated_data_list],
                            page_current=0,
                            page_size=PAGE_SIZE,
                            page_action='custom',
                                 style_cell={'height': 'auto',
                                               'textAlign': 'left',
                                               'minWidth': '200px', 'width': '230px', 'maxWidth': '240px',
                                               'whiteSpace': 'normal'},  
                            style_table={
                                'overflowX': 'auto'},
                           style_data={ 'border': '1px solid blue' ,
                                       'margin-left':'20px',
                                       'margin-right':'20px'},
                            style_header={
                              'backgroundColor': 'rgb(230, 230, 230)',
                              'fontWeight': 'bold'},
                            ),
                            
                            
                                    
                                    
                         ], className = 'row',style = {'margin-top': 40,}
                      ),
                   ),
        
                   ], className = 'row',  style = {'margin-top': 50,
                                                    'margin-bottom': 50,
                                                    'margin-left': 80,
                                                    'margin-right': 80,
                                                   'border':'1px solid #C6CCD5', 
                                                   'padding': 15,
                                                   'border-radius': '5px'}
                ),
               
               
                
                
                
                
                #A horizontal line:
                html.H1(
                    children='',
                    style={
                        'textAlign': 'center',
                        'color': colors['color1'],
                        'backgroundColor': 'black',
                        'borderRadius': '5px',
                        'margin': '20px',
                        'padding': '2px',
                        'margin-bottom':'50px',
                        'font-size': '10px',
                        'margin-top':'120px'
                        
                    }
                ),
                
                
                
                
                
                #Heading of dropdown:-
                html.H3(
                            children='Difference Tables',
                            style={
                                'textAlign': 'Center',
                                'color': colors['color2'],
                                'margin': 'auto',
                                'font-size': '33px',
                                'margin-bottom':'20px',
                                'margin-top':'30px',
                                'font': '33px Arial, sans-serif',
                                
                            }
                        ),
                
               #last Drop Down:
               dbc.Container(
                html.Div([dcc.Dropdown(id='last_dd',
                    options=[{'label': c , 'value': c} for c in diff_day_list],
                    value = diff_day_list[0])],
                style={
                        'width':'40%',
                        'padding':40,
                        'justify-content': 'center',
                        'margin-left':220,
                        'margin-top':'50px'
                    }
                ),
                ),
                
                #print the total register count (This is a extra part)
             
                html.Div([
                        html.Div(
                                    [
                                        html.H3(
                                            children='',
                                            style={
                                                'textAlign': 'Right',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '28px',
                                                'margin-bottom':'0px',
                                                'margin-top':'0px',
                                                'font': '28px Arial, sans-serif',
                                                
                                            }
                                        ),
                                        ],className='seven columns',
                                    style={'padding-top': '30px'}
                        ),
                       html.Div(
                                    [
                                        html.H3(
                                            children='Total Registered: ',
                                            style={
                                                'textAlign': 'Right',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '25px',
                                                'margin-bottom':'0px',
                                                'margin-top':'0px',
                                                'font': '20px Arial, sans-serif',
                                                
                                            }
                                        ),
                                    ],
                                    className='three columns',
                                    style={'padding-top': '30px'}
                                ),
                        html.Div(
                                    [
                                        html.H3(
                                            children = consolidated_count,
                                            style={
                                                'textAlign': 'Left',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '25px',
                                                'margin-bottom':'0px',
                                                'margin-top':'0px',
                                                'font': '20px Arial, sans-serif',
                                                
                                            }
                                        ),
                                    ],
                                    className='two columns',
                                    style={'padding-top': '30px'}
                                )
                    ],className = 'row'
                ),
                 
                
                
                
                
                #heading of difference table
                html.Div([
                        html.Div(
                                    [
                                        html.H3(
                                                id = 'diff_head',
                                                style={
                                                    'textAlign': 'Right',
                                                    'color': 'blue',
                                                    'margin': 'auto',
                                                    'font-size': '25px',
                                                    'margin-bottom':'30px',
                                                    'margin-right':'30px',
                                                    'font': '20px Arial, sans-serif',
                                                    
                                                }
                                          ),
                                        ],className='seven columns',
                                    style={'padding-top': '30px'}
                        ),
                       html.Div(
                                    [
                                        html.H3(
                                            children='Count: ',
                                            style={
                                                'textAlign': 'Right',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '25px',
                                                'margin-bottom':'0px',
                                                'font': '20px Arial, sans-serif',
                                                
                                            }
                                        ),
                                    ],
                                    className='three columns',
                                    style={'padding-top': '30px'}
                                ),
                        html.Div(
                                    [
                                        html.H3(
                                            id = 'check_count_diff',
                                            style={
                                                'textAlign': 'Left',
                                                'color': colors['color2'],
                                                'margin': 'auto',
                                                'font-size': '25px',
                                                'margin-bottom':'0px',
                                                'font': '20px Arial, sans-serif',
                                                
                                            }
                                        ),
                                    ],
                                    className='two columns',
                                    style={'padding-top': '30px'}
                                )
                    ],className = 'row'
                ),
                                    
                                    
                #table by drop down
                dbc.Container(
                html.Div(
                        [
                                
                            dash_table.DataTable(
                            id='diff_daywise',
                            columns=[
                                {"name": i, "id": i} for i in Suspence_day_list],
                           css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
                           page_current = 0,
                           page_size = PAGE_SIZE,
                           page_action = 'custom',
                           style_table={'overflowX': 'auto'},
                           style_cell={'height': 'auto',
                                       'textAlign': 'left',
                                       'minWidth': '200px', 'width': '230px', 'maxWidth': '240px',
                                       'whiteSpace': 'normal'}, 
                           style_data={ 'border': '1px solid blue' ,
                                       'margin-left':'20px',
                                       'margin-right':'20px',
                                       'whiteSpace': 'normal',
                                        'height': 'auto',
                                        'lineHeight': '15px'},
                            style_header={
                              'backgroundColor': 'rgb(230, 230, 230)',
                              'fontWeight': 'bold'
                        },

                          
                            ),
                            
                            
                        ], className = 'row'
                    ),className="p-5",
                ),
                                    
                                    


               #footer part
                  html.H3(
                    children='Footer Section',
                    style={
                        'textAlign': 'center',
                        'color': colors['color1'],
                        'backgroundColor': colors['color2'],
                        'borderRadius': '2px',
                        'padding': '70px',
                        'margin-bottom':'0',
                        'font-size': '20px',
                        'margin-top':'20px'
                        
                    }
                ),
                  
                  
            ]),
        
            ])
            )
            
            
            
            @app.callback(dash.dependencies.Output('reg','children'),[dash.dependencies.Input('dd','value')])
            def update_fig(value):  
                return value
            
            
            @app.callback(dash.dependencies.Output('reg1','children'),[dash.dependencies.Input('dd','value')])
            def update_fig1(value):  
                return value
            
            @app.callback(dash.dependencies.Output('reg2','children'),[dash.dependencies.Input('dd','value')])
            def update_fig2(value):  
                return value
            
            @app.callback(dash.dependencies.Output('reg3','children'),[dash.dependencies.Input('dd','value')])
            def update_fig2(value):  
                return value
            
            
            #Daily trends graph
            @app.callback([dash.dependencies.Output('graph_daily_trends','figure'),
                          dash.dependencies.Output('check_count_Daily_Trends','children')],
                          [dash.dependencies.Input('dd','value')])
            
            def update_fig(value):
                try:
                    create_day_wise_index = reports_days_name_list.index(value)
                    if len(create_daywise[create_day_wise_index].columns.tolist()) == 10:
                        dff = create_daywise[create_day_wise_index]
                        daily_count = len(dff)
                        if len(dff["Join"][0].split()) == 2:
                            for i in range(len(dff)):
                                dff["Join"][i] = dff["Join"][i].split()[1][:-3]
                                dff["Leave"][i] = dff["Leave"][i].split()[1][:-3]
                            
                        min_time = min(dff["Join"].tolist())
                        max_time = max(dff["Leave"].tolist())
                        fmt = '%H:%M'
                        d1 = datetime.datetime.strptime(min_time, fmt)
                        d2 = datetime.datetime.strptime(max_time, fmt)
                        
                        diff = d2 -d1
                        diff_minutes = diff.seconds/60
                        a = math.ceil(diff_minutes/10)
                        
                        list1 = []
                        list1.append(d1)
                        for i in range(a):
                            d1 = d1 + datetime.timedelta(minutes=10)
                            list1.append(d1)
                        list2 = []
                        for i in list1:
                            list2.append(i.strftime('%H:%M'))
                        
                        list3 = [0]
                        for index,Time in enumerate(list2[1:]):
                            count = 0
                            for i in range(len(dff)):
                                if dff["Join"][i] <= list2[index+1] and dff["Leave"][i] >= list2[index+1]:
                                    count += 1
                                elif dff["Join"][i] <= list2[index+1] and dff["Leave"][i] >= list2[index]:
                                    count += 1
                            list3.append(count)
                        
                        data1 = {'Time':list2[:], 'Count':list3}
                        daily_trends = pd.DataFrame(data1)
                        
                        figure = go.Figure(data=go.Scatter(x=daily_trends['Time'], y=daily_trends['Count']))
                        return figure,daily_count
                    
                    elif len(create_daywise[create_day_wise_index].columns.tolist()) == 8:   
                        daily_trends = pd.DataFrame(columns=['Time','Count'])
                        daily_count = len(daily_trends)
                        figure = go.Figure(data=go.Scatter(x=daily_trends['Time'], y=daily_trends['Count']))
                        return figure,daily_count
                        
            
                except:
                    return html.Div(['There was an error processing this file.'])
                
                
            
            
            
            
            
            #calling for Registered and present students
            @app.callback([dash.dependencies.Output('graph','figure'),
                           dash.dependencies.Output('check_count_present','children'),
                           dash.dependencies.Output('my-link_daywise_present', 'href')],
                          [dash.dependencies.Input('dd','value')])
            
            def update_fig(value):
                try:
                
                    dff = pd.read_csv("Reports/{}.csv".format(value))
                    a = dff[(dff["Email"].isnull())].index[0]
                    dff = dff.iloc[:a,]
                    count = len(dff)
                    dff.rename(columns={'Time':'Time(Minutes)'}, inplace = True )
                    figure = px.bar(dff, y ='Time(Minutes)',x = 'Registered Name',
                                    text='Time(Minutes)',
                                    hover_data=['Registered Name','Gender','College Name','WhatsApp No.','Email'],
                                    height=650,
                                    )
                    figure.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                    figure.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
            
                except:
                    return html.Div(['There was an error processing this file.'])
                    
                return figure,count,'/dash/urlToDownload_daywise_present?value={}'.format(value)
            
            #calling for Registered and present students
            @app.server.route('/dash/urlToDownload_daywise_present')
            def Download_daywise_present():
                value = flask.request.args.get('value')
                # create a dynamic csv or file here using `StringIO`
                # (instead of writing to the file system)
                dff = pd.read_csv("Reports/{}.csv".format(value))
                a = dff[(dff["Email"].isnull())].index[0]
                dff = dff.iloc[:a,]
                dff.rename(columns={'Time':'Time(Minutes)'}, inplace = True )
                upper_list4 = [x.upper().strip() if type(x) == str else x for x in Master_sheet["Email ID"].values.tolist()]
                upper_list5 = [z.upper().strip() if type(z) == str else z for z in Master_sheet["Zoom id"].values.tolist()]
                upper_list6 = [y.upper().strip() if type(y) == str else y for y in dff["Zoom id"].values.tolist()]
                master_dataframe = []
                for upper_list6_email in upper_list6:
                    if upper_list6_email in upper_list4:
                        upper_list4_index = upper_list4.index(upper_list6_email)
                        master_dataframe.append(Master_sheet.loc[upper_list4_index,])
                    elif upper_list6_email in upper_list5:
                        upper_list5_index = upper_list5.index(upper_list6_email)
                        master_dataframe.append(Master_sheet.loc[upper_list5_index,])
                master_dataframe = pd.DataFrame(master_dataframe)        
                str_io = io.StringIO()
                master_dataframe.to_csv(str_io)
                mem = io.BytesIO()
                mem.write(str_io.getvalue().encode('utf-8'))
                mem.seek(0)
                str_io.close()
                return flask.send_file(mem,
                                       mimetype='text/csv',
                                       attachment_filename='daywaise_present_{}.csv'.format(value),
                                       as_attachment=True)
            
            
            
            
            
            #Daywise student Absent Student Table
            @app.callback([dash.dependencies.Output('datatable-paging','data'),
                           dash.dependencies.Output('check_count_absent','children'),
                           dash.dependencies.Output('datatable-paging','page_count'),
                           dash.dependencies.Output('my-link_daywise_Absent', 'href')],
                           [dash.dependencies.Input('dd','value'),
                            dash.dependencies.Input('datatable-paging', "page_current"),
                            dash.dependencies.Input('datatable-paging', "page_size")])
            
            def update_fig(value,page_current,page_size):
                try:
                    dff = pd.read_csv("Reports/{}.csv".format(value))
                    b = dff[(dff["Email"].isnull())].index[1]
                    dff = dff.iloc[b+2:,]
                    dff_list = []
                    for dff_index in dff["Email"].tolist():
                        dff_row = df4_copy[df4_copy[df4_column_list[1]] == dff_index]
                        dff_list.append(dff_row)
                    dff = pd.concat(dff_list)
                    count = len(dff)
                    page_count_value = math.ceil(len(dff)/10)
                    dff = dff[df4_column_list + ['Zoom Name','Zoom id']]
                    dff.columns = ["Registered Name","Email ID",'Your Gender',"College Name",'Whatsapp No ', 'Zoom Name', 'Zoom id']
                    data=dff.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                    return data,count,page_count_value,'/dash/urlToDownload_daywise_Absent?value={}'.format(value)
                          
            
                except:
                    return html.Div(['There was an error processing this file.'])
            
            #Daywise student Absent Student Table
            @app.server.route('/dash/urlToDownload_daywise_Absent')
            def Download_daywise_Absent():
                value = flask.request.args.get('value')
                # create a dynamic csv or file here using `StringIO`
                # (instead of writing to the file system)
                dff = pd.read_csv("Reports/{}.csv".format(value))
                b = dff[(dff["Email"].isnull())].index[1]
                dff = dff.iloc[b+2:,]
                dff_list = []
                for dff_index in dff["Email"].tolist():
                    dff_row = df4_copy[df4_copy[df4_column_list[1]] == dff_index]
                    dff_list.append(dff_row)
                dff = pd.concat(dff_list)
                dff = dff[df4_column_list + ['Zoom Name','Zoom id']]
                dff.columns = ["Registered Name","Email ID",'Your Gender',"College Name",'Whatsapp No ', 'Zoom Name', 'Zoom id']
                upper_list4 = [x.upper().strip() if type(x) == str else x for x in Master_sheet["Email ID"].values.tolist()]
                upper_list5 = [z.upper().strip() if type(z) == str else z for z in Master_sheet["Zoom id"].values.tolist()]
                upper_list6 = [y.upper().strip() if type(y) == str else y for y in dff["Email ID"].values.tolist()]
                master_dataframe = []
                for upper_list6_email in upper_list6:
                    if upper_list6_email in upper_list4:
                        upper_list4_index = upper_list4.index(upper_list6_email)
                        master_dataframe.append(Master_sheet.loc[upper_list4_index,])
                    elif upper_list6_email in upper_list5:
                        upper_list5_index = upper_list5.index(upper_list6_email)
                        master_dataframe.append(Master_sheet.loc[upper_list5_index,])
                master_dataframe = pd.DataFrame(master_dataframe)
                str_io = io.StringIO()
                master_dataframe.to_csv(str_io)
                mem = io.BytesIO()
                mem.write(str_io.getvalue().encode('utf-8'))
                mem.seek(0)
                str_io.close()
                return flask.send_file(mem,
                                       mimetype='text/csv',
                                       attachment_filename='daywaise_Absent_{}.csv'.format(value),
                                       as_attachment=True)
            
            
            
            #Daywise Suspense Data Table
            @app.callback([dash.dependencies.Output('suspence_daywise','data'),
                           dash.dependencies.Output('check_count_suspence','children'),
                           dash.dependencies.Output('suspence_daywise','page_count'),
                           dash.dependencies.Output('my-link_daywise_Suspence', 'href')],
                          [dash.dependencies.Input('dd','value'),
                           dash.dependencies.Input('suspence_daywise', "page_current"),
                           dash.dependencies.Input('suspence_daywise', "page_size")])
            
            def update_fig(value,page_current,page_size):
                try:
                    dff = pd.read_csv("Reports/{}.csv".format(value))
                    a = dff[(dff["Email"].isnull())].index[0]
                    b = dff[(dff["Email"].isnull())].index[1]
                    dff = dff.iloc[a+2:b,]
                    dff.reset_index(inplace = True, drop = True)
                    cleanedList1 = [x for x in dff["Zoom Name"].tolist() if x == x]
                    cleanedList2 = [x for x in dff["Registered Name"].tolist() if x == x]
                    cleanedList_copy = cleanedList1 + cleanedList2
                    cleanedList3 = cleanedList1 + cleanedList2
                    cleanedList3.sort()
                    new_dff = pd.DataFrame(columns=['Zoom Name', 'Email', 'Time', 'Registered Name', 'Gender','College Name', 'WhatsApp No.', 'Zoom id'])
                    for cleanedList3_index,cleanedList3_name in enumerate(cleanedList3):
                        if cleanedList3_name in cleanedList_copy:
                            name_index = cleanedList_copy.index(cleanedList3_name)
                            if dff["Email"][name_index] not in new_dff["Email"].tolist():
                                new_dff = new_dff.append(dff.iloc[name_index,])
                        
                    count = len(new_dff)
                    page_count_value = math.ceil(len(new_dff)/10)
                    data=new_dff.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                    return data,count,page_count_value,'/dash/urlToDownload_daywise_Suspence?value={}'.format(value)
                          
            
                except:
                    return html.Div(['There was an error processing this file.'])
              
           
            
            
            @app.server.route('/dash/urlToDownload_daywise_Suspence')
            def daywise_Suspence():
                value = flask.request.args.get('value')
                # create a dynamic csv or file here using `StringIO`
                # (instead of writing to the file system)
                dff = pd.read_csv("Reports/{}.csv".format(value))
                a = dff[(dff["Email"].isnull())].index[0]
                b = dff[(dff["Email"].isnull())].index[1]
                dff = dff.iloc[a+2:b,]
                dff.reset_index(inplace = True, drop = True)
                cleanedList1 = [x for x in dff["Zoom Name"].tolist() if x == x]
                cleanedList2 = [x for x in dff["Registered Name"].tolist() if x == x]
                cleanedList_copy = cleanedList1 + cleanedList2
                cleanedList3 = cleanedList1 + cleanedList2
                cleanedList3.sort()
                new_dff = pd.DataFrame(columns=['Zoom Name', 'Email', 'Time', 'Registered Name', 'Gender','College Name', 'WhatsApp No.', 'Zoom id'])
                for cleanedList3_index,cleanedList3_name in enumerate(cleanedList3):
                    if cleanedList3_name in cleanedList_copy:
                        name_index = cleanedList_copy.index(cleanedList3_name)
                        if dff["Email"][name_index] not in new_dff["Email"].tolist():
                            new_dff = new_dff.append(dff.iloc[name_index,])
                
                str_io = io.StringIO()
                new_dff.to_csv(str_io)
                mem = io.BytesIO()
                mem.write(str_io.getvalue().encode('utf-8'))
                mem.seek(0)
                str_io.close()
            
                return flask.send_file(mem,
                                       mimetype='text/csv',
                                       attachment_filename='download_daywaise_Suspence_{}.csv'.format(value),
                                       as_attachment=True)

            
            
                
                
             
                
            #All Day Present (This part is related to only for download csv) 
            @app.server.route('/dash/urlToDownload_All_day_present')
            def Download_All_day_present():
                value = flask.request.args.get('value')
                # create a dynamic csv or file here using `StringIO`
                # (instead of writing to the file system)
                Full_data_present = pd.read_csv("Reports/{}.csv".format(value))
                Full_dat_index = Full_data_present[(Full_data_present["Name"].isnull())].index[0]
                Full_data_present1 = Full_data_present.iloc[:Full_dat_index,]
                
                Full_data_present1.rename(columns={'Total':'Total Time(Minutes)','Name':'Registered Name'}, inplace = True )
                upper_list4 = [x.upper().strip() if type(x) == str else x for x in Master_sheet["Email ID"].values.tolist()]
                upper_list5 = [z.upper().strip() if type(z) == str else z for z in Master_sheet["Zoom id"].values.tolist()]
                upper_list6 = [y.upper().strip() if type(y) == str else y for y in Full_data_present1["Email"].values.tolist()]
                                
                master_dataframe = []
                for upper_list6_email in upper_list6:
                    if upper_list6_email in upper_list4:
                        upper_list4_index = upper_list4.index(upper_list6_email)
                        master_dataframe.append(Master_sheet.loc[upper_list4_index,])
                    elif upper_list6_email in upper_list5:
                        upper_list5_index = upper_list5.index(upper_list6_email)
                        master_dataframe.append(Master_sheet.loc[upper_list5_index,])
                master_dataframe = pd.DataFrame(master_dataframe)
                str_io = io.StringIO()
                master_dataframe.to_csv(str_io)
                mem = io.BytesIO()
                mem.write(str_io.getvalue().encode('utf-8'))
                mem.seek(0)
                str_io.close()
                return flask.send_file(mem,
                                       mimetype='text/csv',
                                       attachment_filename='Download_{}.csv'.format(value),
                                       as_attachment=True)
                
                
                
             
            #not present any day table
            @app.callback([dash.dependencies.Output('not_present_table','data'),
                           dash.dependencies.Output('not_present_count','children'),
                           dash.dependencies.Output('not_present_table','page_count')],
                          [dash.dependencies.Input('not_present_table', "page_current"),
                           dash.dependencies.Input('not_present_table', "page_size")])

            def update_fig(page_current,page_size):
                try:
                    #Not Any day present student Table
                    Not_Present_any_col_list = ['Name','Email','Gender','College Name','WhatsApp No.']
                    
                    Not_Present_any = pd.read_csv("Reports/Not_present_any_day.csv")
                    Not_dat_index = Not_Present_any[(Not_Present_any["Name"].isnull())].index[0]
                    Not_Present_any = Not_Present_any.iloc[:Not_dat_index,]
                    count = len(Not_Present_any)
                    page_count_value = math.ceil(len(Not_Present_any)/10),
                    Not_Present_any = Not_Present_any[Not_Present_any_col_list]
                    data=Not_Present_any.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                    return data,count,page_count_value
                          
            
                except:
                    return html.Div(['There was an error processing this file.']) 
            
            #not present any day table   
            @app.server.route('/dash/urlToDownload_Not_present')
            def Download_Not_present():
                value = flask.request.args.get('value')
                # create a dynamic csv or file here using `StringIO`
                # (instead of writing to the file system)
                Not_Present_any_col_list = ['Name','Email','Gender','College Name','WhatsApp No.']
                Not_Present_any = pd.read_csv("Reports/{}.csv".format(value))
                Not_dat_index = Not_Present_any[(Not_Present_any["Name"].isnull())].index[0]
                Not_Present_any = Not_Present_any.iloc[:Not_dat_index,]
                Not_Present_any = Not_Present_any[Not_Present_any_col_list]
                upper_list4 = [x.upper().strip() if type(x) == str else x for x in Master_sheet["Email ID"].values.tolist()]
                upper_list5 = [z.upper().strip() if type(z) == str else z for z in Master_sheet["Zoom id"].values.tolist()]
                upper_list6 = [y.upper().strip() if type(y) == str else y for y in Not_Present_any["Email"].values.tolist()]
                                
                master_dataframe = []
                for upper_list6_email in upper_list6:
                    if upper_list6_email in upper_list4:
                        upper_list4_index = upper_list4.index(upper_list6_email)
                        master_dataframe.append(Master_sheet.loc[upper_list4_index,])
                    elif upper_list6_email in upper_list5:
                        upper_list5_index = upper_list5.index(upper_list6_email)
                        master_dataframe.append(Master_sheet.loc[upper_list5_index,])
                master_dataframe = pd.DataFrame(master_dataframe)
                
                str_io = io.StringIO()
                master_dataframe.to_csv(str_io)
                mem = io.BytesIO()
                mem.write(str_io.getvalue().encode('utf-8'))
                mem.seek(0)
                str_io.close()
            
                return flask.send_file(mem,
                                       mimetype='text/csv',
                                       attachment_filename='download_Not_Present_any.csv',
                                       as_attachment=True)   
                
                
                
            #Atleast present data table
            @app.callback([dash.dependencies.Output('Atleast_present_Data','data'),
                           dash.dependencies.Output('Atleast_present_count','children'),
                           dash.dependencies.Output('Atleast_present_Data','page_count')],
                          [dash.dependencies.Input('Atleast_present_Data', "page_current"),
                           dash.dependencies.Input('Atleast_present_Data', "page_size")])

            def update_fig(page_current,page_size):
                try:
                    #Atleast one present student Table
                    Atleast_one_day_copy = pd.read_csv("Reports/Atleast_one_day_present.csv")
                    Atleast_present_col_list = Atleast_one_day_copy.columns.tolist()
                    Atleast_one_day_index = Atleast_one_day_copy[(Atleast_one_day_copy["Email"].isnull())].index[0]
                    Atleast_one_day_copy = Atleast_one_day_copy.iloc[ : Atleast_one_day_index,]
                    count = len(Atleast_one_day_copy)
                    page_count_value = math.ceil(len(Atleast_one_day_copy)/10),
                    Atleast_one_day_copy = Atleast_one_day_copy[Atleast_present_col_list]
                    data=Atleast_one_day_copy.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                    return data,count,page_count_value
                          
            
                except:
                    return html.Div(['There was an error processing this file.'])
                
                
            #Atleast present data table
            @app.server.route('/dash/urlToDownload_Atleast_one_day')
            def Download_Atleast_one_day():
                value = flask.request.args.get('value')
                # create a dynamic csv or file here using `StringIO`
                # (instead of writing to the file system)
                Atleast_one_day_copy = pd.read_csv("Reports/{}.csv".format(value))
                Atleast_present_col_list = Atleast_one_day_copy.columns.tolist()
                Atleast_one_day_index = Atleast_one_day_copy[(Atleast_one_day_copy["Email"].isnull())].index[0]
                Atleast_one_day_copy = Atleast_one_day_copy.iloc[ : Atleast_one_day_index,]
                Atleast_one_day_copy = Atleast_one_day_copy[Atleast_present_col_list]
                upper_list4 = [x.upper().strip() if type(x) == str else x for x in Master_sheet["Email ID"].values.tolist()]
                upper_list5 = [z.upper().strip() if type(z) == str else z for z in Master_sheet["Zoom id"].values.tolist()]
                upper_list6 = [y.upper().strip() if type(y) == str else y for y in Atleast_one_day_copy["Email"].values.tolist()]
                                
                master_dataframe = []
                for upper_list6_email in upper_list6:
                    if upper_list6_email in upper_list4:
                        upper_list4_index = upper_list4.index(upper_list6_email)
                        master_dataframe.append(Master_sheet.loc[upper_list4_index,])
                    elif upper_list6_email in upper_list5:
                        upper_list5_index = upper_list5.index(upper_list6_email)
                        master_dataframe.append(Master_sheet.loc[upper_list5_index,])
                master_dataframe = pd.DataFrame(master_dataframe)
                
                str_io = io.StringIO()
                master_dataframe.to_csv(str_io)
                mem = io.BytesIO()
                mem.write(str_io.getvalue().encode('utf-8'))
                mem.seek(0)
                str_io.close()
            
                return flask.send_file(mem,
                                       mimetype='text/csv',
                                       attachment_filename='download_Atleast_one_day.csv',
                                       as_attachment=True)    
                
             
             
             
             
                
                
            
            #All day suspence table
            @app.callback([dash.dependencies.Output('Suspence_present_data','data'),
                           dash.dependencies.Output('Suspence_present_count','children'),
                           dash.dependencies.Output('Suspence_present_data','page_count')],
                          [dash.dependencies.Input('Suspence_present_data', "page_current"),
                           dash.dependencies.Input('Suspence_present_data', "page_size")])

            def update_fig(page_current,page_size):
                try:
                    #Atleast one present student Table
                    All_suspence_data = pd.read_csv("Reports/Atleast_one_day_present.csv")
#                    All_suspence_data_col_list = All_suspence_data.columns.tolist()
                    Atleast_one_day_index = All_suspence_data[(All_suspence_data["Email"].isnull())].index[0]
                    All_suspence_data = All_suspence_data.iloc[Atleast_one_day_index+2 : ,]
                    count = len(All_suspence_data)
                    page_count_value = math.ceil(len(All_suspence_data)/10),
                    
#                   Atleast_one_day_copy = Atleast_one_day_copy[Atleast_present_col_list]
                    data=All_suspence_data.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                    return data,count,page_count_value
                          
            
                except:
                    return html.Div(['There was an error processing this file.'])
                
            #All day suspence Export button
            @app.server.route('/dash/urlToDownload_All_day_suspence')
            def Download_All_day_suspence():
                value = flask.request.args.get('value')
                # create a dynamic csv or file here using `StringIO`
                # (instead of writing to the file system)
                All_suspence_data = pd.read_csv("Reports/{}.csv".format(value))
#               All_suspence_data_col_list = All_suspence_data.columns.tolist()
                Atleast_one_day_index = All_suspence_data[(All_suspence_data["Email"].isnull())].index[0]
                All_suspence_data = All_suspence_data.iloc[Atleast_one_day_index+2 : ,]
                
                str_io = io.StringIO()
                All_suspence_data.to_csv(str_io)
                mem = io.BytesIO()
                mem.write(str_io.getvalue().encode('utf-8'))
                mem.seek(0)
                str_io.close()
            
                return flask.send_file(mem,
                                       mimetype='text/csv',
                                       attachment_filename='All_suspence_data.csv',
                                       as_attachment=True)
            
            
            
            
            #Consolited Data
            @app.server.route('/dash/urlToDownload_Consolidated_Analysis')
            def Download_Consolidated_Analysis():
#                value = flask.request.args.get('value')
                # create a dynamic csv or file here using `StringIO`
                # (instead of writing to the file system)
                #Consolidated graph which will be permanent below which tells us atleast one day graph
                consolidated_dataframe2 = df4.copy()
                consolidated_dataframe2 = consolidated_dataframe2.rename(columns={'Zoom id': 'Email'})
                consolidated_dataframe2.drop_duplicates(subset=["Email"], keep='first', inplace=True)
                consolidated_dataframe2.reset_index(inplace = True, drop = True) 
                consolidated_dataframe3 = pd.merge(consolidated_dataframe2, Atleast_one_day_copy, how='left', on=['Email'])
                consolidated_dataframe3.drop(consolidated_dataframe3.iloc[:, 5:10], inplace = True, axis = 1)
                
                consolidated_dataframe3 = consolidated_dataframe3.rename(columns={'Name_x': 'Name',
                                                                                  'Gender_x': 'Gender',
                                                                                  'College Name_x': 'College Name',
                                                                                  'WhatsApp No._x':'WhatsApp No.'})
                consolidated_dataframe3.rename(columns={'Total':'Total Time(Minutes)','Name':'Registered Name'}, inplace = True )
                consolidated_dataframe3_day_list = consolidated_dataframe3.columns.tolist()[5:]
                for consolidated_dataframe3_day_list_name in consolidated_dataframe3_day_list:
                        consolidated_dataframe3[consolidated_dataframe3_day_list_name].fillna(0, inplace=True)
                consolidated_dataframe3 = consolidated_dataframe3.sort_values("Total Time(Minutes)", ascending = False)
                consolidated_dataframe3.reset_index(inplace = True, drop = True)
                upper_list4 = [x.upper().strip() if type(x) == str else x for x in Master_sheet["Email ID"].values.tolist()]
                upper_list5 = [z.upper().strip() if type(z) == str else z for z in Master_sheet["Zoom id"].values.tolist()]
                upper_list6 = [y.upper().strip() if type(y) == str else y for y in consolidated_dataframe3["Email"].values.tolist()]
                                
                master_dataframe = []
                for upper_list6_email in upper_list6:
                    if upper_list6_email in upper_list4:
                        upper_list4_index = upper_list4.index(upper_list6_email)
                        master_dataframe.append(Master_sheet.loc[upper_list4_index,])
                    elif upper_list6_email in upper_list5:
                        upper_list5_index = upper_list5.index(upper_list6_email)
                        master_dataframe.append(Master_sheet.loc[upper_list5_index,])
                master_dataframe = pd.DataFrame(master_dataframe)

                
                str_io = io.StringIO()
                master_dataframe.to_csv(str_io)
                mem = io.BytesIO()
                mem.write(str_io.getvalue().encode('utf-8'))
                mem.seek(0)
                str_io.close()
            
                return flask.send_file(mem,
                                       mimetype='text/csv',
                                       attachment_filename='download_Consolidated_Analysis.csv',
                                       as_attachment=True)
            
            
    
    
    
            #Search button
            @app.callback(dash.dependencies.Output('filter_y','type'),[dash.dependencies.Input('filter_x','value')])
            def drop_value(value):
                if value == 1:
                    type = "text"
                    return type
                elif value == 2:
                    type = "email"
                    return type
                elif value == 3:
                    type = "number"
                    return type
                elif value == 4:
                    type = "text"
                    return type
            
            
            #search data
            @app.callback(dash.dependencies.Output('table', 'data'),
                [dash.dependencies.Input('filter_x','value'),
                 dash.dependencies.Input('filter_z','value'),
                 dash.dependencies.Input('table', "page_current"),
                 dash.dependencies.Input('table', "page_size"),
                 dash.dependencies.Input('button_chart', 'n_clicks')],
                [dash.dependencies.State('filter_y', 'value')])
            
            def update_figure(value1,value2,page_current,page_size,n_clicks, filename):
                df5 = consolidated_dataframe3
                if value2 == 1:
                    if value1 == 3:
            #            if type(filename) == int:
                            filename = str(filename)
                            filename_list = []
                            for index,number in enumerate(df5["WhatsApp No."].tolist()):
                                if filename in str(number):
                                    if str(number).startswith(filename):
                                            filename_list.append(index)
                            df6 = []
                            for i in filename_list:
                                df6.append(df5.iloc[i])
                            df7 = pd.DataFrame(df6)
                            data = df7.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                            return data
                    elif value1 == 1:
            #            if filename.isalpha():
                            filename = filename.upper()
                            filename_list = []
                            for index,name in enumerate(df5["Registered Name"].tolist()):
                                if filename in name:
                                    name1 = name.split()
                                    for name1_part in name1:
                                        if name1_part.startswith(filename):
                                            filename_list.append(index)
                                            break
                            df6 = []
                            for i in filename_list:
                                df6.append(df5.iloc[i])
                            df7 = pd.DataFrame(df6)
                            data = df7.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                            return data
                
                    elif value1 == 2:
            #            if filename.isalnum() or filename.isalpha() or filename.isdigit() or "@" in filename or "." in filename:
                            filename = filename.upper()
                            filename_list = []
                            for index,email in enumerate(df5["Email"].tolist()):
                                    if email.upper().startswith(filename):
                                        filename_list.append(index)
                                        
                            df6 = []
                            for i in filename_list:
                                df6.append(df5.iloc[i])
                            df7 = pd.DataFrame(df6)
                            data=df7.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                            return data
                    
                    
                    elif value1 == 4:
            #            if filename.isalnum() or filename.isalpha() or filename.isdigit():
                            filename = filename.upper()
                            filename_list = []
                            for index,name in enumerate(df5["College Name"].tolist()):
                                if filename in name.upper():
                                    name1 = name.upper().split()
                                    for name1_part in name1:
                                        if name1_part.startswith(filename):
                                            filename_list.append(index)
                                            break
                            df6 = []
                            for i in filename_list:
                                df6.append(df5.iloc[i])
                            df7 = pd.DataFrame(df6)
                            data = df7.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                            return data
                elif value2 == 2:
                    if value1 == 3:
            #            if type(filename) == int:
                            filename = str(filename)
                            filename_list = []
                            for index,number in enumerate(df5["WhatsApp No."].tolist()):
                                if filename in str(int(number)):
                                    if str(int(number)).endswith(filename):
                                            filename_list.append(index)
                            df6 = []
                            for i in filename_list:
                                df6.append(df5.iloc[i])
                            df7 = pd.DataFrame(df6)
                            data = df7.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                            return data
                    elif value1 == 1:
            #            if filename.isalpha():
                            filename = filename.upper()
                            filename_list = []
                            for index,name in enumerate(df5["Registered Name"].tolist()):
                                if filename in name:
                                    name1 = name.split()
                                    for name1_part in name1:
                                        if name1_part.endswith(filename):
                                            filename_list.append(index)
                                            break
                            df6 = []
                            for i in filename_list:
                                df6.append(df5.iloc[i])
                            df7 = pd.DataFrame(df6)
                            data = df7.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                            return data
                
                    elif value1 == 2:
            #            if filename.isalnum() or filename.isalpha() or filename.isdigit() or "@" in filename or "." in filename:
                            filename = filename.upper()
                            filename_list = []
                            for index,email in enumerate(df5["Email"].tolist()):
                                    if email.upper().endswith(filename):
                                        filename_list.append(index)
                                        
                            df6 = []
                            for i in filename_list:
                                df6.append(df5.iloc[i])
                            df7 = pd.DataFrame(df6)
                            data=df7.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                            return data
                    
                    
                    elif value1 == 4:
            #            if filename.isalnum() or filename.isalpha() or filename.isdigit():
                            filename = filename.upper()
                            filename_list = []
                            for index,name in enumerate(df5["College Name"].tolist()):
                                if filename in name.upper():
                                    name1 = name.upper().split()
                                    for name1_part in name1:
                                        if name1_part.endswith(filename):
                                            filename_list.append(index)
                                            break
                            df6 = []
                            for i in filename_list:
                                df6.append(df5.iloc[i])
                            df7 = pd.DataFrame(df6)
                            data = df7.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                            return data          
                else:
                    if n_clicks:
                        data = df5.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                        return data
             
             
                
            #difference of daywise present data    
            @app.callback(dash.dependencies.Output('diff_head','children'),[dash.dependencies.Input('last_dd','value')])
            def update_fig2(value):  
                return value
                
            #difference of daywise present data
            @app.callback([dash.dependencies.Output('diff_daywise','data'),
                           dash.dependencies.Output('check_count_diff','children'),
                           dash.dependencies.Output('diff_daywise','page_count')],
                          [dash.dependencies.Input('last_dd','value'),
                           dash.dependencies.Input('diff_daywise', "page_current"),
                           dash.dependencies.Input('diff_daywise', "page_size")])
            
            def update_fig(value,page_current,page_size):
                try:
                    v_list = value.split(" - ")
                    if v_list[0] == 'Registered':
                        dff1 = df4_copy
                        dff2 = pd.read_csv("Reports/{}.csv".format(v_list[-1]))
                        dff2_present_index = dff2[dff2["Zoom Name"].isnull()].index.tolist()[0]
                        present_data2 = dff2.iloc[:dff2_present_index,]
                        
                        diff_data = []
                        for diff_index,diff_email in enumerate(dff1["Your Gmail ID"].tolist()):
                            if diff_email not in present_data2["Zoom id"].tolist():
                                diff_data.append(dff1.iloc[diff_index,])
                        diff_data = pd.DataFrame(diff_data) 
                        diff_data["Time"] = np.nan
                        diff_data.reset_index(inplace = True, drop = True)
                        diff_data = diff_data[['Zoom Name','Your Gmail ID','Time','Name',
                                               'Gender','College Name','WhatsApp No.','Zoom id']]
                        diff_data = diff_data.rename(columns={'Your Gmail ID':'Email',
                                                              'Name':'Registered Name'})
                        count = len(diff_data)
                        page_count_value = math.ceil(len(diff_data)/10)
                        data=diff_data.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                        return data,count,page_count_value
                    
                    else:
                        dff1 = pd.read_csv("Reports/{}.csv".format(v_list[0]))
                        dff1_present_index = dff1[dff1["Zoom Name"].isnull()].index.tolist()[0]
                        present_data1 = dff1.iloc[:dff1_present_index,]
                        dff2 = pd.read_csv("Reports/{}.csv".format(v_list[1]))
                        dff2_present_index = dff2[dff2["Zoom Name"].isnull()].index.tolist()[0]
                        present_data2 = dff2.iloc[:dff2_present_index,]
                        
                        diff_data = []
                        for diff_index,diff_email in enumerate(present_data1["Zoom id"].tolist()):
                            if diff_email not in present_data2["Zoom id"].tolist():
                                diff_data.append(present_data1.iloc[diff_index,])
                        diff_data = pd.DataFrame(diff_data) 
                        diff_data = diff_data.sort_values("Time", ascending = False)
                        diff_data.reset_index(inplace = True, drop = True)
                       
                        count = len(diff_data)
                        page_count_value = math.ceil(len(diff_data)/10)
                        data=diff_data.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
                        return data,count,page_count_value
                          
            
                except:
                    return html.Div(['There was an error processing this file.'])
            
            
            if __name__ == '__main__':
                Timer(1, open_browser).start();
                app.run_server()
    
    
    
    else:
        print("Warning:\nPlease Check Meeting Id & Match.\nAnd also check that in directory missing Excel file")
    
    
else:
    print("Internet Disconnected")





    
    
    

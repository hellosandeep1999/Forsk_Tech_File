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


Meeting_id = int(input("Please Enter your Meeting Id: "))
#you want to UI or not
UI_run = input("Do you want to See UI: ")



#Making a directory by name Reports
if not os.path.exists("Reports"):
    os.makedirs("Reports")
#Creating the log file
LOG_FILENAME = 'Reports/{}.log'.format(Meeting_id)
logging.basicConfig(filename=LOG_FILENAME, filemode='w', format='%(asctime)s - %(name)s - %(lineno)d - %(message)s',level=logging.DEBUG)



SCOPES = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
credentials = Credentials.from_service_account_file('Creds.json', scopes=SCOPES)
client = gspread.authorize(credentials)



#This is Mark down text which will printed by softcoded.
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

first_line = "## "+markdown_list[0]
last_lines = "#### " + "\n#### ".join(markdown_list[1:])[:-6]


markdown_text = '''
{}
{}
'''.format(first_line,last_lines)



print('Please wait we are reading master sheet...')
sheet = client.open("Master").sheet1



#whats your system I want to know by platform.system()
using_system = platform.system()

 
logging.warning('logging file Starts from here')
logging.warning('You entered Metting id  - %d',Meeting_id)
logging.warning('Your Used platform - %s',using_system)


#some address which we will define here and use in whole program
win_cloud_dir = "c:/Users/Cloud"                 #for windows
win_master_file = "c:/Users/Cloud/Master.csv"   #for windows

mac_cloud_dir = "/Users/sylvester/Cloud"                  #for mac
mac_master_file = "/Users/sylvester/Cloud/Master.csv"    #for mac


Inside_report_excel = "Reports/{}.csv".format(Meeting_id)  #This is for Excel sheet which is inside in Report folder
outside_excel = "{}.xlsx".format(Meeting_id)                #outside excel sheet

#pandas gives a lot of warnings 
pd.options.mode.chained_assignment = None



extension1 = 'csv'
extension2 = 'xlsx'
All_csv_files = glob.glob('*.{}'.format(extension1))
All_excel_files = glob.glob('*.{}'.format(extension2))
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
    
    
    #Making a directory by name Reports
    if not os.path.exists("Reports"):
        os.makedirs("Reports")

                                                                                          
                                                                                                      
    #this section will be for Master sheet which have all data

    def window_check_make_Master(): #function for windows c drive cheking and make a master sheet
        if sheet.acell('A1').value == '':
            Master_sheet_columns_list = ["Timestamp","UTR No ( PhonePe)","Title","Registered Name",
                     "Designation","Email ID","Mobile No.",'Your Gender',"College Name",
                     'Whatsapp No ',"Branch/ Department","Current Semester","College City",
                     'Status','Mode','Payee Name/New ID','Calling Responses',
                      'Zoom id','Matched', 'Zoom Name']
            for Master_sheet_columns_index,Master_sheet_columns_name in enumerate(Master_sheet_columns_list):
                Master_sheet_columns_ind = Master_sheet_columns_index + 1
                sheet.update_cell(1,Master_sheet_columns_ind,Master_sheet_columns_name)
        Master_sheet_dict = sheet.get_all_values()
        Master_sheet = pd.DataFrame(Master_sheet_dict)
        Master_sheet.columns = Master_sheet.iloc[0]
        Master_sheet.drop(Master_sheet.index[0],inplace=True)
        Master_sheet.reset_index(inplace = True, drop = True) 
        return Master_sheet
    
    
    def mac_check_make_Master(): #function for mac and linux c drive cheking and make a master sheet
        if sheet.acell('A1').value == '':
            Master_sheet_columns_list = ["Timestamp","UTR No ( PhonePe)","Title","Registered Name",
                     "Designation","Email ID","Mobile No.",'Your Gender',"College Name",
                     'Whatsapp No ',"Branch/ Department","Current Semester","College City",
                     'Status','Mode','Payee Name/New ID','Calling Responses',
                      'Zoom id','Matched', 'Zoom Name']
            for Master_sheet_columns_index,Master_sheet_columns_name in enumerate(Master_sheet_columns_list):
                Master_sheet_columns_ind = Master_sheet_columns_index + 1
                sheet.update_cell(1,Master_sheet_columns_ind,Master_sheet_columns_name)
        Master_sheet_dict = sheet.get_all_values()
        Master_sheet = pd.DataFrame(Master_sheet_dict)
        Master_sheet.columns = Master_sheet.iloc[0]
        Master_sheet.drop(Master_sheet.index[0],inplace=True)
        Master_sheet.reset_index(inplace = True, drop = True) 
        return Master_sheet
    
    
    #according to our system function will be run
     #if windows our system
    if using_system == 'Windows':                        
        Master_sheet = window_check_make_Master()
     
    #if Mac or linux our system    
    if using_system == 'Darwin' or using_system == 'Linux':                         
        Master_sheet = mac_check_make_Master()
    





    #This Part for Reconciliation and it will check both Excel sheet if any new data than he will be update
    def Reconcilation_process():
       Inner_file = pd.read_csv("{}".format(Inside_report_excel))
       total_column2 = len(Inner_file.columns.tolist())
       Inner_file.dropna(thresh=total_column2-8,inplace=True)
       Inner_file.reset_index(inplace = True, drop = True)
       logging.warning('Inside of report meeting id file Shape - %s',Inner_file.shape)
       
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
    
    
       Inner_file_Email_list = Inner_file[mail_id_column_name[0]].values.tolist()
       outer_file_Email_list = outer_file[mail_id_column_name[0]].values.tolist()
    
       Reconcil_dataframe = pd.DataFrame(columns=Inner_file.columns.tolist())
       Reconcil_count = 0
       for out_Email_index,out_Email in enumerate(outer_file_Email_list):
           if out_Email in Inner_file_Email_list:
               INNa_index = Inner_file[Inner_file[mail_id_column_name[0]] == str(out_Email)].index[0]
               Reconcil_dataframe = Reconcil_dataframe.append(outer_file.iloc[out_Email_index,])
               Reconcil_dataframe["Zoom id"][Reconcil_count] = Inner_file["Zoom id"][INNa_index]
               Reconcil_dataframe["Matched"][Reconcil_count] = Inner_file["Matched"][INNa_index]
               Reconcil_dataframe["Zoom Name"][Reconcil_count] = Inner_file["Zoom Name"][INNa_index]
               Reconcil_count += 1
           else:
              Reconcil_dataframe = Reconcil_dataframe.append(outer_file.iloc[out_Email_index,])
              Reconcil_count += 1
       return Reconcil_dataframe 
       
       
    if os.path.exists("{}".format(Inside_report_excel)):
       Reconcil_dataframe = Reconcilation_process()
       Reconcil_dataframe.to_csv("{}".format(Inside_report_excel), index = False)
    
    
    
    
    if os.path.exists("{}".format(Inside_report_excel)):
        df4 = pd.read_csv("{}".format(Inside_report_excel))
        total_column = len(df4.columns.tolist())
        df4.dropna(thresh=total_column-8,inplace=True)
        df4_copy = df4.copy()
    else:
        df4 = pd.read_excel("{}".format(outside_excel))
        total_column = len(df4.columns.tolist())
        df4.dropna(thresh=total_column-8,inplace=True)
        df4_copy = df4.copy()
    
    
    if "Zoom id" not in df4_copy.columns.tolist():
        df4_copy["Zoom id"] = np.nan

    
    if "Matched" not in df4_copy.columns.tolist():
        df4_copy["Matched"] = np.nan
    
    
    
    #files_name is just a copy for all csv files
    All_csv_files2 = [check2_file for check2_file in All_csv_files if str(Meeting_id) in check2_file]
    All_csv_files2 = sorted(All_csv_files2)
    logging.warning('After sorted all csv files - %s',All_csv_files2)
    files_name = All_csv_files2

        
    
    #File_Total is tell us that how many files are exists
    File_Total = len(files_name)
    
    
    #here we are choose column names which are usefull for our script
    df4_column_list = [] 
    def make_main_df4_column_list(df4_column1):
        for column_name in df4.columns.tolist():
            if df4_column1 in column_name.upper():
                df4_column_list.append(column_name)
                break
    check_list1 = ['NAME','MAIL','GENDER','COLLEGE','WHATSAPP']
    for check_list1_name in check_list1:
                make_main_df4_column_list(check_list1_name)
            
    logging.warning('Choosed column list of main meeting id sheet - %s',df4_column_list)
        
    
    df4 = df4[df4_column_list]
    
    
        
        
    df4.columns = ["Name", "Email", "Gender", "College Name", "WhatsApp No."] 
    
      
    
    #for full.csv 
    dataframe_name = []  
    for file_i in range(File_Total):
        a = "data"+str(file_i)
        dataframe_name.append(a)
        
      
    prt_to_reg = pd.DataFrame(columns=['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.','Zoom id'])
      
      
    t2 = pd.DataFrame(columns=['Name', 'Email', 'Gender', 'College Name', 'WhatsApp No.'])
    
    
    #Before updated sheet
    before_updated_day = []  
    for file_i in range(File_Total):
        a = "day_"+str(file_i)
        before_updated_day.append(a)
    
    logging.warning('before updated day list - %s',before_updated_day)  
    
#Main for loop start from here making daywise csv files  
    for file_index,file_name in enumerate(files_name):
        
          
        File_Name = file_name
        
        file_number = File_Name[4]
        
        df1 = pd.read_csv("{}".format(File_Name))
        logging.warning('Day{} Participants data Shape - %s'.format(file_index),df1.shape)
        df1 = df1[df1.columns.tolist()]
        
        df1.columns = ["Name", "Email", "Time"]
        
        prt_to_reg = pd.DataFrame(columns=['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.','Zoom id'])
        
        
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
        
    #   if file == 0:
    #        df4_copy[df4_column_list[0]] = [name.upper() for name in df4_copy[df4_column_list[0]].tolist()]
    #        data_list = df4_copy[df4_column_list[0]].tolist()
    #        df4_copy[df4_column_list[0]] = removing(data_list)
        
        
        prt_to_reg["Zoom id"] = np.nan
        
        #Update sheet using master sheet (By Registered Email id)
        Master_sheet_Email_list2 = Master_sheet["Email ID"].values.tolist()
        df4_copy_email_list2 = df4_copy[df4_column_list[1]].values.tolist()
        for df4_copy_email2_index,df4_copy_email2 in enumerate(df4_copy_email_list2):
            for Master_sheet_Email_index,Master_sheet_Email in enumerate(Master_sheet_Email_list2):
                if str(df4_copy_email2).upper().strip() == str(Master_sheet_Email).upper().strip():
                    df4_copy.loc[df4_copy_email2_index,"Zoom id"] = Master_sheet["Zoom id"][Master_sheet_Email_index]
                    df4_copy.loc[df4_copy_email2_index,"Matched"] = True
                    df4_copy.loc[df4_copy_email2_index,"Zoom Name"] = Master_sheet["Zoom Name"][Master_sheet_Email_index]
                    break
           
            
        
        #Update sheet using master sheet (By Zoom Email id)
        Master_sheet_zoom_Email_list2 = Master_sheet["Zoom id"].values.tolist()
        df4_copy_email_list3 = df4_copy[df4_column_list[1]].values.tolist()
        for df4_copy_email3_index,df4_copy_email3 in enumerate(df4_copy_email_list3):
            for Master_zoom_Email_index,Master_zoom_Email in enumerate(Master_sheet_zoom_Email_list2):
                if str(df4_copy_email3).upper().strip() == str(Master_zoom_Email).upper().strip():
                    df4_copy.loc[df4_copy_email3_index,"Zoom id"] = Master_sheet["Zoom id"][Master_zoom_Email_index]
                    df4_copy.loc[df4_copy_email3_index,"Matched"] = True
                    df4_copy.loc[df4_copy_email3_index,"Zoom Name"] = Master_sheet["Zoom Name"][Master_zoom_Email_index]
                    break
   
        
        
        
        zoom_list = df1['Name'].values.tolist()
        zoom_Email_list = df1['Email'].values.tolist()
        data1_list = df4['Name'].values.tolist()
        data1_Email_list = df4['Email'].values.tolist()
        
        
        #Mater sheet indexing(first we will check in our master sheet for details)
#        master_sheet_Email_list = Master_sheet['Zoom id'].values.tolist()
#        master_sheet_store = []
#        zoom_store1 = []
        
        
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
            
        
        #data checking from participants to registered.
        for zoom_index, zoom_name in enumerate(zoom_list):
            counter = 0
#            if str(zoom_Email_list[zoom_index]) in master_sheet_Email_list:
#                master_index = Master_sheet['Zoom id'].values.tolist().index(str(zoom_Email_list[zoom_index]))
#                master_sheet_store.append(master_index)
#                zoom_store1.append(zoom_index)
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
                
        
        #this section will right the supence entries by Matser sheet.
#        k = 0
#        for v in master_sheet_store:
#            while k < len(zoom_store1):
#                value1 = zoom_store1[k]
#                prt_to_reg = prt_to_reg.append({'Zoom Name': df1['Name'][value1], 
#                                                'Email': df1['Email'][value1], 
#                                                'Time': df1['Time'][value1],
#                                                'Registered Name': Master_sheet["Registered Name"][v].upper(),
#                                                'Gender': Master_sheet["Your Gender"][v],
#                                                'College Name': Master_sheet["College Name"][v],
#                                                'WhatsApp No.': Master_sheet["Whatsapp No "][v],
#                                                'Zoom id': Master_sheet["Email ID"][v]}, ignore_index=True)
#                
#                k += 1
#                break
           
    
    
        #If data is matched than student will get present. 
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
            
        prt_to_reg.drop_duplicates(subset='Email',keep='last', inplace=True)
        
        
        
        
        
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
#                    change_list = list(set_intersection)
#                        store.append(change_list[0])
#                        zoom_store.append(zoom_index)
#                        f["Zoom id"][zoom_index] = df4["Email"][change_list[0]]
#                        df4_copy["Zoom id"][change_list[0]] = f['Email'][zoom_index]
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
                        data1_name_func(data1_name)
                        
                        if zoom_list_filter.count(data1_name) > 1:
                            suspence_store_t2.append(data1_index)
                            break
                        else:

                            break
                              
                else:
                    name_cheking_t2(data1_name,name_cheking_t2)
                    
            else:
                name_cheking_t2(data1_name,name_cheking_t2)
        
        
        
        
        #making dataframe for t2
        suspence_t2 = []
        
        for index in suspence_store_t2:
            suspence_t2.append(df4.iloc[index,])
        
        suspence_t2 = pd.DataFrame(suspence_t2)
        suspence_t2.reset_index(inplace = True, drop = True)  
        
        
        
        
    
        #daywise suspence data
        def suspence_merge_data():
            merge = pd.merge(suspence_t1, suspence_t2, how='outer', on='Email')
            merge = merge[['Name_x', 'Email', 'Time', 'Name_y', 'Gender', 'College Name', 'WhatsApp No.']]
            merge.columns = ['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.']
            merge["Zoom id"] = np.nan
            return merge
        
    
    
    
        #Daywise present data
        def present_data(prt_to_reg):
            prt_to_reg = prt_to_reg.sort_values("Time", ascending = False)
            prt_to_reg.reset_index(inplace = True, drop = True) 
            
            prt_to_reg=prt_to_reg.append(pd.Series("nan"), ignore_index=True)
            prt_to_reg=prt_to_reg.drop([0],axis=1) 
            new_row={"Zoom Name":"Suspense","Email":"Data"}
            prt_to_reg = prt_to_reg.append(new_row,ignore_index=True)   
            return prt_to_reg
        
        
        
        #for full.csv
        my_copy = present_data(prt_to_reg)[:-2].copy()
        dataframe_name[file_index] = my_copy
        dataframe_name[file_index] = dataframe_name[file_index][["Zoom Name","Zoom id","Time"]]
        dataframe_name[file_index].columns = ["Name", "Zoom id", "Time"]
        dataframe_name[file_index].loc[:,"Date"] = file_index+1
        
        
        frame=[present_data(prt_to_reg),suspence_merge_data()]
        result=pd.concat(frame)
        result.reset_index(inplace = True, drop = True)
        logging.warning('Day{} shape(present & suspence) - %s'.format(file_index),result.shape)
        #Now we will just store the result data in --> before_updated_day
        before_updated_day[file_index] = result
        
     
             
       
    df4_copy["Matched"] = df4_copy["Matched"].fillna(False)
        
        
    #Now code for creating daywise file and seprate the absent section
        
    for day_index in range(File_Total):
        null_index1 = before_updated_day[day_index][before_updated_day[day_index]["Zoom Name"].isnull()].index.tolist()[0]
        null_index2 = before_updated_day[day_index][before_updated_day[day_index]["Zoom Name"].isnull()].index.tolist()[1]
        
        #Present data
        def only_present_data(day_index,null_index1):
            present_data = before_updated_day[day_index].iloc[:null_index1,]
            present_data = present_data.append(pd.Series("nan"), ignore_index=True)
            present_data = present_data.drop([0],axis=1) 
            new_row={"Zoom Name":"Suspense","Email":"Data"}
            present_data = present_data.append(new_row,ignore_index=True)
            return present_data
        present_data = only_present_data(day_index,null_index1)
        logging.warning('Day{} only present data shape- %s'.format(day_index),present_data.shape)
        
        #unregistered section
        t1_suspence = before_updated_day[day_index].iloc[null_index1+2 : null_index2,]
        t1_suspence.dropna(subset=['Zoom Name', 'Email','Time'],inplace=True)
        
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
            t2_real_suspence = pd.DataFrame(columns=['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.','Zoom id'])
            t2_real_suspence.reset_index(inplace = True, drop = True)
        else:
            t2_real_suspence = pd.DataFrame(t2_real_suspence)
            t2_real_suspence.reset_index(inplace = True, drop = True)
    
        #copy of t2_real_suspence for all suspence
        t2_real_suspence_copy = t2_real_suspence.copy()
    
    
        #daywise suspence data
        def real_suspence_data_merge():
            merge = pd.merge(t1_suspence, t2_real_suspence, how='outer', on='Email')
            merge = merge[['Zoom Name_x', 'Email', 'Time_x', 'Registered Name_y', 'Gender_y', 'College Name_y', 'WhatsApp No._y','Zoom id_y']]
            merge.columns = ['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.','Zoom id']
        
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
            return t2_absent
        
        if len(t2_absent) == 0:
            t2_absent = pd.DataFrame(columns=['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.','Zoom id'])
        else:
            t2_absent = t2_absent_func(t2_absent)
        
        logging.warning('Day{} only Absent data shape- %s'.format(day_index),t2_absent_func(t2_absent).shape)
        #work for all suspence data
        real_suspence = t2_real_suspence_copy[['Registered Name', 'Email', 'Gender', 'College Name', 'WhatsApp No.']]   
        real_suspence.columns = ['Name','Email','Gender','College Name','WhatsApp No.']
        t2 = t2.append(real_suspence) 
                           
    
        daywise_frame = [present_data,real_suspence_data_merge(),t2_absent]
        daywise_result = pd.concat(daywise_frame)
        daywise_result.reset_index(inplace = True, drop = True)
    
        #this number will print on daywise file name
        daynumber = (int(file_number) - int(File_Total)) + (day_index+1)
        
        daywise_result.to_csv("Reports/Day{}.csv".format(daynumber), index = False)
    
  
    
    
#till here we have completed our daywise data 
#=============================================================
#from here we will generate 4 extra details files
    
         
    #code for suspence data
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
    
    
    #now we will count that how many days exist our scipt
    def days_count_func():
        day_count = ["Zoom Name","Email"]
        for day_index in range(len(t1_time_column)):
            day_count.append("Day{}".format(day_index))
        
        day_count.append("Total")
        return day_count
    t1.columns = days_count_func()
    
    
    
    t1["Total"] = 0
    for daywise_index in range(len(t1_time_column)):
        t1["Total"] += t1["Day{}".format(daywise_index)]
    
    t1 = t1.sort_values("Total", ascending = False)
    
    
    t2.drop_duplicates(subset=["Email"], keep='first', inplace=True)
    
    #using this function we will generate all suspence entries and use every section
    def all_suspence_data(t1,t2):
        suspence_merge = pd.merge(t1,t2, how='outer', on='Email')
        suspence_merge_list = ['Name', 'Gender', 'College Name', 'WhatsApp No.','Zoom Name','Email']
        suspence_merge_list = suspence_merge_list + t1.columns.tolist()[2:]
        suspence_merge = suspence_merge[suspence_merge_list]  #now we will add this data into everyday and atleast present
        return suspence_merge    
    
    suspence_merge = all_suspence_data(t1,t2)  #using all_suspence_data(t1,t2) function
    logging.warning('Total suspence shape- %s',suspence_merge.shape) 
    
    
    
    
    
    
    
    #========================
    #work start for full.csv
    
    
    
        
    df4 = df4.rename(columns={'Email': 'Zoom id'})
    
    
    
    
    #every day present
    def make_zoom(dataframe_name):
        zoom = pd.concat(dataframe_name)
        #Deleting the columns with no value
        zoom = zoom.dropna(how = "all")
        zoom.reset_index(inplace = True, drop = True)     
        return zoom
    
    zoom = make_zoom(dataframe_name) #using make_zoom(dataframe_name) function here
        
    emails = zoom["Zoom id"].tolist()
    
    def Dates_indexing():
        ats = []
        for at_index in range(1,(File_Total+1)):
            b = "at" + str(at_index)
            ats.append(b)
        return ats
    
    ats = Dates_indexing()
        
    index = 0
    while index < File_Total:
        ats[index] = [0] * len(emails)
        index += 1
    
    
    
    zoom_names = zoom["Name"].tolist()
    zoom_durations = zoom["Time"].tolist()
    zoom_dates = zoom["Date"].tolist()
    
    
    for dates_index in range(1,(File_Total+1)):
        for index,name in enumerate(zoom_names): 
            for zindex, zname in enumerate(zoom_names):
                if str(name) in str(zname):
                    if zoom_dates[zindex] == dates_index:
                        ats[(dates_index-1)][index] = zoom_durations[zindex]
        
    
           
    
    total = [0] * len(zoom_names)
    
    
    
    for index,name in enumerate(zoom_names):
          index_at = 0
          while index_at < File_Total:
               if index_at == 0:
                    total[index] = ats[index_at][index] 
               elif index_at > 0:
                    total[index] += ats[index_at][index]
               index_at += 1
     
              
    
    ats.insert(0, zoom_names)
    ats.insert(1, emails)
    cal = 2 + File_Total
    ats.insert(cal, total)
    #z is a dataframe which have our compelete days total time (we need to transpose of dataset here)
    z = pd.DataFrame(ats)
    
    
    #transpose of our dataset
    def datafram_transpose(z):
        z = z.T  #transpose the dataframe
        return z
    
    z = datafram_transpose(z) #using datafram_transpose(z) function
    
    
    #z dataframe not have column names so we will give here names
    def z_columns_list():
        column_list = ["Zoom Name", "Email"]
        for column_list_index in range(File_Total):
            day_name = "Day{}".format(column_list_index)
            column_list.append(day_name)
        
        column_list.append("Total")
        return column_list
    
    z.columns = z_columns_list()  #using z_columns_list() function
    
    
    z.drop_duplicates(inplace = True) #z dataframe have a lot of duplicate queries so we need to remove it
    z.reset_index(inplace = True, drop = True)    #reset the rows indexing
       
    
     
    z = z.rename(columns={'Email': 'Zoom id'})
    #final dataframe have more matching detail of participants
    final = z.merge(right = df4, how = "left", on = "Zoom id", suffixes=('', 'Registered'))
    
    
    
    def final_dataframe_column_list():
        final_list = ['Name', 'Gender', 'College Name', 'WhatsApp No.','Zoom Name', 'Zoom id']
        for final_list_index in range(File_Total):
            day_name = "Day{}".format(final_list_index)
            final_list.append(day_name)
        
        final_list.append("Total")
        return final_list
    
    
    final = final[final_dataframe_column_list()]
    
    final = final.sort_values("Total", ascending = False) #sorting of total column
    
    final_copy = final.copy()  #this copy will be most use for "Reports/Not_present_any_day.csv"
    
    
    
    
    
    
    
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
        for Atleast_list_index in range(File_Total):
            At_day_name = "Day{}".format(Atleast_list_index)
            Atleast_one_day_list.append(At_day_name)
        
        Atleast_one_day_list.append("Total")
        return Atleast_one_day_list
    logging.warning('Atleast one day column list - %s',Atleast_one_day_column_list())    
    
    #choose columns according to our need
    Atleast_one_day = Atleast_one_day[Atleast_one_day_column_list()] #using Atleast_one_day_column_list() function 
    
    
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
    
    Atleast_one_day.to_csv("Reports/Atleast_one_day_present.csv", index = False)    
        
     
         
    
    
    
          
    #code for everyday present who are register and join every day  
    def everyday_present(final):   
        for last_index in range(File_Total):
            final = final[(final["Day{}".format(last_index)] > 0)]
            
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
        for final_list_index in range(File_Total):
            final_day_name = "Day{}".format(final_list_index)
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
    df4_copy.to_csv("{}".format(Inside_report_excel), index = False)
                            
      

    #Master sheet                  
    #Add the data in Master sheet (if we have new data)
    Matching_data = df4_copy[df4_copy["Matched"] == True]
    Matching_data.reset_index(inplace = True, drop = True)
    Matching_data_email_list = Matching_data[df4_column_list[1]].values.tolist()
    upper_list = [x.upper().strip() for x in Master_sheet["Email ID"].values.tolist()]
    upper_list2 = [z.upper().strip() for z in Master_sheet["Zoom id"].values.tolist()]
    row_inc = 0
    for Matching_data_email_index,Matching_data_email in enumerate(Matching_data_email_list):
        if str(Matching_data_email).upper().strip() not in upper_list and str(Matching_data_email).upper().strip() not in upper_list2 and Matching_data["Zoom id"][Matching_data_email_index].upper().strip() not in upper_list and Matching_data["Zoom id"][Matching_data_email_index].upper().strip() not in upper_list2:                                                                       
            
            Master_columns_list = []
            def make_Master_columns_list(column_n):
                for column_name1 in df4_copy.columns.tolist():
                    if column_n in column_name1.upper():
                        Master_columns_list.append(Matching_data[column_name1][Matching_data_email_index])
                        break
                else:
                    Master_columns_list.append(np.nan)
            
            check_list_ = ["TIMESTAMP","UTR","TITLE","NAME","DESIGNATION",'MAIL','MOBILE','GENDER','COLLEGE',
                          "WHATSAPP","DEPARTMENT","SEM","CITY","STATUS",'MODE','PAYEE','CALLING',
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
                          'Status' : Master_columns_list[13],
                          'Mode' : Master_columns_list[14],
                          'Payee Name/New ID' : Master_columns_list[15],
                          'Calling Responses' : Master_columns_list[16],
                          'Zoom id' : Master_columns_list[17],
                          'Matched' : Master_columns_list[18],
                          'Zoom Name' : Master_columns_list[19]
                          }
            Master_sheet = Master_sheet.append(dictionary, ignore_index=True)
    
    #If in any zoom id empty than we will fill that
    for Master_sheet_empty_index,Master_sheet_empty in enumerate(Master_sheet["Email ID"].values.tolist()):
        if Master_sheet["Zoom id"][Master_sheet_empty_index] == '':
            Master_sheet["Zoom id"][Master_sheet_empty_index] = Master_sheet_empty

    #Upload the complete master sheet     
    gd.set_with_dataframe(sheet, Master_sheet)        
            


    
    
    
    
    
    
        
    """
    
    
    ++++++++++++++++++++++++++++
        
    #UI Part
        
    ++++++++++++++++++++++++++++
     
        
    
    """
    
    
    
    
    
    
    
    
    if UI_run.upper() == 'Y' or UI_run.upper() == 'YES':
    
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
        
        
        def open_browser():
              webbrowser.open_new('http://127.0.0.1:8050/')
          
            
        external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']
        
        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
        
        
        
        
        
        
        
        
        
        
        #Daylist for Dropdown
        list1 = []
        for d_index in range(File_Total):
            day_number = (int(file_number) - int(File_Total)) + (d_index+1)
            list1.append("Day{}".format(day_number))
        
        
        
        
        
        list2 = ["Registered Name","Email ID",'Your Gender',"College Name",'Whatsapp No ', 'Zoom Name', 'Zoom id']
        
        
        Suspence_day_list = ['Zoom Name', 'Email', 'Time', 'Registered Name', 'Gender','College Name', 'WhatsApp No.', 'Zoom id']
        
        
        
        #this for all Full datapresent (Who are present everyday)
        Full_data_present = pd.read_csv("Reports/Full_data_present_everyday.csv")
        Full_dat_index = Full_data_present[(Full_data_present["Name"].isnull())].index[0]
        Full_data_present = Full_data_present.iloc[:Full_dat_index,]
        
        Full_data_list1 = ['Name','Gender','College Name','Email','WhatsApp No.']
        Full_data_list2 = Full_data_present.columns.tolist()[6:-1]
        Full_data_list = Full_data_list1 + Full_data_list2
        
        
        fig1 = px.bar(Full_data_present, y ='Total',x = 'Zoom Name',
                        text='Total',
                        color='Total',
                        hover_data=Full_data_list,
                        height=450,
                     )
        
        
        
        
        
        
        #Not Any day present student Table
        Not_Present_any_col_list = ['Name','Email','Gender','College Name','WhatsApp No.']
        
        Not_Present_any = final_work.copy()
        Not_dat_index = Not_Present_any[(Not_Present_any["Name"].isnull())].index[0]
        Not_Present_any = Not_Present_any.iloc[:Not_dat_index,]
        Not_Present_any = Not_Present_any[Not_Present_any_col_list]
        
        
        
        
        
        
        #Atleast One Day Present Students
        Atleast_present_col_list = Atleast_one_day.columns.tolist()
        
        Atleast_one_day_copy = Atleast_one_day.copy()
        Atleast_one_day_index = Atleast_one_day[(Atleast_one_day["Email"].isnull())].index[0]
        Atleast_one_day_copy = Atleast_one_day_copy.iloc[ : Atleast_one_day_index,]
        
        
        
        
        
        #Suspence Data Table of All Day
        Atleast_present_col_list = Atleast_one_day.columns.tolist()
        All_suspence_data = Atleast_one_day.copy()
        All_suspence_data = All_suspence_data.iloc[Atleast_one_day_index+2 : ,]
        
        
        
        
        
        
        colors = {
            'background': '#111111',
            'text': '#7FDBFF',
            'color1': 'white',
            'color2': 'blue'
        }
        
            
        app.layout = html.Div( children=[
                
            html.H1(
                children='Forsk Coding School',
                style={
                    'textAlign': 'center',
                    'color': colors['color1'],
                    'backgroundColor': colors['color2'],
                    'borderRadius': '5px',
                    'margin': '20px',
                    'padding': '10px',
                    'borderStyle': 'dashed',
                    'margin-bottom':'0px',
                    'font-size': '40px',
                    'margin-top':'10px'
                    
                }
            ),
            html.H3(
                children='-- Student Attendence Analysis --',
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
                }
            ),
            
            
            #dropdown (Days)
            html.Div([dcc.Dropdown(id='dd',
                options=[{'label': c , 'value': c} for c in list1],
                value='Day1')],
            style={
                    'width':'40%',
                    'padding':40
                }
            ),
            
            
            
            
            #Present Registered student
            html.H3(
                children='Registered & Present Student',
                style={
                    'textAlign': 'center',
                    'color': colors['color2'],
                    'margin': 'auto',
                    'font-size': '25px',
                    'margin-bottom':'0px',
                    'font': '20px Arial, sans-serif',
                    
                }
            ),
            #graph1
            dcc.Graph(id = 'graph'),
            
            
            
            
            #Absent Students
            html.H3(
                children='Absent Students Table',
                style={
                    'textAlign': 'center',
                    'color': colors['color2'],
                    'margin': 'auto',
                    'font-size': '25px',
                    'margin-bottom':'10px',
                    'margin-top':'70px',
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
                       style_cell={'whiteSpace': 'normal',
                                   'height': 'auto',
                                   'textAlign': 'left',
                                   'overflow': 'hidden',
                                   'textOverflow': 'ellipsis',
                                   'maxWidth': 0,}, 
                       style_data={ 'border': '1px solid blue' ,
                                   'margin-left':'20px',
                                   'margin-right':'20px'},
                        style_header={
                          'backgroundColor': 'rgb(230, 230, 230)',
                          'fontWeight': 'bold'
                    },
                      
                        ),
                        
                        
                    ], className = 'row'
                ),className="p-5",
            ),
                                
                                
                                
                                
            #Suspence Students
            html.H3(
                children='Suspence Students(Daywise)',
                style={
                    'textAlign': 'center',
                    'color': colors['color2'],
                    'margin': 'auto',
                    'font-size': '25px',
                    'margin-bottom':'10px',
                    'margin-top':'70px',
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
                       style_cell={'whiteSpace': 'normal',
                                   'height': 'auto',
                                   'textAlign': 'left',
                                   'overflow': 'hidden',
                                   'textOverflow': 'ellipsis',
                                   'maxWidth': 0,}, 
                       style_data={ 'border': '1px solid blue' ,
                                   'margin-left':'20px',
                                   'margin-right':'20px'},
                        style_header={
                          'backgroundColor': 'rgb(230, 230, 230)',
                          'fontWeight': 'bold'
                    },
                      
                        ),
                        
                        
                    ], className = 'row'
                ),className="p-5",
            ),
            
            
            
            
            
            
            #Present Everyday
            html.H3(
                children='All Day Present Students',
                style={
                    'textAlign': 'center',
                    'color': colors['color2'],
                    'margin': 'auto',
                    'font-size': '25px',
                    'margin-bottom':'0px',
                    'margin-top':'70px',
                    'font': '20px Arial, sans-serif',
                }
            ),
            
             #graph4           
            dcc.Graph(figure=fig1),
            
            
            
            
            #Not present any day student Table
            html.H3(
                children='Not Present Any Day Students Table',
                style={
                    'textAlign': 'center',
                    'color': colors['color2'],
                    'margin': 'auto',
                    'font-size': '25px',
                    'margin-bottom':'10px',
                    'margin-top':'70px',
                    'font': '20px Arial, sans-serif',
                }
            ),
                 dbc.Container(
                 html.Div(
                    [
                            
                        dash_table.DataTable(
                        data=Not_Present_any.to_dict('records'),
                        columns=[
                            {"name": i, "id": i} for i in Not_Present_any_col_list], 
                       css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],     
                       style_cell={'textAlign': 'left'}, 
                       style_data={ 'border': '1px solid blue' ,
                                   'margin-left':'20px',
                                   'margin-right':'20px'},
                        style_header={
                          'backgroundColor': 'rgb(230, 230, 230)',
                          'fontWeight': 'bold'
                    },
                      
                        ),
                        
                        
                    ], className = 'row'
                ),className="p-5",
            ),
               
        
        
        
        
        
        
                         
            #Atleast One Day Present Table
            html.H3(
                children='Atleast One Day Present Students Table',
                style={
                    'textAlign': 'center',
                    'color': colors['color2'],
                    'margin': 'auto',
                    'font-size': '25px',
                    'margin-bottom':'10px',
                    'margin-top':'70px',
                    'font': '20px Arial, sans-serif',
                }
            ),
                 dbc.Container(
                 html.Div(
                    [
                            
                        dash_table.DataTable(
                        data=Atleast_one_day_copy.to_dict('records'),
                        columns=[
                            {"name": i, "id": i} for i in Atleast_present_col_list], 
                       css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],     
                       style_cell={'textAlign': 'left'}, 
                       style_data={ 'border': '1px solid blue' ,
                                   'margin-left':'20px',
                                   'margin-right':'20px',
                                   'whiteSpace': 'normal',
                                    'height': 'auto',
                                    'lineHeight': '15px'},
                        style_cell_conditional=[
                                    {'if': {'column_id': 'College Name'},
                                          'width': '15%'},
                                    {'if': {'column_id': 'Email'},
                                           'width': '18%'},
                                    {'if': {'column_id': 'WhatsApp No.'},
                                           'width': '8%'},
                        ],
                        style_header={
                          'backgroundColor': 'rgb(230, 230, 230)',
                          'fontWeight': 'bold'
                    },
                      
                        ),
                        
                        
                    ], className = 'row'
                ),className="p-10",
            ),                    
                
          
            
            
            
            #Suspence Data Table of All Day
            html.H3(
                children='All Suspence Data Table',
                style={
                    'textAlign': 'center',
                    'color': colors['color2'],
                    'margin': 'auto',
                    'font-size': '25px',
                    'margin-bottom':'10px',
                    'margin-top':'70px',
                    'font': '20px Arial, sans-serif',
                }
            ),
                 dbc.Container(
                 html.Div(
                    [
                            
                        dash_table.DataTable(
                        data=All_suspence_data.to_dict('records'),
                        columns=[
                            {"name": i, "id": i} for i in Atleast_present_col_list], 
                       css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],     
                       style_cell={'textAlign': 'left'}, 
                       style_data={ 'border': '1px solid blue' ,
                                   'margin-left':'20px',
                                   'margin-right':'20px',
                                   'whiteSpace': 'normal',
                                    'height': 'auto',
                                    'lineHeight': '15px'},
                        style_cell_conditional=[
                                    {'if': {'column_id': 'Email'},
                                           'width': '18%'},
                        ],
                        style_header={
                          'backgroundColor': 'rgb(230, 230, 230)',
                          'fontWeight': 'bold'
                    },
                      
                        ),
                        
                        
                    ], className = 'row'
                ),className="p-5",
            ),
           
                      
                        
                                
        ])
        
        
        
        
        
        #calling for Registered and present students
        @app.callback(dash.dependencies.Output('graph','figure'),[dash.dependencies.Input('dd','value')])
        
        def update_fig(value):
            try:
            
                dff = pd.read_csv("Reports/{}.csv".format(value))
                a = dff[(dff["Email"].isnull())].index[0]
                dff = dff.iloc[:a,]
                figure = px.bar(dff, y ='Time',x = 'Zoom Name',
                                text='Time',
                                color='Time',
                                hover_data=['Registered Name','Gender','College Name','Email'],
                                height=650,
                                )
                figure.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                figure.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        
            except:
                return html.Div(['There was an error processing this file.'])
                
            return figure
        
        
        
        
        #Daywise student present Student Table
        @app.callback(dash.dependencies.Output('datatable-paging','data'),[dash.dependencies.Input('dd','value')])
        
        def update_fig(value):
            try:
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
                data=dff.to_dict('records')
                return data
                      
        
            except:
                return html.Div(['There was an error processing this file.'])
        
        
        
        
        #Daywise Suspense Data Table
        @app.callback(dash.dependencies.Output('suspence_daywise','data'),[dash.dependencies.Input('dd','value')])
        
        def update_fig(value):
            try:
                dff = pd.read_csv("Reports/{}.csv".format(value))
                a = dff[(dff["Email"].isnull())].index[0]
                b = dff[(dff["Email"].isnull())].index[1]
                dff = dff.iloc[a+2:b,]
                data=dff.to_dict('records')
                return data
                      
        
            except:
                return html.Div(['There was an error processing this file.'])
            
            
            
            
            
            
        
        if __name__ == '__main__':
            Timer(1, open_browser).start();
            app.run_server()



else:
    print("Warning:\nPlease Check Meeting Id & Match.\nAnd also check that in directory missing Excel file")








    
    
    

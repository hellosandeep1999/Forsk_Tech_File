# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 13:27:28 2020

@author: user
"""



import pandas as pd
import numpy as np
import os 
import glob
import platform



Meeting_id = int(input("Please Enter your Meeting Id: "))

#you want to UI or not
UI_run = input("Do you want to See UI: ")

#whats your system I want to know by platform.system()
using_system = platform.system() 



#some address which we will define here and use in whole program
win_cloud_dir = "c:/Users/Cloud"                 #for windows
win_master_file = "c:/Users/Cloud/Master.csv"   #for windows

mac_cloud_dir = "/Users/sylvester/Cloud"                  #for mac
mac_master_file = "/Users/sylvester/Cloud/Master.csv"    #for mac


Inside_report_excel = "Reports/{}.csv".format(Meeting_id)  #This is for Excel sheet which is inside in Report folder
outside_excel = "{}.xlsx".format(Meeting_id)                #outside excel sheet

#pandas gives a lot of errors
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
        if not os.path.exists("{}".format(win_cloud_dir)):
            os.makedirs("{}".format(win_cloud_dir))
        if not os.path.exists("{}".format(win_master_file)):
            Master = pd.DataFrame(columns=["Timestamp","UTR No ( PhonePe)","Title","Registered Name",
                                           "Designation","Email ID","Mobile No.",'Your Gender',"College Name",
                                           'Whatsapp No ',"Branch/ Department","Current Semester","College City",
                                           'Status','Mode','Payee Name/New ID','Calling Responses',
                                           'Zoom Name','Matched', 'Zoom id'])
            Master.to_csv("{}".format(win_master_file), index = False)
        if os.path.exists(r"{}".format(win_master_file)):
            Master_sheet = pd.read_csv(r"{}".format(win_master_file))
        return Master_sheet
    
    
    def mac_check_make_Master(): #function for mac and linux c drive cheking and make a master sheet
        if not os.path.exists("{}".format(mac_cloud_dir)):
            os.makedirs("{}".format(mac_cloud_dir))
        if not os.path.exists("{}".format(mac_master_file)):
            Master = pd.DataFrame(columns=["Timestamp","UTR No ( PhonePe)","Title","Registered Name",
                                           "Designation","Email ID","Mobile No.",'Your Gender',"College Name",
                                           'Whatsapp No ',"Branch/ Department","Current Semester","College City",
                                           'Status','Mode','Payee Name/New ID','Calling Responses',
                                           'Zoom Name','Matched', 'Zoom id'])
            Master.to_csv("{}".format(mac_master_file), index = False)
        if os.path.exists("{}".format(mac_master_file)):
            Master_sheet = pd.read_csv("{}".format(mac_master_file))
        return Master_sheet
    
    
    #according to our system function will be run
     #if windows our system
    if using_system == 'Windows':                        
        Master_sheet = window_check_make_Master()
     
    #if Mac or linux our system    
    if using_system == 'Darwin' or using_system == 'Linux':                         
        Master_sheet = mac_check_make_Master()
    





    #This Part for Reconciliation and it will check both Excel sheet if any new data than he will be update
    if os.path.exists("{}".format(Inside_report_excel)):
       Inner_file = pd.read_csv("{}".format(Inside_report_excel))
       outer_file = pd.read_excel("{}".format(outside_excel)) 
    
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
    files_name = All_csv_files2

        
    
    #File_Total is tell us that how many files are exists
    File_Total = len(files_name)
    
    
    
    df4_column_list = [] 
    
    for column_name in df4.columns.tolist():
        if "NAME" in column_name.upper():
            df4_column_list.append(column_name)
            break
    for column_name in df4.columns.tolist():
        if "MAIL" in column_name.upper():
            df4_column_list.append(column_name)
            break
    for column_name in df4.columns.tolist():
        if "GENDER" in column_name.upper():
            df4_column_list.append(column_name)
            break
    for column_name in df4.columns.tolist():
        if "COLLEGE" in column_name.upper():
            df4_column_list.append(column_name)
            break
    for column_name in df4.columns.tolist():
        if "WHATSAPP" in column_name.upper():
            df4_column_list.append(column_name)
            break
            
            
    
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
    
        
    
#Main for loop start from here making daywise csv files  
    for file_index,file_name in enumerate(files_name):
          
        File_Name = file_name
        
        file_number = File_Name[4]
        
        df1 = pd.read_csv("{}".format(File_Name))
        
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
        
        
        zoom_list = df1['Name'].values.tolist()
        zoom_Email_list = df1['Email'].values.tolist()
        data1_list = df4['Name'].values.tolist()
        data1_Email_list = df4['Email'].values.tolist()
        
        #Mater sheet indexing(first we will check in our master sheet for details)
        master_sheet_Email_list = Master_sheet['Zoom id'].values.tolist()
        master_sheet_store = []
        zoom_store1 = []
        
        #This for our registration data indexing
        store = []
        zoom_store = []
        suspence_store = []
        
        
        
        
        data1_list_filter = list(map(lambda x: x.split(),data1_list))
    
        data1_list_ = []
        for i in data1_list_filter:
              data1_list_.append(list(filter(lambda x : len(x)>2, i)))
    
        data1_list_filter = list(map(lambda x: " ".join(x),data1_list_))
        
        
        
        
        
        for zoom_index, zoom_name in enumerate(zoom_list):
            counter = 0
            if str(zoom_Email_list[zoom_index]) in master_sheet_Email_list:
                master_index = Master_sheet['Zoom id'].values.tolist().index(str(zoom_Email_list[zoom_index]))
                master_sheet_store.append(master_index)
                zoom_store1.append(zoom_index)
            elif "." in str(zoom_Email_list[zoom_index]):
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
    
                            
                            
                      
            else:
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
        
    #    store = [i for n, i in enumerate(store) if i not in store[:n]]
    #    zoom_store = [i for n, i in enumerate(zoom_store) if i not in zoom_store[:n]]
        k = 0
        for v in master_sheet_store:
            while k < len(zoom_store1):
                value1 = zoom_store1[k]
                prt_to_reg = prt_to_reg.append({'Zoom Name': df1['Name'][value1], 
                                                'Email': df1['Email'][value1], 
                                                'Time': df1['Time'][value1],
                                                'Registered Name': Master_sheet["Registered Name"][v].upper(),
                                                'Gender': Master_sheet["Your Gender"][v],
                                                'College Name': Master_sheet["College Name"][v],
                                                'WhatsApp No.': Master_sheet["Whatsapp No "][v],
                                                'Zoom id': Master_sheet["Email ID"][v]}, ignore_index=True)
                
                k += 1
                break
           
    
    
    
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
        
     
    #    df4_copy["Matched"] = df4_copy["Matched"].fillna("False")
        
        
        
    #    ['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.','Zoom id']
        
    
        
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
        
        
        
    
        zoom_list_filter = list(map(lambda x: x.split(),zoom_list))
    
        zoom_list_ = []
        for i in zoom_list_filter:
              zoom_list_.append(list(filter(lambda x : len(x)>2, i)))
    
        zoom_list_filter = list(map(lambda x: " ".join(x),zoom_list_))
        
        
        suspence_store_t2 = []
        
        
        for data1_index, data1_name in enumerate(data1_list):
            if "." in str(data1_Email_list[data1_index]):
                for zoom_Email_index,zoom_Email in enumerate(zoom_Email_list):
                    if str(data1_Email_list[data1_index]).upper().strip() == str(zoom_Email).upper().strip():
                        data1_name = data1_name.split()
                        data1_name = " ".join(list(filter(lambda x : len(x)>2, data1_name)))
                        
                        if zoom_list_filter.count(data1_name) > 1:
                            suspence_store_t2.append(data1_index)
                            break
                        else:
    #                        store.append(data1_Email_index)
    #                        zoom_store.append(zoom_index)
    #                        f["Zoom id"][zoom_index] = data1_Email
    #                        df4_copy["Zoom id"][data1_Email_index] = data1_Email
                            break
    #                elif str(df4_copy["Matched"][data1_index]).upper() == True:
    #                    break
                              
                else:
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
                            change_list = list(set_intersection)
    #                        store.append(change_list[0])
    #                        zoom_store.append(zoom_index)
    #                        f["Zoom id"][zoom_index] = df4["Email"][change_list[0]]
    #                        df4_copy["Zoom id"][change_list[0]] = f['Email'][zoom_index]
                        else:
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
                    change_list = list(set_intersection)
    #                        store.append(change_list[0])
    #                        zoom_store.append(zoom_index)
    #                        f["Zoom id"][zoom_index] = df4["Email"][change_list[0]]
    #                        df4_copy["Zoom id"][change_list[0]] = f['Email'][zoom_index]
                else:
                   suspence_store_t2.append(data1_index) 
        
        
        #making dataframe for t2
        suspence_t2 = []
        
        for index in suspence_store_t2:
            suspence_t2.append(df4.iloc[index,])
        
        suspence_t2 = pd.DataFrame(suspence_t2)
        suspence_t2.reset_index(inplace = True, drop = True)  
        
        
        #work for all suspence data
    #    t2 = t2.append(suspence_t2)
        
        
    
        #daywise suspence data
        merge = pd.merge(suspence_t1, suspence_t2, how='outer', on='Email')
        
        merge = merge[['Name_x', 'Email', 'Time', 'Name_y', 'Gender', 'College Name', 'WhatsApp No.']]
    
        merge.columns = ['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.']
    
        merge["Zoom id"] = np.nan
        
    #    else:
    #        df4_copy_Email_list = df4_copy[df4_column_list[1]].values.tolist()
    #        suspence_t2_Email_list = suspence_t2['Email'].values.tolist() 
    #        
    #        suspence_real_t2 = []
    #        absent_t2 = []
    #        
    #        for suspence_t2_index,suspence_t2_Email in enumerate(suspence_t2_Email_list):
    #            for df4_copy_index,df4_copy_Email in enumerate(df4_copy_Email_list):
    #                if suspence_t2_Email == df4_copy_Email:
    #                    if df4_copy["Matched"][df4_copy_index] == "True":
    #                        absent_t2.append(suspence_t2.iloc[suspence_t2_index,])
    #                    else:
    #                        suspence_real_t2.append(suspence_t2.iloc[suspence_t2_index,])
    #        
    #        #this for suspence_t2
    #        suspence_real_t2 = pd.DataFrame(suspence_real_t2)
    #        suspence_real_t2.reset_index(inplace = True, drop = True)
    #    
    #        #this for absent list
    #        absent_t2 = pd.DataFrame(absent_t2)
    #        absent_t2.reset_index(inplace = True, drop = True) 
    #        absent_t2["Zoom Name"] = np.nan
    #        absent_t2["Time"] = np.nan
    #        
    #        absent_t2 = absent_t2[['Zoom Name', 'Email', 'Time', 'Name', 'Gender', 'College Name', 'WhatsApp No.']]
    #        absent_t2.columns = ['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.']
    #        absent_t2["Zoom id"] = np.nan
    #        
    #        #work for all suspence data
    #        t2 = t2.append(suspence_real_t2)
    #    
    #        #daywise suspence data
    #        merge = pd.merge(suspence_t1, suspence_real_t2, how='outer', on='Email')
    #        
    #        merge = merge[['Name_x', 'Email', 'Time', 'Name_y', 'Gender', 'College Name', 'WhatsApp No.']]
    #        
    #        merge.columns = ['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.']
    #    
    #        merge["Zoom id"] = np.nan
    #    
    #        merge = merge.append(pd.Series("nan"), ignore_index=True)
    #        merge = merge.drop([0],axis=1) 
    #        new_row={"Zoom Name":"Absent","Email":"Data"}
    #        merge = merge.append(new_row,ignore_index=True)
        
        
        prt_to_reg = prt_to_reg.sort_values("Time", ascending = False)
        prt_to_reg.reset_index(inplace = True, drop = True) 
        
        prt_to_reg=prt_to_reg.append(pd.Series("nan"), ignore_index=True)
        prt_to_reg=prt_to_reg.drop([0],axis=1) 
        new_row={"Zoom Name":"Suspense","Email":"Data"}
        prt_to_reg = prt_to_reg.append(new_row,ignore_index=True)   
        
        
        #for full.csv
        my_copy = prt_to_reg[:-2].copy()
        dataframe_name[file_index] = my_copy
        dataframe_name[file_index] = dataframe_name[file_index][["Zoom Name","Zoom id","Time"]]
        dataframe_name[file_index].columns = ["Name", "Zoom id", "Time"]
        dataframe_name[file_index].loc[:,"Date"] = file_index+1
        
        
        frame=[prt_to_reg,merge]
        result=pd.concat(frame)
        result.reset_index(inplace = True, drop = True)
        
        #Now we will just store the result data in --> before_updated_day
        before_updated_day[file_index] = result
        
    #    result.to_csv("Day{}.csv".format(file_number), index = False)   
             
       
    df4_copy["Matched"] = df4_copy["Matched"].fillna(False)
        
        
    #Now code for creating daywise file and seprate the absent section
        
    for day_index in range(File_Total):
        null_index1 = before_updated_day[day_index][before_updated_day[day_index]["Zoom Name"].isnull()].index.tolist()[0]
        null_index2 = before_updated_day[day_index][before_updated_day[day_index]["Zoom Name"].isnull()].index.tolist()[1]
        
        #seprate section
        present_data = before_updated_day[day_index].iloc[:null_index1,]
        present_data = present_data.append(pd.Series("nan"), ignore_index=True)
        present_data = present_data.drop([0],axis=1) 
        new_row={"Zoom Name":"Suspense","Email":"Data"}
        present_data = present_data.append(new_row,ignore_index=True)
        
        
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
        t2_real_suspence = pd.DataFrame(t2_real_suspence)
        t2_real_suspence.reset_index(inplace = True, drop = True)
    
        #copy of t2_real_suspence for all suspence
        t2_real_suspence_copy = t2_real_suspence.copy()
    
    
        #daywise suspence data
        merge = pd.merge(t1_suspence, t2_real_suspence, how='outer', on='Email')
            
        merge = merge[['Zoom Name_x', 'Email', 'Time_x', 'Registered Name_y', 'Gender_y', 'College Name_y', 'WhatsApp No._y','Zoom id_y']]
            
        merge.columns = ['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.','Zoom id']
    
        #add a nun row for absent data
        merge = merge.append(pd.Series("nan"), ignore_index=True)
        merge = merge.drop([0],axis=1) 
        new_row={"Zoom Name":"Absent","Email":"Data"}
        merge = merge.append(new_row,ignore_index=True)
        
         
        
        #this for absent list
        if len(t2_absent) == 0:
            t2_absent = pd.DataFrame(columns=['Zoom Name','Email','Time','Registered Name','Gender','College Name','WhatsApp No.','Zoom id'])
        else:
            t2_absent = pd.DataFrame(t2_absent)
            t2_absent.reset_index(inplace = True, drop = True)
            t2_absent["Zoom Name"] = np.nan
            t2_absent["Time"] = np.nan
        
        
        #work for all suspence data
        real_suspence = t2_real_suspence_copy[['Registered Name', 'Email', 'Gender', 'College Name', 'WhatsApp No.']]   
        real_suspence.columns = ['Name','Email','Gender','College Name','WhatsApp No.']
        t2 = t2.append(real_suspence) 
                           
    
        daywise_frame = [present_data,merge,t2_absent]
        daywise_result = pd.concat(daywise_frame)
        daywise_result.reset_index(inplace = True, drop = True)
    
        #this number will print on daywise file name
        daynumber = (int(file_number) - int(File_Total)) + (day_index+1)
        
        daywise_result.to_csv("Reports/Day{}.csv".format(daynumber), index = False)
    
    
    
    #from here we will generate 4 extra details files
    
    
    
    
    #code for suspence data
    t1.dropna(subset=['Email'], inplace=True)
    t1_name_column = []
    for t1_name in t1.columns.tolist():
        if "Name" in t1_name:
            t1_name_column.append(t1_name)
    
    t1.reset_index(inplace = True, drop = True)        
    name_list = []
    for i in range(t1.shape[0]):    
         a = t1.loc[i,t1_name_column].tolist()   
         cleanedList = [x for x in a if str(x) != 'nan']
         name_list.append(cleanedList[0])
    
    t1["Name_column"] = name_list
    
    t1_name_column2 = ["Name_column"]
    
    t1_name_column2.append("Email")
    t1_time_column = []
    for t1_time in t1.columns.tolist():
        if "Time" in t1_time:
            t1_time_column.append(t1_time)
    
    
    t1_column = t1_name_column2+t1_time_column
    
    t1 = t1[t1_column]
    t1["Total"] = np.nan
    t1 = t1.fillna(0)
    
    day_count = ["Zoom Name","Email"]
    for day_index in range(len(t1_time_column)):
        day_count.append("Day{}".format(day_index))
    
    day_count.append("Total")
    t1.columns = day_count
    
    t1["Total"] = 0
    for daywise_index in range(len(t1_time_column)):
        t1["Total"] += t1["Day{}".format(daywise_index)]
    
    t1 = t1.sort_values("Total", ascending = False)
    
    t2.drop_duplicates(subset=["Email"], keep='first', inplace=True)
    
    suspence_merge = pd.merge(t1,t2, how='outer', on='Email')
    
    suspence_merge_list = ['Name', 'Gender', 'College Name', 'WhatsApp No.','Zoom Name','Email']
    
    suspence_merge_list = suspence_merge_list + t1.columns.tolist()[2:]
    
    suspence_merge = suspence_merge[suspence_merge_list]  #now we will add this data into everyday and atleast present
        
      
    
    
    
    
    
    
    
    #========================
    
    
    
    
        
    df4 = df4.rename(columns={'Email': 'Zoom id'})
    #work start for full.csv
    
    
    
    #every day present
        
    zoom = pd.concat(dataframe_name)
    #Deleting the columns with no value
    zoom = zoom.dropna(how = "all")
    
    zoom.reset_index(inplace = True, drop = True)     
        
    
    
        
    emails = zoom["Zoom id"].tolist()
    ats = []
    for at_index in range(1,(File_Total+1)):
        b = "at" + str(at_index)
        ats.append(b)
        
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
    
    z = pd.DataFrame(ats)
       
    z = z.T  #transpose the dataframe
    
    
    column_list = ["Zoom Name", "Email"]
    for column_list_index in range(File_Total):
        day_name = "Day{}".format(column_list_index)
        column_list.append(day_name)
    
    column_list.append("Total")
    
    z.columns = column_list
    
    
    z.drop_duplicates(inplace = True)
    z.reset_index(inplace = True, drop = True)    
       
    
     
    z = z.rename(columns={'Email': 'Zoom id'})
    final = z.merge(right = df4, how = "left", on = "Zoom id", suffixes=('', 'Registered'))
    
    
    
    
    final_list = ['Name', 'Gender', 'College Name', 'WhatsApp No.','Zoom Name', 'Zoom id']
    for final_list_index in range(File_Total):
        day_name = "Day{}".format(final_list_index)
        final_list.append(day_name)
    
    final_list.append("Total")
    final = final[final_list]
    
    
    final = final.sort_values("Total", ascending = False)
    
    final_copy = final.copy()  #make a copy of dataframe
    
    
    
    
    
    
    
    #atleast one day present data
    
    Atleast_one_day = final.copy()  
    Atleast_one_day.drop_duplicates(subset=["Zoom id"], keep='first', inplace=True)
    Atleast_one_day.reset_index(inplace = True, drop = True) 
        
      
    Atleast_one_day = Atleast_one_day.rename(columns={'Zoom id': 'Email'})
    Atleast_one_day = Atleast_one_day.rename(columns={'Name': 'Original_Name'})
    
    #this is for original name
    original_copy = df4_copy.copy()
    
    original_copy = original_copy.rename(columns={df4_column_list[1]: 'Email'})
    
    Atleast_one_day = Atleast_one_day.merge(right = original_copy, how = "inner", on = "Email", suffixes=('', '_Reg') )
    
    Atleast_one_day_list = ['{}'.format(df4_column_list[0]), 'Gender', 'College Name', 'WhatsApp No.','Zoom Name', 'Email']
    for Atleast_list_index in range(File_Total):
        At_day_name = "Day{}".format(Atleast_list_index)
        Atleast_one_day_list.append(At_day_name)
    
    Atleast_one_day_list.append("Total")
    
    Atleast_one_day = Atleast_one_day[Atleast_one_day_list]
    
    
    #Now we will add suspence section in atleast one day
    Atleast_one_day=Atleast_one_day.append(pd.Series("nan"), ignore_index=True)
    Atleast_one_day=Atleast_one_day.drop([0],axis=1) 
    new_row={df4_column_list[0]:"Suspense","Gender":"Data"}
    Atleast_one_day = Atleast_one_day.append(new_row,ignore_index=True) 
    
    Atleast_one_day = Atleast_one_day.rename(columns={df4_column_list[0]:'Name'})
    
    #suspence_merge1 = suspence_merge.rename(columns={'Name':df4_column_list[0]})
    
    frame2 = [Atleast_one_day,suspence_merge]
    Atleast_one_day = pd.concat(frame2)
    Atleast_one_day.reset_index(inplace = True, drop = True)
    
    Atleast_one_day.to_csv("Reports/Atleast_one_day_present.csv", index = False)    
        
     
         
    
    
    
          
    #code for everyday present who are register and join every day  
        
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
    
    frame3 = [final,suspence_merge]
    final = pd.concat(frame3)
    final.reset_index(inplace = True, drop = True)
    
    final.to_csv("Reports/Full_data_present_everyday.csv", index = False)    
        
        
        
        
        
        
        
    #Code start for No_present.csv 
    
    final_copy.drop_duplicates(subset=["Zoom id"], keep='first', inplace=True) 
    
    final_work = final_copy.merge(right = df4, how = "outer", on = "Zoom id", suffixes=('', '_Reg') )
    
    final_work = final_work[final_work['Zoom Name'].isnull()]
    
    final_work_list = ['Name_Reg','Gender_Reg', 'College Name_Reg', 'WhatsApp No._Reg','Zoom Name','Zoom id']
    
    for final_list_index in range(File_Total):
        final_day_name = "Day{}".format(final_list_index)
        final_work_list.append(final_day_name)
    
    final_work_list.append("Total")
    
    final_work = final_work[final_work_list]
    
    final_work = final_work.rename(columns={'Name_Reg': 'Name',
                                            'Gender_Reg': 'Gender',
                                            'College Name_Reg': 'College Name',
                                            'WhatsApp No._Reg': 'WhatsApp No.',
                                            'Name_Reg': 'Name',
                                            'Zoom id': 'Email'})
    
    final_work = final_work.append(pd.Series("nan"), ignore_index=True)
    final_work = final_work.drop([0],axis=1) 
    new_row = {'Name':"Suspense","Gender":"Data"}
    final_work = final_work.append(new_row,ignore_index=True) 
    
    
    frame4 = [final_work,suspence_merge]
    final_work = pd.concat(frame4)
    final_work.reset_index(inplace = True, drop = True)
    
    
    final_work.to_csv("Reports/Not_present_any_day.csv", index = False)
    
    
    
    
    #updated excel sheet
    if not os.path.exists("{}".format(Inside_report_excel)):
        df4_copy.to_csv("{}".format(Inside_report_excel), index = False)
                            
      

    #Master sheet                  
    #Add the data in Master sheet (if we have new data)
    Matching_data = df4_copy[df4_copy["Matched"] == True]
    Matching_data.reset_index(inplace = True, drop = True)
    Matching_data_email_list = Matching_data[df4_column_list[1]].values.tolist()
    for Matching_data_email_index,Matching_data_email in enumerate(Matching_data_email_list):
        if str(Matching_data_email) not in Master_sheet["Email ID"].values.tolist():
            
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
                          'Zoom Name' : Master_columns_list[17],
                          'Matched' : Master_columns_list[18],
                          'Zoom id' : Master_columns_list[19]
                          }
            Master_sheet = Master_sheet.append(dictionary, ignore_index=True)
    
    #if windows our system
    if using_system == 'Windows':
        Master_sheet.to_csv(r"{}".format(win_master_file), index = False)
    
    #if Mac or linux our system    
    if using_system == 'Darwin' or using_system == 'Linux':
        Master_sheet.to_csv("{}".format(mac_master_file), index = False)         



    
    
    
    
    
    
        
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
        
        
        
        markdown_text = '''
        ## **Prime - 5** (Unsupervised Machine Learning Training)
        #### Schedule **26 to 30 May** (5 days Training Timing 5:00Pm - 7:00Pm)
        #### Traning Fee : INR - only **500 /-INR**
        ######  Call or whatsapp. [+917851929944](/)
        '''
        
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








    
    
    

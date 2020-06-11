# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 13:27:28 2020

@author: user
"""

import pandas as pd
import numpy as np
import os 

Meeting_id = int(input("Enter your Meeting Id: "))


df4 = pd.read_excel("{}.xlsx".format(Meeting_id))
total_column = len(df4.columns.tolist())
df4.dropna(thresh=total_column-8,inplace=True)
df4_copy = df4.copy()

#df4_copy["Zoom id"] = np.nan
#df4_copy["Matched"] = np.nan



#checking that how many files are exists in directory
files_name = []
if os.path.isfile("Day_0_participants_{}.csv".format(Meeting_id)):
    files_name.append("Day_0_participants_{}.csv".format(Meeting_id))

count = 1
while True:
    if os.path.isfile("Day_{}_participants_{}.csv".format(count,Meeting_id)):
        files_name.append("Day_{}_participants_{}.csv".format(count,Meeting_id))
    else:
        break
    count += 1
    
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
                df4_copy["Zoom id"][df4_copy_email_index] = prt_to_reg["Email"][prt_to_reg_zoom_id_index]
                df4_copy["Matched"][df4_copy_email_index] = "TRUE"
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
    dataframe_name[file_index]["Date"] = file_index+1
    
    
    frame=[prt_to_reg,merge]
    result=pd.concat(frame)
    result.reset_index(inplace = True, drop = True)
    
    #Now we will just store the result data in --> before_updated_day
    before_updated_day[file_index] = result
    
#    result.to_csv("Day{}.csv".format(file_number), index = False)   
         
   
df4_copy["Matched"] = df4_copy["Matched"].fillna("FALSE")
    
    
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
    merge = pd.merge(suspence_t1, t2_real_suspence, how='outer', on='Email')
        
    merge = merge[['Name', 'Email', 'Time_x', 'Registered Name', 'Gender', 'College Name', 'WhatsApp No.','Zoom id']]
        
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
    
    daywise_result.to_csv("Day{}.csv".format(daynumber), index = False)



df4_copy.to_excel("{}.xlsx".format(Meeting_id), index = False)









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

suspence_merge1 = suspence_merge.rename(columns={'Name':df4_column_list[0]})

frame2 = [Atleast_one_day,suspence_merge1]
Atleast_one_day = pd.concat(frame2)
Atleast_one_day.reset_index(inplace = True, drop = True)

Atleast_one_day.to_csv("Atleast_one_day_present.csv", index = False)    
    
 
     



      
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

final.to_csv("Full_data_present_everyday.csv", index = False)    
    
    
    
    
    
    
    
#Code start for No_present.csv 

final_copy.drop_duplicates(subset=["Zoom id"], keep='first', inplace=True) 

final_work = final_copy.merge(right = df4, how = "outer", on = "Zoom id", suffixes=('', '_Reg') )

final_work = final_work[final_work['Zoom Name'].isnull()]

final_work = final_work[['Name_Reg','Zoom id','Gender_Reg', 'College Name_Reg', 'WhatsApp No._Reg']]

final_work.to_csv("Not_present_any_day.csv", index = False)







#updated excel sheet
df4_copy.to_csv("Updated_Excel _sheet.csv", index = False)

   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
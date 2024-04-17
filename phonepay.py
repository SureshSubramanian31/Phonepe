# Importing The library's
import os
import json
import pandas as pd
import plotly.express as px

# Creating a path and Extracting the Data for Aggregated Transaction:
path1 = "C:/Users/Kavin/Desktop/Assignments/pulse/data/aggregated/transaction/country/india/state/"
Agg_tran_list = os.listdir(path1)

Part1 = { "States":[], "Years":[], "Quarter":[], "Transaction_type":[], "Transaction_count":[], "Transaction_amount":[]}

for state in Agg_tran_list:
    Tran_states = path1+state+"/" 
    Agg_year_list = os.listdir(Tran_states)

    for year in Agg_year_list: 
        Tran_year = Tran_states+year+"/" 
        Agg_file_list = os.listdir(Tran_year)

        for file in Agg_file_list: 
            Tran_file = Tran_year +file 
            Phone = open(Tran_file,"r")

            Tran_Agg = json.load(Phone)

            for i in Tran_Agg ["data"]["transactionData"]: 
                Name = i["name"] 
                Count = i["paymentInstruments"][0]["count"] 
                Amount = i["paymentInstruments"][0]["amount"] 

                Part1["Transaction_type"].append(Name) 
                Part1["Transaction_count"].append(Count) 
                Part1["Transaction_amount"].append(Amount) 

                Part1["States"].append(state)
                Part1["Years"].append(year)
                Part1["Quarter"].append(int(file.strip (".json")))

Aggregate_Transaction = pd.DataFrame(Part1)

Aggregate_Transaction["States"] = Aggregate_Transaction["States"].str.replace("andaman-&-nicobar-islands", "Andaman & Nicobar")
Aggregate_Transaction["States"] = Aggregate_Transaction["States"].str.replace("-"," ")
Aggregate_Transaction["States"] = Aggregate_Transaction["States"].str.title()
Aggregate_Transaction["States"] = Aggregate_Transaction["States"].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")                

# Creating a path and Extracting the Data for Aggregated Users

path2 = "C:/Users/Kavin/Desktop/Assignments/pulse/data/aggregated/user/country/india/state/"
Agg_user_list = os.listdir(path2)

Part2 = { "States":[], "Years":[], "Quarter":[], "Brands":[], "Transaction_count":[], "Percentage":[]}

for state in Agg_user_list:
    Tran_states = path2+state+"/" 
    Agg_year_list = os.listdir(Tran_states)

    for year in Agg_year_list: 
        Tran_year = Tran_states+year+"/" 
        Agg_file_list = os.listdir(Tran_year)

        for file in Agg_file_list: 
            Tran_file = Tran_year +file 
            Phone = open(Tran_file,"r")

            Agg_User = json.load(Phone)

            try:
                for i in Agg_User["data"]["usersByDevice"]: 
                    Brand = i["brand"] 
                    Count = i["count"] 
                    Percentages = i["percentage"] 

                    Part2["Brands"].append(Brand) 
                    Part2["Transaction_count"].append(Count) 
                    Part2["Percentage"].append(Percentages) 

                    Part2["States"].append(state)
                    Part2["Years"].append(year)
                    Part2["Quarter"].append(int(file.strip (".json")))
            except:
                pass
            
Aggregate_User = pd.DataFrame(Part2)

Aggregate_User["States"] = Aggregate_User["States"].str.replace("andaman-&-nicobar-islands", "Andaman & Nicobar")
Aggregate_User["States"] = Aggregate_User["States"].str.replace("-"," ")
Aggregate_User["States"] = Aggregate_User["States"].str.title()
Aggregate_User["States"] = Aggregate_User["States"].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")            

# Creating a path and Extracting the Data for Map Transaction
path3 = "C:/Users/Kavin/Desktop/Assignments/pulse/data/map/transaction/hover/country/india/state/"
Map_tran_list = os.listdir(path3)

Part3 = { "States": [], "Years":[], "Quarter":[], "Districts":[], "Transaction_count":[], "Transaction_amount":[]}

for state in Map_tran_list:
    Tran_states = path3+state+"/" 
    Agg_year_list = os.listdir(Tran_states)

    for year in Agg_year_list: 
        Tran_year = Tran_states+year+"/" 
        Agg_file_list = os.listdir(Tran_year)

        for file in Agg_file_list: 
            Tran_file = Tran_year +file 
            Phone = open(Tran_file,"r")

            Map_Tran = json.load(Phone)

            for i in Map_Tran ["data"]["hoverDataList"]: 

                Name = i["name"] 
                Count =i["metric"][0]["count"] 
                Amount =i["metric"][0]["amount"] 

                Part3["Districts"].append(Name) 
                Part3["Transaction_count"].append(Count) 
                Part3["Transaction_amount"].append(Amount) 

                Part3["States"].append(state)
                Part3["Years"].append(year)
                Part3["Quarter"].append(int(file.strip (".json")))
                
Map_Transaction = pd.DataFrame(Part3)

Map_Transaction["States"] = Map_Transaction["States"].str.replace("andaman-&-nicobar-islands", "Andaman & Nicobar")
Map_Transaction["States"] = Map_Transaction["States"].str.replace("-"," ")
Map_Transaction["States"] = Map_Transaction["States"].str.title()
Map_Transaction["States"] = Map_Transaction["States"].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")                                                  

# Creating a path and Extracting the Data for Map Users
path4 = "C:/Users/Kavin/Desktop/Assignments/pulse/data/map/user/hover/country/india/state/"
Map_user_list = os.listdir(path4)

Part4 = { "States": [], "Years":[], "Quarter":[], "Districts":[], "Registered_Users":[], "AppOpens":[]}

for state in Map_user_list:
    Tran_states = path4+state+"/" 
    Agg_year_list = os.listdir(Tran_states)

    for year in Agg_year_list: 
        Tran_year = Tran_states+year+"/" 
        Agg_file_list = os.listdir(Tran_year)

        for file in Agg_file_list: 
            Tran_file = Tran_year +file 
            Phone = open(Tran_file,"r")

            Map_Us = json.load(Phone)

            for i in Map_Us ["data"]["hoverData"].items(): 

                District = i[0] 
                RegisteredUser = i[1]["registeredUsers"] 
                AppOpen = i[1]["appOpens"] 

                Part4["Districts"].append(District) 
                Part4["Registered_Users"].append(RegisteredUser) 
                Part4["AppOpens"].append(AppOpen) 

                Part4["States"].append(state)
                Part4["Years"].append(year)
                Part4["Quarter"].append(int(file.strip (".json")))
                
Map_User = pd.DataFrame(Part4)

Map_User["States"] = Map_User["States"].str.replace("andaman-&-nicobar-islands", "Andaman & Nicobar")
Map_User["States"] = Map_User["States"].str.replace("-"," ")
Map_User["States"] = Map_User["States"].str.title()
Map_User["States"] = Map_User["States"].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")                

path5 ="C:/Users/Kavin/Desktop/Assignments/pulse/data/top/transaction/country/india/state/"
Top_Tran_list = os.listdir(path5)

# Creating a path and Extracting the Data for Top Transaction
Part5 = { "States": [], "Years":[], "Quarter":[], "Pincodes":[], "Transaction_count":[], "Transaction_amount":[]}

for state in Top_Tran_list:
    Tran_states = path5+state+"/" 
    Agg_year_list = os.listdir(Tran_states)

    for year in Agg_year_list: 
        Tran_year = Tran_states+year+"/" 
        Agg_file_list = os.listdir(Tran_year)

        for file in Agg_file_list: 
            Tran_file = Tran_year +file 
            Phone = open(Tran_file,"r")

            Top_Tran = json.load(Phone)

            for i in Top_Tran ["data"]["pincodes"]: 
                Entityname= i["entityName"] 
                Count=i["metric"]["count"] 
                Amount=i["metric"]["amount"] 

                Part5["Pincodes"].append(Entityname) 
                Part5["Transaction_count"].append(Count) 
                Part5["Transaction_amount"].append(Amount) 

                Part5["States"].append(state)
                Part5["Years"].append(year)
                Part5["Quarter"].append(int(file.strip (".json")))
                
Top_Transaction = pd.DataFrame(Part5)

Top_Transaction["States"] = Top_Transaction["States"].str.replace("andaman-&-nicobar-islands", "Andaman & Nicobar")
Top_Transaction["States"] = Top_Transaction["States"].str.replace("-"," ")
Top_Transaction["States"] = Top_Transaction["States"].str.title()
Top_Transaction["States"] = Top_Transaction["States"].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")               


# Creating a path and Extracting the Data for Top Users
path6 = "C:/Users/Kavin/Desktop/Assignments/pulse/data/top/user/country/india/state/"
Top_user_list = os.listdir(path6)

Part6 = { "States": [], "Years":[], "Quarter":[], "Pincodes":[], "RegisteredUsers":[]}

for state in Top_user_list:
    Tran_states = path6+state+"/" 
    Agg_year_list = os.listdir(Tran_states)

    for year in Agg_year_list: 
        Tran_year = Tran_states+year+"/" 
        Agg_file_list = os.listdir(Tran_year)

        for file in Agg_file_list: 
            Tran_file   =  Tran_year +file 
            Phone = open(Tran_file,"r")

            Top_user = json.load(Phone)

            for i in Top_user ["data"]["pincodes"]: 

                Entityname= i["name"] 
                RegisteredUser =i["registeredUsers"] 

                Part6["Pincodes"].append(Entityname) 
                Part6["RegisteredUsers"].append(RegisteredUser)  

                Part6["States"].append(state)
                Part6["Years"].append(year)
                Part6["Quarter"].append(int(file.strip (".json")))


Top_User = pd.DataFrame(Part6)

Top_User["States"] = Top_User["States"].str.replace("andaman-&-nicobar-islands", "Andaman & Nicobar")
Top_User["States"] = Top_User["States"].str.replace("-"," ")
Top_User["States"] = Top_User["States"].str.title()
Top_User["States"] = Top_User["States"].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

# connecting to MySQL
# Creating a Table And inserting the Data

import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Suresh@01",
  database="phone")
cursor = mydb.cursor()

# Creating Aggregated Transaction Table:
Query01 = """Create Table if not exists aggregated_transaction(States varchar(255),
                                                Years int,
                                                Quaters int,
                                                Transaction_Type varchar(255),
                                                Transaction_Count int,
                                                Transaction_Amount float)"""
cursor.execute(Query01)
mydb.commit()

# Inserting Aggregated Transaction Values:
insert01 = """Insert into aggregated_transaction (States, 
                                                Years,
                                                Quaters,
                                                Transaction_Type,
                                                Transaction_Count, 
                                                Transaction_Amount)
                                                
                                                values(%s,%s,%s,%s,%s,%s)"""
Insert_A_T = Aggregate_Transaction.values.tolist()
cursor.executemany(insert01, Insert_A_T)  
mydb.commit()


import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Suresh@01",
  database="phone")
cursor = mydb.cursor()

#Creating Aggregated User table:
Query02 = """Create Table if not exists aggregated_users(States varchar(255),
                                                        Years int,
                                                        Quaters int,
                                                        Brands varchar(255),
                                                        Transaction_Count int,
                                                        Percentage float)"""
cursor.execute(Query02)
mydb.commit()

#Inserting Aggregated User Values:
insert02 = """Insert into aggregated_users (States, 
                                            Years,
                                            Quaters, 
                                            Brands,
                                            Transaction_Count, 
                                            Percentage)
                                            
                                            values(%s,%s,%s,%s,%s,%s)"""
Insert_A_U = Aggregate_User.values.tolist()
cursor.executemany(insert02, Insert_A_U)  
mydb.commit()

import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Suresh@01",
  database="phone")
cursor = mydb.cursor()

# Creating Map transaction Table:
Query03 = """Create Table if not exists map_transaction (States varchar(255),
                                                        Years int,
                                                        Quaters int,
                                                        District varchar(255),
                                                        Transaction_Count int,
                                                        Transaction_Amount float)"""
cursor.execute(Query03)
mydb.commit()

# Inserting Map Transaction Values:
insert03 = """Insert into map_transaction (States, 
                                          Years,
                                          Quaters, 
                                          District,
                                          Transaction_Count, 
                                          Transaction_Amount)
                                            
                                          values(%s,%s,%s,%s,%s,%s)"""
Insert_M_T = Map_Transaction.values.tolist()
cursor.executemany(insert03, Insert_M_T)  
mydb.commit()


import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Suresh@01",
  database="phone")
cursor = mydb.cursor()

# Creating Map User Table:
Query04 = """Create Table if not exists map_users(States varchar(255),
                                                        Years int,
                                                        Quaters int,
                                                        Districts varchar(255),
                                                        Registered_Users int,
                                                        AppOpens int)"""
cursor.execute(Query04)
mydb.commit()

# Inserting Map User Values:
insert04 = """Insert into map_users (States, 
                                            Years,
                                            Quaters, 
                                            Districts,
                                            Registered_Users, 
                                            AppOpens)
                                            
                                            values(%s,%s,%s,%s,%s,%s)"""
Insert_M_U = Map_User.values.tolist()
cursor.executemany(insert04, Insert_M_U)  
mydb.commit()


import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Suresh@01",
  database="phone")
cursor = mydb.cursor()

# Creating Top Transaction table:
Query05 = """Create Table if not exists top_transaction(States varchar(255),
                                                        Years int,
                                                        Quaters int,
                                                        Pincodes int,
                                                        Transaction_Count int,
                                                        Transaction_Amount float)"""
cursor.execute(Query05)
mydb.commit()

# Inserting Top Transaction Values:
insert05 = """Insert into top_transaction (States, 
                                            Years,
                                            Quaters, 
                                            Pincodes,
                                            Transaction_Count, 
                                            Transaction_Amount)
                                            
                                            values(%s,%s,%s,%s,%s,%s)"""
Insert_T_T = Top_Transaction.values.tolist()
cursor.executemany(insert05, Insert_T_T)  
mydb.commit()

import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Suresh@01",
  database="phone")
cursor = mydb.cursor()

# Creating Top User table:
Query06 = """Create Table if not exists top_users(States varchar(255),
                                                  Years int,
                                                  Quaters int,
                                                  Pincodes int,
                                                  RegisteredUsers int)"""
cursor.execute(Query06)
mydb.commit()

# Inserting Top User Values:
insert06 = """Insert into top_users (States, 
                                    Years,
                                    Quaters, 
                                    Pincodes,
                                    RegisteredUsers)
                                            
                                    values(%s,%s,%s,%s,%s)"""
Insert_T_U = Top_User.values.tolist()
cursor.executemany(insert06, Insert_T_U)  
mydb.commit()                                                                                                                                                                                                                                                      
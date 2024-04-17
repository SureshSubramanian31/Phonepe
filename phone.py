# Importing the library's
import streamlit as st 

import pandas as pd 
import mysql.connector
import plotly.express as px

import requests
import json

# Connecting to MySQL and Retriving the Data
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Suresh@01",
  database="phone")
cursor = mydb.cursor()

# Aggregated Transaction Details:
cursor.execute("select * from aggregated_transaction")
Table01 = cursor.fetchall()

p_aggregated_transaction = pd.DataFrame(Table01,columns=("States", "Years", "Quater", "Transaction_Type", "Transaction_Count", "Transaction_Amount"))

# Aggregated User Details:
cursor.execute("select * from aggregated_users")
Table02 = cursor.fetchall()

p_aggregated_users = pd.DataFrame(Table02,columns=("States", "Years", "Quater", "Brands", "Transaction_Count", "Percentage"))

## Map Transaction Details:
cursor.execute("select * from map_transaction")
Table03 = cursor.fetchall()

p_map_transaction = pd.DataFrame(Table03,columns=("States", "Years", "Quater", "Districts", "Transaction_Count", "Transaction_Amount"))

## Map Users Details:
cursor.execute("select * from map_users")
Table04 = cursor.fetchall()

p_map_users = pd.DataFrame(Table04,columns=("States", "Years", "Quater", "Districts", "Registered_Users", "AppOpens"))

## Top Transaction:
cursor.execute("select * from top_transaction")
Table05 = cursor.fetchall()

p_top_transaction = pd.DataFrame(Table05,columns=("States", "Years", "Quater", "Pincodes", "Transaction_Count", "Transaction_Amount"))

## Top users Details:
cursor.execute("select * from top_users")
Table06 = cursor.fetchall()

p_top_users= pd.DataFrame(Table06,columns=("States", "Years", "Quater", "Pincodes", "RegisteredUsers"))
 
###############################################################################################################################################
# We are Aggregated Transaction Year and viewing them in a India Map:
def A_T_Y(df, year):  # sourcery skip: extract-duplicate-method, extract-method
    pay = df[df["Years"] == year]
    pay.reset_index(drop = True, inplace = True)
        
    payy = pay.groupby("States")[["Transaction_Count", "Transaction_Amount"]].sum()
    payy.reset_index(inplace = True)
    
    col1, col2 = st.columns(2)
    with col1:
        
        graph_A = px.bar(payy, x="States", y="Transaction_Amount", title = f" {year} Transaction Amount",
                         height = 600, width = 600)
        st.plotly_chart(graph_A)
    
    with col2:
        graph_C = px.bar(payy, x="States", y="Transaction_Count", title = f" {year} Transaction Count",
                         height = 600, width = 600)
        st.plotly_chart(graph_C)
    
    col1,col2 = st.columns(2)
    with col1:    
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        map1 = json.loads(response.text)

        State_map = []
        for india in map1["features"]:
            State_map.append(india["properties"]["ST_NM"])
        State_map.sort()
        
        India_map = px.choropleth(payy,geojson = map1, locations = "States", featureidkey = "properties.ST_NM",color = "Transaction_Amount", color_continuous_scale = "Rainbow", 
                                range_color = (payy["Transaction_Amount"].min(), payy["Transaction_Amount"].max()),
                                hover_name = "States", title = f"{year} Transaction Amount", fitbounds = "locations",  height = 600, width = 600)

        India_map.update_geos(visible = False)
        st.plotly_chart(India_map)
    
    with col2:
        
        India_map1 = px.choropleth(payy,geojson = map1, locations = "States", featureidkey = "properties.ST_NM",color = "Transaction_Count", color_continuous_scale = "Rainbow", 
                                range_color = (payy["Transaction_Count"].min(), payy["Transaction_Count"].max()),
                                hover_name = "States", title = f"{year} Transaction Count", fitbounds = "locations",  height = 600, width = 600)

        India_map1.update_geos(visible = False)
        st.plotly_chart(India_map1)
    return pay    

# We are Aggregated Transaction Quarter and viewing them in a India Map:        
def A_T_Q(df, quarter):
    pay = df[df["Quater"] == quarter]
    pay.reset_index(drop = True, inplace = True)
        
    payy = pay.groupby("States")[["Transaction_Count", "Transaction_Amount"]].sum()
    payy.reset_index(inplace = True)
    
    col1, col2 = st.columns(2)
    with col1:   
        graph_A = px.bar(payy, x="States", y="Transaction_Amount", title = f"{pay['Years'].unique()} Year {quarter} Quarter Transaction Amount",  height = 600, width = 600)
        st.plotly_chart(graph_A)
    with col2:
        graph_C = px.bar(payy, x="States", y="Transaction_Count", title = f"{pay['Years'].unique()} Year {quarter} Quarter Transaction Count",  height = 600, width = 600)
        st.plotly_chart(graph_C)
    
    col1, col2 = st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        map1 = json.loads(response.text)

        State_map = []
        for india in map1["features"]:
            State_map.append(india["properties"]["ST_NM"])
        State_map.sort()
        
        India_map = px.choropleth(payy,geojson = map1, locations = "States", featureidkey = "properties.ST_NM",color = "Transaction_Amount", color_continuous_scale = "Rainbow", 
                                range_color =(payy["Transaction_Amount"].min(), payy["Transaction_Amount"].max()),
                                hover_name = "States", title = f"{pay['Years'].unique()} Year {quarter} Transaction Amount", fitbounds = "locations",  height = 600, width = 600)

        India_map.update_geos(visible = False)
        st.plotly_chart(India_map)
    
    with col2:    
        India_map1 = px.choropleth(payy,geojson = map1, locations = "States", featureidkey = "properties.ST_NM",color = "Transaction_Count", color_continuous_scale = "Rainbow", 
                                range_color = (payy["Transaction_Count"].min(), payy["Transaction_Count"].max()),
                                hover_name = "States", title = f"{pay['Years'].unique()} Year {quarter} TRANSACTION Count", fitbounds = "locations",  height = 600, width = 600)

        India_map1.update_geos(visible = False)
        st.plotly_chart(India_map1)
    
    return pay        

# We are Aggregated Transaction States and viewing them in the Bar Chart:        
def A_T_S(df, state):
    pay = df[df["States"] == state]
    pay.reset_index(drop=True, inplace=True)

    payy = pay.groupby("Transaction_Type")[["Transaction_Count", "Transaction_Amount"]].sum().reset_index()
    
    col1,col2 = st.columns(2)
    with col1:
        graph_A = px.bar(payy, x="Transaction_Type", y="Transaction_Amount", title = f"{state} Transaction Amount",  height = 600, width = 600)
        st.plotly_chart(graph_A)
        
    with col2:
        graph_C = px.bar(payy, x="Transaction_Type", y="Transaction_Count", title = f"{state} Transaction Count",  height = 600, width = 600)
        st.plotly_chart(graph_C)
                
# We are Aggregated User Years and viewing them in the Bar Chart:        
def A_T_U (df,year):
    payuy = df[df["Years"] == year]
    payuy.reset_index(drop= True, inplace = True)
    
    payyuy = pd.DataFrame(payuy.groupby("Brands")["Transaction_Count"].sum())
    payyuy.reset_index(inplace = True)
    
    graph_A = px.bar(payyuy, x = "Brands", y = "Transaction_Count", title = f"{year} Brands And The Transaction_Count",width=1500)
    st.plotly_chart(graph_A)
    
    return payuy 

# We are Aggregated User Quaters and viewing them in the Bar Chart:
def A_T_U_Q (df,quarter):
    payuyq = df[df["Quater"] == quarter]
    payuyq.reset_index(drop= True, inplace = True)
    
    payyuyq = pd.DataFrame(payuyq.groupby("Brands")["Transaction_Count"].sum())
    payyuyq.reset_index(inplace = True)
    
    graph_A = px.bar(payyuyq, x = "Brands", y = "Transaction_Count", title = f"{quarter} Quarter, Brands And The Transaction_Count",width=1500)
    st.plotly_chart(graph_A)
    
    return payuyq

# We are Aggregated User States and viewing them in the Bar Chart:
def A_T_U_S(df, state):
    payu = df[df["States"] == state]
    payu.reset_index(drop=True, inplace=True)
    
    graph_A = px.bar(payu, x="Brands", y="Transaction_Count", hover_data = "Percentage", title = f"{state} Brands, Transaction Count, Percentage", width = 1500)
    st.plotly_chart(graph_A)
    
# We are Map Transaction and viewing them in the Bar Chart:
def M_T_D(df, state):
    pay = df[df["States"] == state]
    pay.reset_index(drop=True, inplace=True)

    payy = pay.groupby("Districts")[["Transaction_Count", "Transaction_Amount"]].sum().reset_index()
    
    col1, col2 = st.columns(2)
    with col1:
        graph_A = px.bar(payy, x="Transaction_Amount", y="Districts", height=500, title = f"{state} Districts and Transaction Amount")
        st.plotly_chart(graph_A)
    with col2:
        graph_C = px.bar(payy, x="Transaction_Count", y="Districts", height=500, title = f"{state} Districts and Transaction Count")
        st.plotly_chart(graph_C)

# We are Map Users Years and viewing them in the Bar Chart:        
def M_U_Y (df,year):
    mapy = df[df["Years"] == year]
    mapy.reset_index(drop= True, inplace = True)
    
    mapyy = mapy.groupby("States")[["Registered_Users", "AppOpens"]].sum()
    mapyy.reset_index(inplace = True)
    
    mapyy_long = pd.melt(mapyy, id_vars=["States"], value_vars=["Registered_Users", "AppOpens"],
                         var_name="Metric", value_name="Count")    
    graph_A = px.bar(mapyy_long, x="States", y="Count", color="Metric", height = 700, width = 1500, title=f"{year} Registered Users and App Opens by State", barmode="group",
                     labels={"Count": "Count"}, color_discrete_map={"Registered_Users": "white", "AppOpens": "Blue"})
    st.plotly_chart(graph_A)
    
    return mapy 

# We are Map Users Quaters and viewing them in the Bar Chart:
def M_U_Q (df,quarter):
    mapq = df[df["Quater"] == quarter]
    mapq.reset_index(drop= True, inplace = True)
    
    mapyq = mapq.groupby("States")[["Registered_Users", "AppOpens"]].sum()
    mapyq.reset_index(inplace = True)
    
    mapy_long_q = pd.melt(mapyq, id_vars=["States"], value_vars=["Registered_Users", "AppOpens"],
                         var_name="Metric", value_name="Count")    
    graph_A = px.bar(mapy_long_q, x="States", y="Count", color="Metric", height = 700, width = 1500, title=f"{quarter} Registered Users and App Opens by State", barmode="group",
                     labels={"Count": "Count"}, color_discrete_map={"Registered_Users": "sky Blue", "AppOpens": "White"})
    st.plotly_chart(graph_A)
    
    return mapq

# We are Map Users Districts and viewing them in the Bar Chart:
def M_U_D(df, state):
    pays = df[df["States"] == state]
    pays.reset_index(drop=True, inplace=True)
    
    col1, col2 = st.columns(2)
    with col1:
        graph_A = px.bar(pays, x="Registered_Users", y="Districts", height=500, width = 1000, title = f"{state} Registered Users")
        st.plotly_chart(graph_A)
    with col2:
        graph_C = px.bar(pays, x="AppOpens", y="Districts", height=500, width = 1000, title = f"{state} AppOpens")
        st.plotly_chart(graph_C)       
                          
# We are Top Transaction States and viewing them in the Bar Chart:
def T_T_D(df, state):
    tops = df[df["States"] == state]
    tops.reset_index(drop = True, inplace = True)
    
    col1, col2 = st.columns(2)
    with col1:
        graph_T = px.bar(tops, x = "Quater", y = "Transaction_Amount", hover_data = "Pincodes", title = "Transaction Amount", height = 550)
        st.plotly_chart(graph_T)
    with col2:
        graph_U = px.bar(tops, x = "Quater", y = "Transaction_Count", hover_data = "Pincodes", title = "Transaction Counts", height = 550)
        st.plotly_chart(graph_U)  

# We are Top Users Years and viewing them in the Bar Chart:    
def T_U (df, year):
    topu = df[df["Years"]== year]
    topu.reset_index(drop = True, inplace = True)
    
    topus = pd.DataFrame(topu.groupby(["States", "Quater"])["RegisteredUsers"].sum())
    topus.reset_index(inplace = True)
    
    graph_Top = px.bar(topu, x= "States", y = "RegisteredUsers", color = "Quater", width = 1500, height = 900, hover_name = "States", title = f"{year} Registered Users")
    st.plotly_chart(graph_Top)
    
    return topu

# We are Top Users States and viewing them in the Bar Chart: 
def T_U_S (df, state):
    toptus = df[df["States"] == state]
    toptus.reset_index( drop = True, inplace = True)
    
    graph_User = px.bar(toptus, x= "Quater", y = "RegisteredUsers", title = "RegisteredUsers, Pincodes, Quaters", width = 1500, height = 800,
                        color = "RegisteredUsers", hover_data = "Pincodes")
    st.plotly_chart(graph_User)

################################################################################################################################################

# Codes for the Top Charts:
# Establishing the Connection To MySQL and We are getting the Answers for the 10 Questions that we have Created:
# Viewing the Results in the India Map and In Bar Charts as well:

def I_M_T_A(choose_table):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Suresh@01",
        database="phone"
    )
    cursor = mydb.cursor()

    query_01 = f"""SELECT States, SUM(Transaction_Amount) AS Transaction_Amount
        FROM {choose_table}
        GROUP BY States
        ORDER BY Transaction_Amount DESC
        LIMIT 10;"""
        
    cursor.execute(query_01)
    rows = cursor.fetchall()
    mydb.commit()

    data_base_01 = pd.DataFrame(rows, columns=["States", "Transaction_Amount"])

    col1, col2 = st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        map1 = json.loads(response.content)

        State_map = [india["properties"]["ST_NM"] for india in map1["features"]]
        State_map.sort()

        merged_data = map1.copy()
        for feature in merged_data["features"]:
            state_name = feature["properties"]["ST_NM"]
            if state_name in data_base_01["States"].values:
                row = data_base_01[data_base_01["States"] == state_name]
                feature["properties"]["Transaction_Amount"] = row["Transaction_Amount"].values[0]
            else:
                feature["properties"]["Transaction_Amount"] = 0
                
# Create a choropleth map using Plotly Express with the merged data
        India_map_01 = px.choropleth_mapbox(data_base_01,geojson=merged_data,locations="States",featureidkey="properties.ST_NM",
            color="Transaction_Amount",color_continuous_scale="Rainbow",
            range_color=(data_base_01["Transaction_Amount"].min(), data_base_01["Transaction_Amount"].max()),
            hover_name="States",title=" This are the Top 10 Transaction Amount by State",mapbox_style="carto-positron",zoom=3,
            center={"lat": 20.5937, "lon": 78.9629},opacity=0.7,width=650,height=650)
        st.plotly_chart(India_map_01)


    query_02 = f"""SELECT States, SUM(Transaction_Amount) AS Transaction_Amount
        FROM {choose_table}
        GROUP BY States
        ORDER BY Transaction_Amount
        LIMIT 10;"""
        
    cursor.execute(query_02)
    rows = cursor.fetchall()
    mydb.commit()

    data_base_02 = pd.DataFrame(rows, columns=["States", "Transaction_Amount"])

    with col2:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        map1 = json.loads(response.content)

        State_map = [india["properties"]["ST_NM"] for india in map1["features"]]
        State_map.sort()

        merged_data = map1.copy()
        for feature in merged_data["features"]:
            state_name = feature["properties"]["ST_NM"]
            if state_name in data_base_02["States"].values:
                row = data_base_02[data_base_02["States"] == state_name]
                feature["properties"]["Transaction_Amount"] = row["Transaction_Amount"].values[0]
            else:
                feature["properties"]["Transaction_Amount"] = 0

# Create a choropleth map using Plotly Express with the merged data
        India_map_02 = px.choropleth_mapbox(data_base_02,geojson=merged_data,locations="States",featureidkey="properties.ST_NM",
            color="Transaction_Amount",color_continuous_scale="Rainbow",
            range_color=(data_base_02["Transaction_Amount"].min(), data_base_02["Transaction_Amount"].max()),
            hover_name="States",title=" This are the Least 10 Transaction Amount by State",mapbox_style="carto-positron",zoom=3,
            center={"lat": 20.5937, "lon": 78.9629},opacity=0.7,width=650,height=650)
        st.plotly_chart(India_map_02)


    query_03 = f"""SELECT States, AVG(Transaction_Amount) AS Transaction_Amount
        FROM {choose_table}
        GROUP BY States
        ORDER BY Transaction_Amount;"""
        
    cursor.execute(query_03)
    rows = cursor.fetchall()
    mydb.commit()

    data_base_03 = pd.DataFrame(rows, columns=["Transaction_Amount", "States"])

    col1, col2 = st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        map1 = json.loads(response.content)

        State_map = [india["properties"]["ST_NM"] for india in map1["features"]]
        State_map.sort()

        merged_data = map1.copy()
        for feature in merged_data["features"]:
            state_name = feature["properties"]["ST_NM"]
            if state_name in data_base_03["States"].values:
                row = data_base_03[data_base_03["States"] == state_name]
                feature["properties"]["Transaction_Amount"] = row["Transaction_Amount"].values[0]
            else:
                feature["properties"]["Transaction_Amount"] = 0
                
# Create a choropleth map using Plotly Express with the merged data
        India_map_03 = px.choropleth_mapbox(data_base_03,geojson=merged_data,locations="Transaction_Amount",featureidkey="properties.ST_NM",
            color="States",color_continuous_scale="Rainbow",
            range_color=(data_base_03["States"].min(), data_base_03["States"].max()),
            hover_name="Transaction_Amount",title="This are the Total Transaction Amount for all States",mapbox_style="carto-positron",zoom=3,
            center={"lat": 20.5937, "lon": 78.9629},opacity=0.7,width=500,height=500)
        st.plotly_chart(India_map_03)
        

def I_M_T_C(choose_table):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Suresh@01",
        database="phone"
    )
    cursor = mydb.cursor()

    query_01 = f"""SELECT States, SUM(Transaction_Count) AS Transaction_Count
        FROM {choose_table}
        GROUP BY States
        ORDER BY Transaction_Count DESC
        LIMIT 10;""" 
        
    cursor.execute(query_01)
    rows = cursor.fetchall()
    mydb.commit()

    data_base_01 = pd.DataFrame(rows, columns=["States", "Transaction_Count"])

    col1, col2 = st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        map1 = json.loads(response.content)

        State_map = [india["properties"]["ST_NM"] for india in map1["features"]]
        State_map.sort()

        merged_data = map1.copy()
        for feature in merged_data["features"]:
            state_name = feature["properties"]["ST_NM"]
            if state_name in data_base_01["States"].values:
                row = data_base_01[data_base_01["States"] == state_name]
                feature["properties"]["Transaction_Count"] = row["Transaction_Count"].values[0]
            else:
                feature["properties"]["Transaction_Count"] = 0

# Create a choropleth map using Plotly Express with the merged data
        India_map_01 = px.choropleth_mapbox(data_base_01,geojson=merged_data,locations="States",featureidkey="properties.ST_NM",
            color="Transaction_Count",color_continuous_scale="Rainbow",
            range_color=(data_base_01["Transaction_Count"].min(), data_base_01["Transaction_Count"].max()),
            hover_name="States",title=" This are the Top 10 Transaction Count by State",mapbox_style="carto-positron",zoom=3,
            center={"lat": 20.5937, "lon": 78.9629},opacity=0.7,width=650,height=650)
        st.plotly_chart(India_map_01)


    query_02 = f"""SELECT States, SUM(Transaction_Count) AS Transaction_Count
        FROM {choose_table}
        GROUP BY States
        ORDER BY Transaction_Count
        LIMIT 10;"""
        
    cursor.execute(query_02)
    rows = cursor.fetchall()
    mydb.commit()

    data_base_02 = pd.DataFrame(rows, columns=["States", "Transaction_Count"])

    with col2:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        map1 = json.loads(response.content)

        State_map = [india["properties"]["ST_NM"] for india in map1["features"]]
        State_map.sort()

        merged_data = map1.copy()
        for feature in merged_data["features"]:
            state_name = feature["properties"]["ST_NM"]
            if state_name in data_base_02["States"].values:
                row = data_base_02[data_base_02["States"] == state_name]
                feature["properties"]["Transaction_Count"] = row["Transaction_Count"].values[0]
            else:
                feature["properties"]["Transaction_Count"] = 0

# Create a choropleth map using Plotly Express with the merged data
        India_map_02 = px.choropleth_mapbox(data_base_02,geojson=merged_data,locations="States",featureidkey="properties.ST_NM",
            color="Transaction_Count",color_continuous_scale="Rainbow",
            range_color=(data_base_02["Transaction_Count"].min(), data_base_02["Transaction_Count"].max()),
            hover_name="States",title=" This are the Least 10 Transaction Count by State",mapbox_style="carto-positron",zoom=3,
            center={"lat": 20.5937, "lon": 78.9629},opacity=0.7,width=650,height=650)
        st.plotly_chart(India_map_02)


    query_03 = f"""SELECT States, AVG(Transaction_Count) AS Transaction_Count
        FROM {choose_table}
        GROUP BY States
        ORDER BY Transaction_Count;"""
        
    cursor.execute(query_03)
    rows = cursor.fetchall()
    mydb.commit()

    data_base_03 = pd.DataFrame(rows, columns=["Transaction_Count", "States"])

    col1, col2 = st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        map1 = json.loads(response.content)

        State_map = [india["properties"]["ST_NM"] for india in map1["features"]]
        State_map.sort()

        merged_data = map1.copy()
        for feature in merged_data["features"]:
            state_name = feature["properties"]["ST_NM"]
            if state_name in data_base_03["States"].values:
                row = data_base_03[data_base_03["States"] == state_name]
                feature["properties"]["Transaction_Count"] = row["Transaction_Count"].values[0]
            else:
                feature["properties"]["Transaction_Count"] = 0

# Create a choropleth map using Plotly Express with the merged data
        India_map_03 = px.choropleth_mapbox(data_base_03,geojson=merged_data,locations="Transaction_Count",featureidkey="properties.ST_NM",
            color="States",color_continuous_scale="Rainbow",
            range_color=(data_base_03["States"].min(), data_base_03["States"].max()),
            hover_name="Transaction_Count",title="This are the Total Transaction Count for all States",mapbox_style="carto-positron",zoom=3,
            center={"lat": 20.5937, "lon": 78.9629},opacity=0.7,width=900,height=700)
        st.plotly_chart(India_map_03)


def I_M_R_U(choose_table, state):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Suresh@01",
        database="phone"
    )
    cursor = mydb.cursor()
    query_01 = f"""SELECT Districts, SUM(Registered_Users) AS Registered_Users
        FROM {choose_table}
        Where States = '{state}'
        GROUP BY Districts
        ORDER BY Registered_Users DESC
        LIMIT 10;"""
        
    cursor.execute(query_01)
    rows = cursor.fetchall()
    mydb.commit()
    data_base_01 = pd.DataFrame(rows, columns=("Districts", "Registered_Users"))
    
# Create a Bar Chart map using Plotly Express with the merged data
    col1, col2 = st.columns(2)
    with col1:
        graph_f = px.bar(data_base_01, x = "Districts", y = "Registered_Users", title = "This are the Top 10 Registered Users by Districts", hover_name = "Districts",height = 700, width = 700 )
        st.plotly_chart(graph_f)
    
    query_02 = f"""SELECT Districts, SUM(Registered_Users) AS Registered_Users
        FROM {choose_table}
        Where States = '{state}'
        GROUP BY Districts
        ORDER BY Registered_Users
        LIMIT 10;"""
        
    cursor.execute(query_02)
    rows = cursor.fetchall()
    mydb.commit()
    data_base_02 = pd.DataFrame(rows, columns=("Districts", "Registered_Users"))

# Create a Bar Chart map using Plotly Express with the merged data
    with col2:
        graph_g = px.bar(data_base_02, x = "Districts", y = "Registered_Users", title = "This are the Least 10 Registered Users by Districts", hover_name = "Districts",height = 700, width = 700 )
        st.plotly_chart(graph_g)
        
    query_03 = f"""SELECT Districts, AVG(Registered_Users) AS Registered_Users
    FROM {choose_table}
    Where States = '{state}'
    GROUP BY Districts
    ORDER BY Registered_Users;"""
    
    cursor.execute(query_03)
    rows = cursor.fetchall()
    mydb.commit()
    data_base_03 = pd.DataFrame(rows, columns=("Districts", "Registered_Users"))

# Create a Bar Chart map using Plotly Express with the merged data
    graph_h = px.bar(data_base_03, x = "Districts", y = "Registered_Users", title = " This are the The Total Registered Users by Districts", hover_name = "Districts",height = 700, width = 1500 )
    st.plotly_chart(graph_h)
    


def I_M_A_O(choose_table, state):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Suresh@01",
        database="phone"
    )
    cursor = mydb.cursor()

    query_01 = f"""SELECT Districts, SUM(AppOpens) AS AppOpens
        FROM {choose_table}
        Where States = '{state}'
        GROUP BY Districts
        ORDER BY AppOpens DESC
        LIMIT 10;"""
        
    cursor.execute(query_01)
    rows = cursor.fetchall()
    mydb.commit()
    data_base_01 = pd.DataFrame(rows, columns=("Districts", "AppOpens"))

# Create a Bar Chart map using Plotly Express with the merged data
    col1, col2 = st.columns(2)
    with col1:
        graph_f = px.bar(data_base_01, x = "Districts", y = "AppOpens", title = "This are the Top 10 AppOpens by Districts", hover_name = "Districts",height = 700, width = 700 )
        st.plotly_chart(graph_f)
    
    query_02 = f"""SELECT Districts, SUM(AppOpens) AS AppOpens
        FROM {choose_table}
        Where States = '{state}'
        GROUP BY Districts
        ORDER BY AppOpens
        LIMIT 10;"""
        
    cursor.execute(query_02)
    rows = cursor.fetchall()
    mydb.commit()
    data_base_02 = pd.DataFrame(rows, columns=("Districts", "AppOpens"))

# Create a Bar Chart map using Plotly Express with the merged data
    with col2:
        graph_g = px.bar(data_base_02, x = "Districts", y = "AppOpens", title = "This are the Least 10 AppOpens by Districts", hover_name = "Districts",height = 700, width = 700 )
        st.plotly_chart(graph_g)
        
    query_03 = f"""SELECT Districts, AVG(AppOpens) AS AppOpens
    FROM {choose_table}
    Where States = '{state}'
    GROUP BY Districts
    ORDER BY AppOpens;"""
    
    cursor.execute(query_03)
    rows = cursor.fetchall()
    mydb.commit()
    data_base_03 = pd.DataFrame(rows, columns=("Districts", "AppOpens"))

# Create a Bar Chart map using Plotly Express with the merged data
    graph_h = px.bar(data_base_03, x = "Districts", y = "AppOpens", title = "This are the The Total AppOpens by Districts", hover_name = "Districts",height = 700, width = 1500 )
    st.plotly_chart(graph_h)                  



def R_U_T_U(choose_table):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Suresh@01",
        database="phone"
    )
    cursor = mydb.cursor()

    query_01 = f"""SELECT States, SUM(RegisteredUsers) AS RegisteredUsers
        FROM {choose_table}
        GROUP BY States
        ORDER BY RegisteredUsers DESC
        LIMIT 10;"""
        
    cursor.execute(query_01)
    rows = cursor.fetchall()
    mydb.commit()
    data_base_01 = pd.DataFrame(rows, columns=("States", "RegisteredUsers"))

# Create a Bar Chart map using Plotly Express with the merged data
    col1, col2 = st.columns(2)
    with col1:
        graph_f = px.bar(data_base_01, x = "States", y = "RegisteredUsers", title = "This are the Top 10 Registered Users by States", hover_name = "States",height = 700, width = 700 )
        st.plotly_chart(graph_f)
    
    query_02 = f"""SELECT States, SUM(RegisteredUsers) AS RegisteredUsers
        FROM {choose_table}
        GROUP BY States
        ORDER BY RegisteredUsers
        LIMIT 10;"""
        
    cursor.execute(query_02)
    rows = cursor.fetchall()
    mydb.commit()
    data_base_02 = pd.DataFrame(rows, columns=("States", "RegisteredUsers"))

# Create a Bar Chart map using Plotly Express with the merged data
    with col2:
        graph_g = px.bar(data_base_02, x = "States", y = "RegisteredUsers", title = "This are the Least 10 Registered Users by States", hover_name = "States",height = 700, width = 700 )
        st.plotly_chart(graph_g)
        
    query_03 = f"""SELECT States, AVG(RegisteredUsers) AS RegisteredUsers
        FROM {choose_table}
        GROUP BY States
        ORDER BY RegisteredUsers;"""
        
    cursor.execute(query_03)
    rows = cursor.fetchall()
    mydb.commit()
    data_base_03 = pd.DataFrame(rows, columns=("States", "RegisteredUsers"))

# Create a Bar Chart map using Plotly Express with the merged data
    graph_h = px.bar(data_base_03, x = "States", y = "RegisteredUsers", title = "This are the The Total Registered Users by States", hover_name = "States",height = 700, width = 1500 )
    st.plotly_chart(graph_h)
     
def I_M_S_R(choose_table, state):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Suresh@01",
        database="phone"
    )
    cursor = mydb.cursor()

    query_01 = f"""SELECT Transaction_Type, SUM(Transaction_Amount) AS Transaction_Amount
        FROM {choose_table}
        Where States = '{state}' 
        GROUP BY Transaction_Type
        ORDER BY Transaction_Amount DESC
        LIMIT 10;"""
        
    cursor.execute(query_01)
    rows = cursor.fetchall()
    mydb.commit()
    data_base_01 = pd.DataFrame(rows, columns=("Transaction_Type", "Transaction_Amount"))

# Create a Bar Chart map using Plotly Express with the merged data
    col1, col2 = st.columns(2)
    with col1:
        graph_f = px.bar(data_base_01, x = "Transaction_Type", y = "Transaction_Amount", title = "This are the Top 10 Transaction Amount by Transaction Type", hover_name = "Transaction_Type",height = 700, width = 700 )
        st.plotly_chart(graph_f)
    
    query_02 = f"""SELECT Transaction_Type, SUM(Transaction_Amount) AS Transaction_Amount
        FROM {choose_table}
        Where States = '{state}' 
        GROUP BY Transaction_Type
        ORDER BY Transaction_Amount
        LIMIT 10;"""
        
    cursor.execute(query_02)
    rows = cursor.fetchall()
    mydb.commit()
    data_base_02 = pd.DataFrame(rows, columns=("Transaction_Type", "Transaction_Amount"))

# Create a Bar Chart map using Plotly Express with the merged data
    with col2:
        graph_g = px.bar(data_base_02, x = "Transaction_Type", y = "Transaction_Amount", title = "This are the Least 10 Transaction Amount by Transaction Type", hover_name = "Transaction_Type",height = 700, width = 700 )
        st.plotly_chart(graph_g)
        
    query_03 = f"""SELECT Transaction_Type, AVG(Transaction_Amount) AS Transaction_Amount
    FROM {choose_table}
    Where States = '{state}' 
    GROUP BY Transaction_Type
    ORDER BY Transaction_Amount;"""
    
    cursor.execute(query_03)
    rows = cursor.fetchall()
    mydb.commit()
    data_base_03 = pd.DataFrame(rows, columns=("Transaction_Type", "Transaction_Amount"))

# Create a Bar Chart map using Plotly Express with the merged data
    graph_h = px.bar(data_base_03, x = "Transaction_Type", y = "Transaction_Amount", title = "This are the The Total Transaction Amount by Transaction Type", hover_name = "Transaction_Type",height = 700, width = 1500 )
    st.plotly_chart(graph_h) 



def I_M_B_C(choose_table, state):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Suresh@01",
        database="phone"
    )
    cursor = mydb.cursor()

    query_01 = f"""SELECT Brands, SUM(Transaction_Count) AS Transaction_Count
        FROM {choose_table}
        Where States = '{state}' 
        GROUP BY Brands
        ORDER BY Transaction_Count DESC
        LIMIT 10; """
        
    cursor.execute(query_01)
    rows = cursor.fetchall()
    mydb.commit()
    data_base_01 = pd.DataFrame(rows, columns=("Brands", "Transaction_Count"))

# Create a Bar Chart map using Plotly Express with the merged data
    col1, col2 = st.columns(2)
    with col1:
        graph_f = px.bar(data_base_01, x = "Transaction_Count", y = "Brands", title = "This are the Top 10 Transaction Count by Brands", hover_name = "Brands",height = 700, width = 700 )
        st.plotly_chart(graph_f)
    
    query_02 = f"""SELECT Brands, SUM(Transaction_Count) AS Transaction_Count
        FROM {choose_table}
        Where States = '{state}' 
        GROUP BY Brands
        ORDER BY Transaction_Count
        LIMIT 10;"""
        
    cursor.execute(query_02)
    rows = cursor.fetchall()
    mydb.commit()
    data_base_02 = pd.DataFrame(rows, columns=("Brands", "Transaction_Count"))

# Create a Bar Chart map using Plotly Express with the merged data
    with col2:
        graph_g = px.bar(data_base_02, x = "Transaction_Count", y = "Brands", title = "This are the Least 10 Transaction Count by Brands", hover_name = "Transaction_Count",height = 700, width = 700 )
        st.plotly_chart(graph_g)
        
    query_03 = f"""SELECT Brands, AVG(Transaction_Count) AS Transaction_Count
    FROM {choose_table}
    Where States = '{state}' 
    GROUP BY Brands
    ORDER BY Transaction_Count;"""
    
    cursor.execute(query_03)
    rows = cursor.fetchall()
    mydb.commit()
    data_base_03 = pd.DataFrame(rows, columns=("Brands", "Transaction_Count"))

# Create a Bar Chart map using Plotly Express with the merged data
    graph_h = px.bar(data_base_03, x = "Transaction_Count", y = "Brands", title = "The Total Transaction Count", hover_name = "Transaction_Count",height = 700, width = 1500 )
    st.plotly_chart(graph_h)   


def I_M_B_Per(choose_table, state):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Suresh@01",
        database="phone"
    )
    cursor = mydb.cursor()

    query_01 = f"""SELECT Brands, SUM(Percentage) AS Percentage
        FROM {choose_table}
        Where States = '{state}' 
        GROUP BY Brands
        ORDER BY Percentage DESC
        LIMIT 10;"""
        
    cursor.execute(query_01)
    rows = cursor.fetchall()
    mydb.commit()
    data_base_01 = pd.DataFrame(rows, columns=("Brands", "Percentage"))

# Create a Bar Chart map using Plotly Express with the merged data
    col1, col2 = st.columns(2)
    with col1:
        graph_f = px.bar(data_base_01, x = "Percentage", y = "Brands", title = "This are the Top 10 Brands by Percentage", hover_name = "Brands",height = 700, width = 700 )
        st.plotly_chart(graph_f)
    
    query_02 = f"""SELECT Brands, SUM(Percentage) AS Percentage
        FROM {choose_table}
        Where States = '{state}' 
        GROUP BY Brands
        ORDER BY Percentage
        LIMIT 10;"""
        
    cursor.execute(query_02)
    rows = cursor.fetchall()
    mydb.commit()
    data_base_02 = pd.DataFrame(rows, columns=("Brands", "Percentage"))

# Create a Bar Chart map using Plotly Express with the merged data
    with col2:
        graph_g = px.bar(data_base_02, x = "Percentage", y = "Brands", title = "This are the Least 10 Brands by Percentage", hover_name = "Percentage",height = 700, width = 700 )
        st.plotly_chart(graph_g)
        
    query_03 = f"""SELECT Brands, AVG(Percentage) AS Percentage
    FROM {choose_table}
    Where States = '{state}' 
    GROUP BY Brands
    ORDER BY Percentage;"""
    
    cursor.execute(query_03)
    rows = cursor.fetchall()
    mydb.commit()
    
    data_base_03 = pd.DataFrame(rows, columns=("Brands", "Percentage"))

# Create a Bar Chart map using Plotly Express with the merged data
    graph_h = px.bar(data_base_03, x = "Percentage", y = "Brands", title = "This are The Total Brands by Percentage", hover_name = "Percentage",height = 700, width = 1500 )
    st.plotly_chart(graph_h)   

##############################################################################################################################################

# Streamlit Part

st.set_page_config(layout='wide')
st.title("Phonepe Pulse Data Visualization")

# Sidebar menu
option = st.sidebar.selectbox("Main menu", ["Home", "Data Exploration", "Top Charts"])

# Display content based on selected option
if option == "Home":
    st.write("Welcome to the Home page!")
    
    col1,col2 = st.columns(2)
    with col1:
        st.header("PhonePe")
        st.subheader(" Thank You For Choosing Phonepe")

elif option == "Data Exploration":
    st.write("Explore the data here!")
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])
    with tab1:
        tab_selected = st.radio("Select the Analysis Method", ["Transaction Analysis", "User Analysis"])
    
        if tab_selected == "Transaction Analysis":
            st.write("Perform Transaction Analysis here!")
            
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Years",p_aggregated_transaction["Years"].min(), p_aggregated_transaction["Years"].max(), p_aggregated_transaction["Years"].min())
            payye = A_T_Y(p_aggregated_transaction, years)
                
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The States", payye["States"].unique())
            A_T_S(payye, states)
            
            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarters",payye["Quater"].min(), payye["Quater"].max(), payye["Quater"].min())    
            payye_q = A_T_Q(payye, quarters)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox(" The Select States", payye["States"].unique())
            A_T_S(payye, states)        
                
        elif tab_selected == "User Analysis":
            st.write("Perform User Analysis here!")
            
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year",p_aggregated_users["Years"].min(), p_aggregated_users["Years"].max(), p_aggregated_users["Years"].min())
            payye1 = A_T_U(p_aggregated_users,years)
                
            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter",payye1["Quater"].min(), payye1["Quater"].max(), payye1["Quater"].min())    
            payye_q = A_T_U_Q(payye1, quarters)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State", payye_q["States"].unique())
            A_T_U_S(payye_q, states)    
        
    
    with tab2:
        tab_selected2 = st.radio("Select the Analysis Method", ["Map Transaction", "Map User"])
    
        if tab_selected2 == "Map Transaction":
            st.write("Perform Map Transaction Analysis here!")
            
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Years for Analysis",p_map_transaction["Years"].min(), p_map_transaction["Years"].max(), p_map_transaction["Years"].min())
            payye_t = A_T_Y(p_map_transaction, years)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The States for Analysis", payye_t["States"].unique())
            M_T_D(payye_t, states)
            
            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarters for Analysis", payye_t["Quater"].min(), payye_t["Quater"].max(), payye_t["Quater"].min())    
            payye_qt = A_T_Q( payye_t, quarters)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox(" The Selected States for Analysis", payye_qt["States"].unique())
            M_T_D(payye_qt, states)
                
        elif tab_selected2 == "Map User":
            st.write("Perform  Map User Analysis here!")
            
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year for Analysis",p_map_users["Years"].min(), p_map_users["Years"].max(), p_map_users["Years"].min())
            map_u_y = M_U_Y (p_map_users, years)
            
            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter for Analysis", map_u_y["Quater"].min(), map_u_y["Quater"].max(), map_u_y["Quater"].min())    
            map_u_q = M_U_Q(map_u_y, quarters)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Selected The State for Analysis", map_u_q["States"].unique())
            M_U_D(map_u_q, states)
                     
    with tab3:
        tab_selected3 = st.radio("Select the Analysis Method", ["Top Transaction", "Top User"])
    
        if tab_selected3 == "Top Transaction":
            st.write("Perform Top Transaction Analysis here!")
            
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Years to View",p_top_transaction["Years"].min(), p_top_transaction["Years"].max(), p_top_transaction["Years"].min())
            top_y = A_T_Y(p_top_transaction, years)
        
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The States to View", top_y["States"].unique())
            T_T_D(top_y, states)
            
            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarters for View", top_y["Quater"].min(), top_y["Quater"].max(), top_y["Quater"].min())    
            top_t_q =  A_T_Q (top_y, quarters)
 
        elif tab_selected3 == "Top User":
            st.write("Perform Top User Analysis here!")
            
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider(" The Selected Year to View",p_top_users["Years"].min(), p_top_users["Years"].max(), p_top_users["Years"].min())
            top_u_y = T_U(p_top_users, years)
             
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Selected The State to View", top_u_y["States"].unique())
            T_U_S(top_u_y, states)
            
            
elif option == "Top Charts":
    st.write("View top charts")
    
    Questions = st.selectbox(" Select the Question", ["1. What is the total Transaction Amount and Count for Aggregated Transaction?",
                                                      "2. What is the total Transaction Amount and Count for Map Transaction?",
                                                      "3. What is the total Transaction Amount and Count for Top Transaction?",
                                                      "4. How does the Transaction Amount vary for different Transaction Types?",
                                                      "5. Which Brands have the highest Transaction Count?",
                                                      "6. What are the percentages associated with different Brands?",
                                                      "7. How many transactions are counted for Aggregated Users?",
                                                      "8. How many Registered Users are there in Map Users?",
                                                      "9. How many times have the App Opens occurred in Map Users?",
                                                      "10. What is the count of Registered Users among the Top Users?"])

    if Questions == "1. What is the total Transaction Amount and Count for Aggregated Transaction?":
        
        st.subheader("Transaction Amount")
        I_M_T_A("aggregated_transaction")
        
        st.subheader("Transaction Count")
        I_M_T_C("aggregated_transaction")
        
    elif Questions == "2. What is the total Transaction Amount and Count for Map Transaction?":
        
        st.subheader("Transaction Amount")
        I_M_T_A("map_transaction")
        
        st.subheader("Transaction Count")
        I_M_T_C("map_transaction")
        
    elif Questions ==  "3. What is the total Transaction Amount and Count for Top Transaction?":
        
        st.subheader("Transaction Amount")
        I_M_T_A("top_transaction")
        
        st.subheader("Transaction Count")
        I_M_T_C("top_transaction")
                
    elif Questions == "4. How does the Transaction Amount vary for different Transaction Types?":       
        P_Type = st.selectbox("Select The States To View", p_aggregated_transaction ["States"].unique())
        st.subheader("Transaction_Amount")
        I_M_S_R("aggregated_transaction", P_Type)
        
    elif Questions == "5. Which Brands have the highest Transaction Count?":       
        P_Brands = st.selectbox("Select The States To View", p_aggregated_users ["States"].unique())
        st.subheader("Transaction_Count")
        I_M_B_C(" aggregated_users", P_Brands)        
        
    elif Questions == "6. What are the percentages associated with different Brands?":       
        P_Percent = st.selectbox("Select The States To View", p_aggregated_users ["States"].unique())
        st.subheader("Percentage")
        I_M_B_Per(" aggregated_users", P_Percent)            
        
    elif Questions == "7. How many transactions are counted for Aggregated Users?":        
        st.subheader("Transaction Count")
        I_M_T_C("aggregated_users")
        
    elif Questions == "8. How many Registered Users are there in Map Users?":       
        P_state = st.selectbox("Select The States To View", p_map_users ["States"].unique())
        st.subheader("Registered Users")
        I_M_R_U("map_users", P_state)
        
    elif Questions == "9. How many times have the App Opens occurred in Map Users?":       
        P_state = st.selectbox("Select The States To View", p_map_users ["States"].unique())
        st.subheader("AppOpens")
        I_M_A_O("map_users", P_state)
        
    elif Questions == "10. What is the count of Registered Users among the Top Users?":       
        st.subheader("RegisteredUsers")
        R_U_T_U("top_users")
        
############################################################# The End #####################################################################################       
import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image


#dataframe Creation


mydb=mysql.connector.connect(host='localhost', user='root', password='srinidhi@123',database='phonepe')
cursor=mydb.cursor()

#Aggregated_insurance_df

cursor.execute("select * from aggregated_insurance")
#mydb.commit()
table0=cursor.fetchall()

aggre_insurance=pd.DataFrame(table0, columns=("states","years","Quarter","Transaction_type",
                                              "Transaction_count","Transaction_Amount"))

mydb=mysql.connector.connect(host='localhost', user='root', password='srinidhi@123',database='phonepe')
cursor=mydb.cursor()

#Aggregated_Transaction_df

cursor.execute("select * from aggregated_transaction")
#mydb.commit()
table1=cursor.fetchall()

aggre_transaction=pd.DataFrame(table1, columns=("states","years","Quarter","Transaction_type"
                                              ,"Transaction_count","Transaction_Amount"))

mydb=mysql.connector.connect(host='localhost', user='root', password='srinidhi@123',database='phonepe')
cursor=mydb.cursor()

#Aggregated_user_df

cursor.execute("select * from aggregated_user")
#mydb.commit()
table2=cursor.fetchall()

aggre_user=pd.DataFrame(table2, columns=("states","years","Quarter","Brands"
                                              ,"Transaction_count","Percentage"))


mydb=mysql.connector.connect(host='localhost', user='root', password='srinidhi@123',database='phonepe')
cursor=mydb.cursor()

#map_insurance_table

cursor.execute("select * from map_insurance")
#mydb.commit()
table3=cursor.fetchall()

map_insurance=pd.DataFrame(table3, columns=("states","years","Quarter","Districts"
                                              ,"Transaction_count","Transaction_Amount"))

mydb=mysql.connector.connect(host='localhost', user='root', password='srinidhi@123',database='phonepe')
cursor=mydb.cursor()


#map_Transaction_table

cursor.execute("select * from map_transaction")
#mydb.commit()
table4=cursor.fetchall()

map_tran=pd.DataFrame(table4, columns=("states","years","Quarter","Districts"
                                              ,"Transaction_count","Transaction_Amount"))


mydb=mysql.connector.connect(host='localhost', user='root', password='srinidhi@123',database='phonepe')
cursor=mydb.cursor()


#map_user_table

cursor.execute("select * from map_user")
#mydb.commit()
table5=cursor.fetchall()

map_user=pd.DataFrame(table5, columns=("states","years","Quarter","Districts"
                                              ,"RegisteredUsers","AppOpens"))

mydb=mysql.connector.connect(host='localhost', user='root', password='srinidhi@123',database='phonepe')
cursor=mydb.cursor()


#top_insurance_table

cursor.execute("select * from top_insurance")
#mydb.commit()
table6=cursor.fetchall()

top_insurance=pd.DataFrame(table6, columns=("states","years","Quarter","Pincodes"
                                              ,"Transaction_count","Transaction_Amount"))


mydb=mysql.connector.connect(host='localhost', user='root', password='srinidhi@123',database='phonepe')
cursor=mydb.cursor()


#top_transaction_table

cursor.execute("select * from top_transaction")
#mydb.commit()
table7=cursor.fetchall()

top_transaction=pd.DataFrame(table7, columns=("states","years","Quarter","Pincodes"
                                              ,"Transaction_count","Transaction_Amount"))

mydb=mysql.connector.connect(host='localhost', user='root', password='srinidhi@123',database='phonepe')
cursor=mydb.cursor()


#top_user_table

cursor.execute("select * from top_user")
#mydb.commit()
table8=cursor.fetchall()

top_user=pd.DataFrame(table8, columns=("states","years","Quarter","Pincodes"
                                              ,"RegisteredUsers"))


#Transaction year based
def Transaction_Amount_Count_y(df,year):


    TACY=df[df["years"] == year]
    TACY.reset_index(drop=True,inplace=True)


    TACYG=TACY.groupby("states")[["Transaction_count","Transaction_Amount"]].sum()
    TACYG.reset_index(inplace=True)


    column1,column2= st.columns(2)
    with column1:


        fig_amount= px.bar(TACYG, x="states", y="Transaction_Amount", title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence= px.colors.sequential.Agsunset,height=650,width=600)
        st.plotly_chart(fig_amount)

    with column2:

        fig_count= px.bar(TACYG, x="states", y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence= px.colors.sequential.Bluered,height=650,width=600)
        st.plotly_chart(fig_count)


    column1,column2=st.columns(2)
    with column1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

        response= requests.get(url)
        data1= json.loads(response.content)

        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1=px.choropleth(TACYG,geojson=data1,locations="states",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(TACYG["Transaction_count"].min(),TACYG["Transaction_count"].max()),
                                hover_name= "states", title= f"{year} TRANSACTION COUNT", fitbounds="locations",

                                )
        
        fig_india_1.update_geos(visible= False)

        st.plotly_chart(fig_india_1)

    with column2:

        fig_india_2=px.choropleth(TACYG,geojson=data1,locations="states",featureidkey="properties.ST_NM",
                                color="Transaction_Amount",color_continuous_scale="Rainbow",
                                range_color=(TACYG["Transaction_Amount"].min(),TACYG["Transaction_Amount"].max()),
                                hover_name= "states", title= f"{year} TRANSACTION AMOUNT", fitbounds="locations",

                                )
        
        fig_india_2.update_geos(visible= False)

        st.plotly_chart(fig_india_2)

    return TACY

#Transaction Quarter based
def Transaction_Amount_Count_y_Q(df,quarter):

    TACY=df[df["Quarter"] == quarter]
    TACY.reset_index(drop=True,inplace=True)


    TACYG=TACY.groupby("states")[["Transaction_count","Transaction_Amount"]].sum()
    TACYG.reset_index(inplace=True)

    column1,column2= st.columns(2)
    with column1:

        fig_amount= px.bar(TACYG, x="states", y="Transaction_Amount", title=f"{TACY['years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence= px.colors.sequential.Agsunset,height=600,width=600)
        st.plotly_chart(fig_amount)

    with column2:
        fig_count= px.bar(TACYG, x="states", y="Transaction_count", title=f"{TACY['years'].min()} YEAR {quarter} QUARTER{quarter} TRANSACTION COUNT",
                        color_discrete_sequence= px.colors.sequential.Bluered,height=600,width=600)
        st.plotly_chart(fig_amount)


    column1,column2= st.columns(2)
    with column1:
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

        response= requests.get(url)
        data1= json.loads(response.content)

        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1=px.choropleth(TACYG,geojson=data1,locations="states",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(TACYG["Transaction_count"].min(),TACYG["Transaction_count"].max()),
                                hover_name= "states", title= f"{TACY['years'].min()} YEAR {quarter} QUARTER{quarter} TRANSACTION COUNT", fitbounds="locations",

                                )
        
        fig_india_1.update_geos(visible= False)

        st.plotly_chart(fig_india_1)

    with column2:
        fig_india_2=px.choropleth(TACYG,geojson=data1,locations="states",featureidkey="properties.ST_NM",
                                color="Transaction_Amount",color_continuous_scale="Rainbow",
                                range_color=(TACYG["Transaction_Amount"].min(),TACYG["Transaction_Amount"].max()),
                                hover_name= "states", title= f"{TACY['years'].min()} YEAR {quarter} QUARTER{quarter} TRANSACTION AMOUNT", fitbounds="locations",

                                )
        
        fig_india_2.update_geos(visible= False)

        st.plotly_chart(fig_india_2)
    return TACY

#Transaction Type
def aggre_trans_Transaction_type(df,state):


    TACY=df[df["states"] == state]
    TACY.reset_index(drop=True,inplace=True)

    TACYG=TACY.groupby("Transaction_type")[["Transaction_count","Transaction_Amount"]].sum()
    TACYG.reset_index(inplace=True)

    column1,column2= st.columns(2)
    with column1:

        fig_pie_1= px.pie(data_frame=TACYG, names= "Transaction_type", values = "Transaction_Amount",
                        width= 600, title= f"{state.upper()} TRANSACTION AMOUNT",hole=0.5 )

        st.plotly_chart(fig_pie_1)
    
    
    with column2:

        fig_pie_2= px.pie(data_frame=TACYG, names= "Transaction_type", values = "Transaction_count",
                        width= 600, title=f"{state.upper()} TRANSACTION COUNT",hole=0.5 )

        st.plotly_chart(fig_pie_2)



#aggre_user_analsys_1

def aggre_user_plot_1(df, year):
    aguy=df[df["years"]== year]
    aguy.reset_index(drop=True, inplace= True)

    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)


    fig_bar_1= px.bar(aguyg, x="Brands", y="Transaction_count", title= f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000, color_discrete_sequence= px.colors.sequential.Blackbody,hover_name= "Brands")

    st.plotly_chart(fig_bar_1)

    return aguy


#aggre_user_analysis_2

def aggre_user_plot_2(df, Quarter):
    aguyq=df[df["Quarter"]== Quarter]
    aguyq.reset_index(drop=True, inplace= True)

    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)


    fig_bar_1= px.bar(aguyqg, x="Brands", y="Transaction_count", title= f"{Quarter} Quarter, BRANDS AND TRANSACTION COUNT",
                    width=800, color_discrete_sequence= px.colors.sequential.Blackbody, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq


#map_insurance

def map_insurance_district(df,state):


    TACY=df[df["states"] == state]
    TACY.reset_index(drop=True,inplace=True)

    TACYG=TACY.groupby("Districts")[["Transaction_count","Transaction_Amount"]].sum()
    TACYG.reset_index(inplace=True)                                                                        


    fig_bar_1= px.bar(TACYG, x="Transaction_Amount" , y= "Districts" , orientation="h", title=f"{state.upper()} DISTRICTS AND TRANSACTION AMOUNT ")
    st.plotly_chart(fig_bar_1)

    fig_bar_2= px.bar(TACYG, x="Transaction_count" , y= "Districts" , orientation="h", title=f"{state.upper()} DISTRICTS AND TRANSACTION COUNT ")
    st.plotly_chart(fig_bar_2)

#Map_user_plot_1
def map_user_plot_1(df, year):

    muy=df[df["years"]== year]
    muy.reset_index(drop=True, inplace= True)

    muyg=muy.groupby("states")[["RegisteredUsers","AppOpens"]].sum()
    muyg.reset_index(inplace=True)

    fig_line_1=px.line(muyg, x= "states", y=["RegisteredUsers","AppOpens"], 
                    title= f"{year} REGISTERED USER, APPOPENS",width=1000,height=800,markers=True)

    st.plotly_chart(fig_line_1)
    return muy


#Map_user_plot_2
def map_user_plot_2(df, Quarter	):

    muyq=df[df["Quarter"]== Quarter	]
    muyq.reset_index(drop=True, inplace= True)

    muyqg=muyq.groupby("states")[["RegisteredUsers","AppOpens"]].sum()
    muyqg.reset_index(inplace=True)

    fig_line_1=px.line(muyqg, x= "states", y=["RegisteredUsers","AppOpens"], 
                    title= f"{df['years'].min()} YEARS {Quarter} QUARTER REGISTERED USER, APPOPENS",width=1000,height=800,markers=True,
                    color_discrete_sequence= px.colors.sequential.Rainbow_r)

    st.plotly_chart(fig_line_1)
    return muyq



#map_user_plot_3
def map_user_plot_3(df, states):
    muyqs=df[df["states"]== states]
    muyqs.reset_index(drop=True, inplace= True)

    column1,column2=st.columns(2)
    with column1:

        fig_map_user_bar_1=px.bar(muyqs, x="RegisteredUsers", y="Districts", orientation= "h",
                                title=f"{states.upper()} REGISTERED USER", height=800, color_discrete_sequence= px.colors.sequential.amp_r)

        st.plotly_chart(fig_map_user_bar_1)

    with column2:

        fig_map_user_bar_2=px.bar(muyqs, x="AppOpens", y="Districts", orientation= "h",
                                title=f"{states.upper()} APPOPENS", height=800)

        st.plotly_chart(fig_map_user_bar_2)



 #top_insurance_plot_1
def top_insurance_plot_1(df, state):

    tiy=df[df["states"]== state]
    tiy.reset_index(drop=True, inplace= True)

    tiyg=tiy.groupby("Pincodes")[["Transaction_count","Transaction_Amount"]].sum()
    tiyg.reset_index(inplace=True)


    column1,column2=st.columns(2)
    with column1:

        fig_top_insurance_bar_1=px.bar(tiy, x="Quarter", y="Transaction_Amount", hover_data= "Pincodes",
                                    title="TRANSACTION AMOUNT", height=800, color_discrete_sequence= px.colors.sequential.amp_r)

        st.plotly_chart(fig_top_insurance_bar_1)

    with column2:

        fig_top_insurance_bar_2=px.bar(tiy, x="Quarter", y="Transaction_count", hover_data= "Pincodes",
                                    title="TRANSACTION cOUNT", height=800, color_discrete_sequence= px.colors.sequential.amp_r)

        st.plotly_chart(fig_top_insurance_bar_2)



def top_user_plot_1(df, year):

    tuy=df[df["years"]== year]
    tuy.reset_index(drop=True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["states", "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)


    fig_top_plot_1 = px.bar(tuyg, x="states", y="RegisteredUsers", color="Quarter", width=1000, height=800,
                        hover_name="states", title= f"{year} REGISTERED USERS")

    st.plotly_chart(fig_top_plot_1)              

    return tuy


#top_user_plot_2
def top_user_plot_2(df, state):    
    
    tuys=df[df["states"]== state]
    tuys.reset_index(drop=True, inplace= True)


    fig_top_plot_2= px.bar(tuys, x= "Quarter", y= "RegisteredUsers", title= "REGISTEREDUSER, PINCODES, QUARTER",
                        width=1000, height=800,color="RegisteredUsers", hover_data= "Pincodes")
    
    st.plotly_chart(fig_top_plot_2) 
    


def top_chart_transaction_amount(table_name):

    mydb=mysql.connector.connect(host='localhost', user='root', password='srinidhi@123',database='phonepe')
    cursor=mydb.cursor()
    #plot_1

    query1=f'''select states, sum(Transaction_Amount) as Transaction_Amount
                from {table_name}
                GROUP BY  states
                ORDER BY Transaction_Amount DESC
                LIMIT 10;'''

    cursor.execute(query1)

    table1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table1, columns=("states", "Transaction_Amount"))

    column1,column2=st.columns(2)
    with column1:

        fig_amount_1= px.bar(df_1, x="states", y="Transaction_Amount", title= "TOP 10 OF TRANSACTION AMOUNT", hover_name="states",
                            color_discrete_sequence= px.colors.sequential.Agsunset,height=600,width=600)
        st.plotly_chart(fig_amount_1)


    #plot_2

    query2=f'''select states, sum(Transaction_Amount) as Transaction_Amount
                from {table_name}
                GROUP BY  states
                ORDER BY Transaction_Amount
                LIMIT 10;'''

    cursor.execute(query2)

    table2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table2, columns=("states", "Transaction_Amount"))

    with column2:

        fig_amount_2= px.bar(df_2, x="states", y="Transaction_Amount", title= "LAST 10 OF TRANSACTION AMOUNT", hover_name="states",
                            color_discrete_sequence= px.colors.sequential.Agsunset,height=600,width=600)
        st.plotly_chart(fig_amount_2)



    #plot_3

    query3=f'''select states, AVG(Transaction_Amount) as Transaction_Amount
                from {table_name}
                GROUP BY  states
                ORDER BY Transaction_Amount;'''

    cursor.execute(query3)

    table3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table3, columns=("states", "Transaction_Amount"))

    fig_amount_3= px.bar(df_3, x="Transaction_Amount", y="states", title= "AVERAGE 0F TRANSACTION AMOUNT", hover_name="states", orientation="h",
                        color_discrete_sequence= px.colors.sequential.Agsunset,height=800,width=1000)
    st.plotly_chart(fig_amount_3)


#TRANSACTION COUNT

def top_chart_transaction_count(table_name):

    mydb=mysql.connector.connect(host='localhost', user='root', password='srinidhi@123',database='phonepe')
    cursor=mydb.cursor()
    #plot_1

    query1=f'''select states, sum(Transaction_count) as Transaction_count
                from {table_name}
                GROUP BY  states
                ORDER BY Transaction_count DESC
                LIMIT 10;'''

    cursor.execute(query1)

    table1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table1, columns=("states", "Transaction_count"))
    
    column1,column2=st.columns(2)
    with column1:


        fig_amount_1= px.bar(df_1, x="states", y="Transaction_count", title= "TOP 10 OF TRANSACTION COUNT", hover_name="states",
                            color_discrete_sequence= px.colors.sequential.Agsunset,height=600,width=600)
        st.plotly_chart(fig_amount_1)


    #plot_2

    query2=f'''select states, sum(Transaction_count) as Transaction_count
                from {table_name}
                GROUP BY  states
                ORDER BY Transaction_count
                LIMIT 10;'''

    cursor.execute(query2)

    table2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table2, columns=("states", "Transaction_count"))

    with column1:

        fig_amount_2= px.bar(df_2, x="states", y="Transaction_count", title= "LAST 10 OF TRANSACTION COUNT", hover_name="states",
                            color_discrete_sequence= px.colors.sequential.Agsunset,height=600,width=600)
        st.plotly_chart(fig_amount_2)



    #plot_3

    query3=f'''select states, AVG(Transaction_count) as Transaction_count
                from {table_name}
                GROUP BY  states
                ORDER BY Transaction_count;'''

    cursor.execute(query3)

    table3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table3, columns=("states", "Transaction_count"))

    fig_amount_3= px.bar(df_3, x="Transaction_count", y="states", title= "AVERAGE OF TRANSACTION COUNT", hover_name="states", orientation="h",
                        color_discrete_sequence= px.colors.sequential.Agsunset,height=800,width=1000)
    st.plotly_chart(fig_amount_3)

##3############33####3###


def top_chart_Registered_User(table_name, state):

    mydb=mysql.connector.connect(host='localhost', user='root', password='srinidhi@123',database='phonepe')
    cursor=mydb.cursor()
    #plot_1

    query1=f'''select districts, sum(registeredusers) as Registeredusers
                from {table_name}
                where states='{state}'
                group by districts
                order by registeredusers DESC
                LIMIT 10;'''

    cursor.execute(query1)

    table1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table1, columns=("districts", "Registeredusers"))
    
    column1,column2=st.columns(2)
    with column1:

        fig_amount_1= px.bar(df_1, x="districts", y="Registeredusers", title= "top 10 of REGISTERED USER", hover_name="districts",
                            color_discrete_sequence= px.colors.sequential.Agsunset,height=600,width=600)
        st.plotly_chart(fig_amount_1)


    #plot_2

    query2=f'''select districts, AVG(registeredusers) as Registeredusers
                from {table_name}
                where states='{state}'
                group by districts
                order by registeredusers
                LIMIT 10;'''

    cursor.execute(query2)

    table2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table2, columns=("districts", "Registeredusers"))

    with column2:

        fig_amount_2= px.bar(df_2, x="districts", y="Registeredusers", title= "LAST 10 OF REGISTERED USER", hover_name="districts",
                            color_discrete_sequence= px.colors.sequential.Agsunset,height=600,width=600)
        st.plotly_chart(fig_amount_2)


    #plot_3

    query3=f'''select districts, AVG(registeredusers) as Registeredusers
                from {table_name}
                where states='{state}'
                group by districts
                order by registeredusers;'''

    cursor.execute(query3)

    table3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table3, columns=("districts", "Registeredusers"))

    fig_amount_3= px.bar(df_3, y="districts", x="Registeredusers", title= "AVARAGE OF REGISTERED USER", hover_name="districts", orientation="h",
                        color_discrete_sequence= px.colors.sequential.Agsunset,height=800,width=1000)
    st.plotly_chart(fig_amount_3)



def top_chart_appopens(table_name, state):

    mydb=mysql.connector.connect(host='localhost', user='root', password='srinidhi@123',database='phonepe')
    cursor=mydb.cursor()
    #plot_1

    query1=f'''select districts, sum(appopens) as appopens
                from {table_name}
                where states='{state}'
                group by districts
                order by appopens DESC
                LIMIT 10;'''

    cursor.execute(query1)

    table1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table1, columns=("districts", "appopens"))

    column1,column2=st.columns(2)
    with column1:

        fig_amount_1= px.bar(df_1, x="districts", y="appopens", title= "top 10 of APPOPENS", hover_name="districts",
                            color_discrete_sequence= px.colors.sequential.Agsunset,height=600,width=600)
        st.plotly_chart(fig_amount_1)


    #plot_2

    query2=f'''select districts, AVG(appopens) as appopens
                from {table_name}
                where states='{state}'
                group by districts
                order by appopens
                LIMIT 10;'''

    cursor.execute(query2)

    table2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table2, columns=("districts", "appopens"))

    with column2:

        fig_amount_2= px.bar(df_2, x="districts", y="appopens", title= "LAST 10 OF APPOPENS", hover_name="districts",
                            color_discrete_sequence= px.colors.sequential.Agsunset,height=600,width=600)
        st.plotly_chart(fig_amount_2)



    #plot_3

    query3=f'''select districts, AVG(appopens) as appopens
                from {table_name}
                where states='{state}'
                group by districts
                order by appopens;'''

    cursor.execute(query3)

    table3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table3, columns=("districts", "appopens"))

    fig_amount_3= px.bar(df_3, y="districts", x="appopens", title= "AVARAGE OF APPOPENS", hover_name="districts", orientation="h",
                        color_discrete_sequence= px.colors.sequential.Agsunset,height=800,width=1000)
    st.plotly_chart(fig_amount_3)



def top_chart_Registered_Users(table_name):

    mydb=mysql.connector.connect(host='localhost', user='root', password='srinidhi@123',database='phonepe')
    cursor=mydb.cursor()
    #plot_1

    query1=f'''select states, sum(RegisteredUsers) as RegisteredUsers
                from {table_name}
                group by states
                order by registeredusers DESC
                LIMIT 10;'''

    cursor.execute(query1)

    table1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table1, columns=("states", "Registeredusers"))
    column1,column2=st.columns(2)
    with column1:

        fig_amount_1= px.bar(df_1, x="states", y="Registeredusers", title= "top 10 of REGISTERED USERS", hover_name="states",
                            color_discrete_sequence= px.colors.sequential.amp_r,height=600,width=600)
        st.plotly_chart(fig_amount_1)



    #plot_2

    query2=f'''select states, sum(RegisteredUsers) as RegisteredUsers
                from {table_name}
                group by states
                order by registeredusers
                LIMIT 10;'''

    cursor.execute(query2)

    table2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table2, columns=("states", "Registeredusers"))

    with column2:

        fig_amount_2= px.bar(df_2, x="states", y="Registeredusers", title= "LAST 10 OF REGISTERED USERS", hover_name="states",
                            color_discrete_sequence= px.colors.sequential.Agsunset,height=600,width=600)
        st.plotly_chart(fig_amount_2)




    #plot_3

    query3=f'''select states, avg(RegisteredUsers) as RegisteredUsers
                from {table_name}
                group by states
                order by registeredusers;'''

    cursor.execute(query3)

    table3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table3, columns=("states", "Registeredusers"))

    fig_amount_3= px.bar(df_3, y="states", x="Registeredusers", title= "AVARAGE OF REGISTERED USERS", hover_name="states", orientation="h",
                        color_discrete_sequence= px.colors.sequential.amp,height=800,width=1000)
    st.plotly_chart(fig_amount_3)






#streamlit part
st.set_page_config(layout= "wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    
    select=option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP CHARTS"])

if select =="HOME":
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.image(Image.open(r"C:\Users\SunLand\Desktop\images\phonepe1.jpg"),width=500)

    col3,col4= st.columns(2)
    
    with col3:
        st.image(Image.open(r"C:\Users\SunLand\Desktop\images\phonepe2.jpg"),width=400)

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.image(Image.open(r"C:\Users\SunLand\Desktop\images\phonepe3.jpg"),width= 500)




elif select =="DATA EXPLORATION":

    tab1,tab2,tab3=st.tabs(["Aggregated Analysis", "Map Analysis","Top Analysis"])

    with tab1:
        method= st.radio("Select The Method",["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":

            column1,column2= st.columns(2)
            with column1:
                
                years= st.slider("Select The Year",aggre_insurance["years"].min(),aggre_insurance["years"].max(),aggre_insurance["years"].min())
            tac_y=Transaction_Amount_Count_y(aggre_insurance,years)

            column1,column2= st.columns(2)
            with column1:
                
                quarters= st.slider("Select The Quarter",tac_y["Quarter"].min(),tac_y["Quarter"].max(),tac_y["Quarter"].min())
            Transaction_Amount_Count_y_Q(tac_y,quarters)


        elif method == "Transaction Analysis":

            column1,column2= st.columns(2)
            with column1:
                
                years= st.slider("Select The Year",aggre_transaction["years"].min(),aggre_transaction["years"].max(),aggre_transaction["years"].min())
            agre_tran_tac_y=Transaction_Amount_Count_y(aggre_transaction,years)

            column1,column2= st.columns(2)
            with column1:
                states=st.selectbox("Select The State", agre_tran_tac_y["states"].unique())

            aggre_trans_Transaction_type(agre_tran_tac_y,states)

            column1,column2= st.columns(2)
            with column1:
                
                quarters= st.slider("Select The Quarter",agre_tran_tac_y["Quarter"].min(),agre_tran_tac_y["Quarter"].max(),agre_tran_tac_y["Quarter"].min())
            aggre_tran_tac_y_q=Transaction_Amount_Count_y_Q(agre_tran_tac_y,quarters)

            column1,column2= st.columns(2)
            with column1:
                states=st.selectbox("Select The State_Ty", aggre_tran_tac_y_q["states"].unique())

            aggre_trans_Transaction_type(aggre_tran_tac_y_q,states)    


    
        elif method == "User Analysis":

            column1,column2= st.columns(2)
            with column1:
                
                years= st.slider("Select The Year",aggre_user["years"].min(),aggre_user["years"].max(),aggre_user["years"].min())
                aggre_user_y= aggre_user_plot_1(aggre_user, years)



                column1,column2= st.columns(2)
            with column1:
                
                quarters= st.slider("Select The Quarter",aggre_user_y["Quarter"].min(),aggre_user_y["Quarter"].max(),aggre_user_y["Quarter"].min())
            aggre_tran_tac_y_q=aggre_user_plot_2(aggre_user_y,quarters)





        with tab2:
            method_1=st.radio("Select The Method",["Map Insurance","Map Transaction","Map User"])

            if method_1 == "Map Insurance":

                column1,column2= st.columns(2)
                with column1:
                    
                    years= st.slider("Select The Year_Mi",map_insurance["years"].min(),map_insurance["years"].max(),map_insurance["years"].min())
                map_insurance_tac_y=Transaction_Amount_Count_y(map_insurance,years)


                column1,column2= st.columns(2)
                with column1:
                    states=st.selectbox("Select The State_Mi", map_insurance_tac_y["states"].unique())

                map_insurance_district(map_insurance_tac_y,states)


                column1,column2= st.columns(2)
                with column1:
                    
                    quarters= st.slider("Select The Quarter_Mt",map_insurance_tac_y["Quarter"].min(),map_insurance_tac_y["Quarter"].max(),map_insurance_tac_y["Quarter"].min())
                map_insurance_tac_y_q=Transaction_Amount_Count_y_Q(map_insurance_tac_y,quarters)

                column1,column2= st.columns(2)
                with column1:
                    states=st.selectbox("Select The State_Ty", map_insurance_tac_y_q["states"].unique())

                map_insurance_district(map_insurance_tac_y_q,states)




            elif method_1 == "Map Transaction":
                
                column1,column2= st.columns(2)
                with column1:
                    
                    years= st.slider("Select The Year_Mi",map_tran["years"].min(),map_tran["years"].max(),map_tran["years"].min())
                map_transaction_tac_y=Transaction_Amount_Count_y(map_tran,years)


                column1,column2= st.columns(2)
                with column1:
                    states=st.selectbox("Select The State_Mi", map_transaction_tac_y["states"].unique())

                map_insurance_district(map_transaction_tac_y,states)


                column1,column2= st.columns(2)
                with column1:
                    
                    quarters= st.slider("Select The Quarter",map_transaction_tac_y["Quarter"].min(),map_transaction_tac_y["Quarter"].max(),map_transaction_tac_y["Quarter"].min())
                map_transaction_tac_y_q=Transaction_Amount_Count_y_Q(map_transaction_tac_y,quarters)

                column1,column2= st.columns(2)
                with column1:
                    states=st.selectbox("Select The State_Ty", map_transaction_tac_y_q["states"].unique())

                map_insurance_district(map_transaction_tac_y_q,states)





            elif method_1 == "Map User":
                column1,column2= st.columns(2)
                with column1:
                    
                    years= st.slider("Select The Year_Mu",map_user["years"].min(),map_user["years"].max(),map_user["years"].min())
                map_user_y=map_user_plot_1(map_user,years)


                column1,column2= st.columns(2)
                with column1:
                    
                    quarters= st.slider("Select The Quarter_mu",map_user_y["Quarter"].min(),map_user_y["Quarter"].max(),map_user_y["Quarter"].min())
                map_user_y_q=map_user_plot_2(map_user_y,quarters)


                column1,column2= st.columns(2)
                with column1:
                    states=st.selectbox("Select The State_mu", map_user_y_q["states"].unique())

                map_user_plot_3(map_user_y_q, states)





        with tab3:
            method_3=st.radio("Select The Method",["Top Insurance","Top Transaction","Top User"])

            if method_3 == "Top Insurance":

                column1,column2= st.columns(2)
                with column1:
                    
                    years= st.slider("Select The Year_Ti",top_insurance["years"].min(),top_insurance["years"].max(),top_insurance["years"].min())
                top_insurance_tac_y=Transaction_Amount_Count_y(top_insurance,years)

                column1,column2= st.columns(2)
                with column1:
                    states=st.selectbox("Select The State_Ti", top_insurance_tac_y["states"].unique())

                top_insurance_plot_1(top_insurance_tac_y, states)

                column1,column2= st.columns(2)
                with column1:
                    
                    quarters= st.slider("Select The Quarter_mu",top_insurance_tac_y["Quarter"].min(),top_insurance_tac_y["Quarter"].max(),top_insurance_tac_y["Quarter"].min())
                top_insurance_y_q=Transaction_Amount_Count_y_Q(top_insurance_tac_y,quarters)
                
                
            elif method_3 == "Top Transaction":
                column1,column2= st.columns(2)
                with column1:
                    
                    years= st.slider("Select The Year_Tt",top_transaction["years"].min(),top_transaction["years"].max(),top_transaction["years"].min())
                top_transaction_tac_y=Transaction_Amount_Count_y(top_transaction,years)

                column1,column2= st.columns(2)
                with column1:
                    states=st.selectbox("Select The State_Tt", top_transaction_tac_y["states"].unique())

                top_insurance_plot_1(top_transaction_tac_y, states)

                column1,column2= st.columns(2)
                with column1:
                    
                    quarters= st.slider("Select The Quarter_Tt",top_transaction_tac_y["Quarter"].min(),top_transaction_tac_y["Quarter"].max(),top_transaction_tac_y["Quarter"].min())
                top_transaction_tac_y_q=Transaction_Amount_Count_y_Q(top_transaction_tac_y,quarters)
                
            elif method_3 == "Top User":
                column1,column2= st.columns(2)
                with column1:
                    
                    years= st.slider("Select The Year_Tu",top_user["years"].min(),top_user["years"].max(),top_user["years"].min())
                top_user_y=top_user_plot_1(top_user,years)


                column1,column2= st.columns(2)
                with column1:
                    states=st.selectbox("Select The State_Tt", top_user_y["states"].unique())

                top_user_plot_2(top_user_y, states)


                

elif select =="TOP CHARTS":

        question= st.selectbox("select the question" , ["1. Transaction Amount and Count of Aggregated Insurance",
                                                        "2. Transaction Amount and Count of Map Insurance",
                                                        "3. Transaction Amount and Count of Top Insurance",
                                                        "4. Transaction Amount and Count of Aggregated Transaction",
                                                        "5. Transaction Amount and Count of Map Transaction",
                                                        "6. Transaction Amount and Count of Top Transaction",
                                                        "7. Transaction Count of Aggregated User",
                                                        "8. Registered Users of Map User",
                                                        "9. App Opens of Map User",
                                                        "10.Registered Users of Top User",
                                                        ])
        
        if question == "1. Transaction Amount and Count of Aggregated Insurance":

            st.subheader("TRANSACTION AMOUNT")
            top_chart_transaction_amount("aggregated_insurance")

            st.subheader("TRANSACTION COUNT")
            top_chart_transaction_count("aggregated_insurance")


        elif question == "2. Transaction Amount and Count of Map Insurance":

            st.subheader("TRANSACTION AMOUNT")
            top_chart_transaction_amount("map_insurance")
            
            st.subheader("TRANSACTION COUNT")
            top_chart_transaction_count("map_insurance")


        elif question == "3. Transaction Amount and Count of Top Insurance":

            st.subheader("TRANSACTION AMOUNT")
            top_chart_transaction_amount("top_insurance")
            
            st.subheader("TRANSACTION COUNT")
            top_chart_transaction_count("top_insurance")


        elif question == "4. Transaction Amount and Count of Aggregated Transaction":

            st.subheader("TRANSACTION AMOUNT")
            top_chart_transaction_amount("aggregated_transaction")
            
            st.subheader("TRANSACTION COUNT")
            top_chart_transaction_count("aggregated_transaction")


        elif question == "5. Transaction Amount and Count of Map Transaction":

            st.subheader("TRANSACTION AMOUNT")
            top_chart_transaction_amount("map_transaction")
            
            st.subheader("TRANSACTION COUNT")
            top_chart_transaction_count("map_transaction")


        elif question == "6. Transaction Amount and Count of Top Transaction":

            st.subheader("TRANSACTION AMOUNT")
            top_chart_transaction_amount("top_transaction")
            
            st.subheader("TRANSACTION COUNT")
            top_chart_transaction_count("top_transaction")



        elif question == "7. Transaction Count of Aggregated User":
            
            st.subheader("TRANSACTION COUNT")
            top_chart_transaction_count("aggregated_user")


        elif question == "8. Registered Users of Map User":

            states=st.selectbox("select the state", map_user["states"].unique())
            st.subheader("REGISTERED USERS")
            top_chart_Registered_User("Map_User", states)


        elif question == "9. App Opens of Map User":

            states=st.selectbox("select the state", map_user["states"].unique())
            st.subheader("APPOPENS")
            top_chart_appopens("Map_User", states)

        elif question == "10.Registered Users of Top User":

            #states=st.selectbox("select the state", map_user["states"].unique())
            st.subheader("REGISTERED USERS")
            top_chart_Registered_Users("top_user")







        
        
        
        
        



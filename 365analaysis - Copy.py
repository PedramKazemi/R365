from ast import Index
from asyncio.windows_events import NULL
from distutils.errors import CompileError
from enum import auto
import imp
from multiprocessing.sharedctypes import Value
from re import A, M, U, X
from tkinter import Y
from tokenize import Double
from turtle import color
import datetime
from unicodedata import name
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import convert_numbers
import plotly.graph_objects as go
from plotly.subplots import make_subplots






conn = psycopg2.connect(
database="R365", user='postgres', password='971406138', host='localhost', port= '5432'
)
cur = conn.cursor()

# rowNumber = int(input("chose ur row number in database : "))


def tablesName():
    myQuery = '''SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema='public' AND table_type='BASE TABLE'
    '''
    cur.execute(myQuery)
    result = cur.fetchall()
    return result


def tableSize(tableName):
    myQuery = f'SELECT count(*) from {tableName};'
    cur.execute(myQuery)
    result = cur.fetchone()
    return result[0]

def getData(tableName , name = "" , rowNumber = int):
    cur.execute(f'''SELECT * from {tableName}''')
    Rows = cur.fetchall()
    sValue = 0
    for row in Rows:
        sName = name
        if row[0] == sName:
            sValue = row[rowNumber]   #for last price row number is 3
        else:
            pass
    return sValue


def allValues(name = "" , rowNumber = int):
    allValuesList = []
    datename =[]
    ValuesListSeries = []
    for tn in tablesName():
        tn = str(tn)
        tn = tn.replace("'" , "").replace("(" , "").replace(")" , "").replace("," , "")  #prepare tables name

        if "-" in str(getData(tn , name , rowNumber)):
            t = int(convert_numbers.persian_to_english(getData(tn , name , rowNumber)))
            t2 = t - (2*t)
            allValuesList.append(t2)
        # elif "٫" in str(getData(tn , name , rowNumber)):
        #     m = str(getData(tn , name , rowNumber))
        #     m = m.replace("٫" , "/").replace("٪", "")

        #     print(m)
        #     allValuesList.append(int(m))

        else:
            allValuesList.append(int(convert_numbers.persian_to_english(getData(tn , name , rowNumber))))


        # allValuesList.append(int(convert_numbers.persian_to_english(getData(tn , name , 4))))
        datename.append(tn)
    

    
    dates = [datetime.datetime.strptime(ts, "_%Y_%m_%d") for ts in datename]
    sorteddates = [datetime.datetime.strftime(ts, "%Y-%m-%d") for ts in dates]
    datename = sorteddates

    ValuesListSeries =pd.Series(allValuesList , datename , name=name )
    return ValuesListSeries


def drawing(val): #  allValues() data
    nwIndex = []
    for m in val.index:
        m = m.replace("2022" , "").replace("_" , "/").replace("//" , "")
        nwIndex.append(m)
    val.index = nwIndex
    val = val.sort_index(ascending = True)
    plt.plot(val.index , val.values , marker = ".", mew = 3 , color = "purple")   
    plt.title((val.name)[::-1])
    plt.xlabel("Date")
    plt.ylabel("Values")
    plt.margins(0.1)
    plt.grid()
    plt.show()



    # fig = go.Figure(data = go.Scatter(x = val.index , y = val.values))
    # fig.show()

   

def comparisonDrawing(val1 , val2): #  allValues() data
    nwIndex1 = []
    for m in val1.index:
        m = m.replace("2022" , "").replace("_" , "/").replace("//" , "")
        nwIndex1.append(m)
    
    val1.index = nwIndex1
    val1 = val1.sort_index(ascending = True)

    nwIndex2 = []
    for m in val2.index:
        m = m.replace("2022" , "").replace("_" , "/").replace("//" , "")
        nwIndex2.append(m)
    
    val2.index = nwIndex2
    val2 = val2.sort_index(ascending = True)
    
    plt.subplot(2,1,1)
    plt.plot(val1.index , val1.values , marker = ".", mew = 3 , color = "blue")
    plt.title(val1.name)
    plt.xlabel("Date")
    plt.ylabel("Values")
    plt.margins(0.1)
    plt.grid()
    plt.subplot(2,1,2) 
    plt.plot(val2.index , val2.values , marker = ".", mew = 3 , color = "purple" )
    plt.title(val2.name) 
    plt.xlabel("Date")
    plt.ylabel("Values")
    plt.margins(0.1)
    plt.grid()
    plt.tight_layout()

    plt.show()





def months():
    result = []
    

    month1 = []
    month2 = []
    month3 = []
    month4 = []
    month5 = []
    month6 = []
    month7 = []
    month8 = []
    month9 = []
    month10 = []
    month11 = []
    month12 = []
    for tn in tablesName():
        tn = str(tn)
        tn = tn.replace("'" , "").replace("(" , "").replace(")" , "").replace("," , "")  #prepare tables name
        monthNum = tn.split("_")[2]

        if monthNum == "1":
            month1.append(tn)
        if monthNum == "2":
            month2.append(tn)
        if monthNum == "3":
            month3.append(tn)
        if monthNum == "4":
            month4.append(tn)
        if monthNum == "5":
            month5.append(tn)
        if monthNum == "6":
            month6.append(tn)
        if monthNum == "7":
            month7.append(tn)
        if monthNum == "8":
            month8.append(tn)
        if monthNum == "9":
            month9.append(tn)
        if monthNum == "10":
            month10.append(tn)
        if monthNum == "11":
            month11.append(tn)
        if monthNum == "12":
            month12.append(tn)
    
    result.append(month1)
    result.append(month2)
    result.append(month3)
    result.append(month4)
    result.append(month5)
    result.append(month6)
    result.append(month7)
    result.append(month8)
    result.append(month9)
    result.append(month10)
    result.append(month11)
    result.append(month12)

    return result



def risk(symbol):
    changeRate =  allValues(symbol , 4).values
    param1 = sum(changeRate)       # posetive or negetive changes in a period (column 4) 
    lastmin =  allValues(symbol , 3).values
    param2 = min(lastmin)    #min value of the lastprice
    lastmax =  allValues(symbol , 3).values
    param3 = max(lastmax)    #max value of the lastprice
    valmax =  allValues(symbol , 7).values
    param4 = max(valmax)    #min value of the stock
    valmin =  allValues(symbol ,  7).values
    param5 = min(valmin)    #min value of the stock
    changePercent = allValues(symbol , 4).values / (allValues(symbol , 3).values / 100)
    param6 = round(sum(changePercent) , 2)



    riskResult =  {
        "param1":param1,
        "param2":param2,
        "param3":param3,
        "param4":param4,
        "param5":param5,
        "param6":param6
    }

    return riskResult




def monthly(month):
    monthData = []

    if month == 1:
        monthData = months()[0]
    if month == 2:
        monthData = months()[1]
    if month == 3:
        monthData = months()[2]
    if month == 4:
        monthData = months()[3]
    if month == 5:
        monthData = months()[4]
    if month == 6:
        monthData = months()[5]
    if month == 7:
        monthData = months()[6]
    if month == 8:
        monthData = months()[7]
    if month == 9:
        monthData = months()[8]
    if month == 10:
        monthData = months()[9]
    if month == 11:
        monthData = months()[10]
    if month == 12:
        monthData = months()[11]
    

    monthData.sort(reverse=False)

    # for i in monthData:
    #     print(risk("فولاد"))

    return monthData



def riskCal(symbol , month):
    def AVformonth( RNumber):
        mydatas = []
        for tn in monthly(month):
            if "-" in str(getData(tn , symbol , RNumber)):
                t = int(convert_numbers.persian_to_english(getData(tn , symbol , RNumber)))
                t2 = t - (2*t)
                mydatas.append(t2)
            
            else:
                mydata = getData(tn , symbol ,RNumber)
                mydatas.append(int(convert_numbers.persian_to_english(mydata)))
        return mydatas


    changeRate =  AVformonth(4)
    param1 = sum(changeRate)  # posetive or negetive changes in a period (column 4) 
    lastmin =  AVformonth(3)
    param2 = min(lastmin)     # min value of the lastprice
    lastmax =  AVformonth(3)
    param3 = max(lastmax)     # max value of the lastprice
    valmax =  AVformonth(7)
    param4 = max(valmax)      # max value of the stock
    valmin =  AVformonth(7)
    param5 = min(valmin)     # min value of the stock

    i = 0
    j = 0
    param6 = 0
    for m in range(len(AVformonth(4))):
        try:
            mysum = AVformonth(4)[i] / (AVformonth(3)[j] / 100)

        except ZeroDivisionError:
            mysum = 0

                
        i+=1
        j+=1
        param6 += mysum 

    param6 = round(param6 , 2)

    return [param1 , param2 , param3 , param4 , param5 , param6]






def stockDraw(symbol):

    ind = allValues(symbol , 3).index
    op =  allValues(symbol , 8)
    hi =  allValues(symbol , 9)
    low = allValues(symbol , 10)
    cl =  allValues(symbol , 3)

    fig3 = make_subplots(specs=[[{"secondary_y": False}]])
    fig3.add_trace(go.Candlestick(x = ind,
                                open = op,
                                high = hi,
                                low = low,
                                close = cl,
                                ))
    fig3.show()



# stockDraw("فولاد")


def riskDegree():
    mesurment = 0
    changeRate , lastmin , lastmax , valmax , valmin , changePercent = riskCal("آ س پ" , 7)

    # if changePercent > 0:
    #     mesurment += 1
    # else:
    #     mesurment -= 1
    
    # if changeRate > 0:
    #     mesurment += 1
    # else:
    #     mesurment -= 1
    print(changePercent)


    
  

riskDegree()




# print(riskCal("آ س پ" , 7 ))




# monthly(7)

# risk("آ س پ")

# drawing(allValues("آ س پ" , 3))

# comparisonDrawing(allValues("آ س پ") , allValues("فولاد"))

conn.close()

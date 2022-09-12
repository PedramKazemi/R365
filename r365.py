from asyncio.windows_events import NULL
from re import A, X
from turtle import shape
from requests import delete
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import datetime
import psycopg2



def dbName():
   dt = datetime.datetime.today()
   year = dt.year
   month = dt.month
   day = dt.day
   res ="_" + str(year) + "_" + str(month) + "_" + str(day)
   return res

conn = psycopg2.connect(
database="R365", user='postgres', password='971406138', host='localhost', port= '5432'
)
cur = conn.cursor()


def createTable(name):

   myDB =f'''CREATE TABLE {name}(
      symbol text NOT NULL,
      market text NOT NULL,
      datetime text NOT NULL,
      lastprice text NOT NULL,
      changes text NOT NULL,
      changespercent text NOT NULL,
      volume text NOT NULL,
      value text NOT NULL,
      open text NOT NULL,
      most text NOT NULL,
      least text NOT NULL,
      norequest text NOT NULL,
      rprice text NOT NULL,
      sprice text NOT NULL,
      nosupply text NOT NULL

   )'''
   cur.execute(myDB)
   conn.commit()


def insertData():
   postgres_insert_query = f''' INSERT INTO {dbName()} (symbol , market , datetime , lastprice , changes , changespercent , volume , value , open , most , least , norequest , rprice , sprice , nosupply) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
   record_to_insert = (symbol , market , dateTime , lastPrice , changes , changesPercent , volume , value , open , most , least , NORequest , RPrice , SPrice , NOSupply)
   cur.execute(postgres_insert_query, record_to_insert)
   conn.commit()





tdlist = []  #list of a list of a td
finalList = []


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options = options)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver.get("https://rahavard365.com/stock")


print(driver.title)
elem = driver.find_elements(By.TAG_NAME, "tr")




counter = 1


createTable(dbName())




while(counter < 700):
   po = elem[counter].find_elements(By.TAG_NAME, "td")
   symbol = po[0].text
   market = po[1].text
   dateTime =  po[2].text
   lastPrice =  po[3].text
   changes =  po[4].text
   changesPercent =  po[5].text
   changesPercent = changesPercent.replace("▼" , "")
   changesPercent =  changesPercent.replace("▲" , "")
   volume =  po[6].text
   value =  po[7].text
   open =  po[8].text
   most =  po[9].text
   least =  po[10].text
   NORequest =  po[11].text
   RPrice =  po[12].get_attribute('textContent')
   SPrice =  po[13].get_attribute('textContent')
   NOSupply = po[14].get_attribute('textContent')

   insertData()

      
   print(changesPercent)
   print("****")
   counter += 1



driver.close()


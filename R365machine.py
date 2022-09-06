import r365analaysis as RA
import psycopg2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import scale



conn = psycopg2.connect(
database="R365", user='postgres', password='971406138', host='localhost', port= '5432'
)
cur = conn.cursor()


conn2 = psycopg2.connect(
database="skudb", user='postgres', password='971406138', host='localhost', port= '5432'
)
cur2 = conn2.cursor()

tbNames = []

for tn in RA.tablesName():
        tn = str(tn)
        tn = tn.replace("'" , "").replace("(" , "").replace(")" , "").replace("," , "")  #prepare tables name
        tbNames.append(tn)


symbolList = []

for tbn in tbNames:
    cur.execute(f'''SELECT * from {tbn}''')
    Rows = cur.fetchall()
    for row in Rows:
        if row[0] in symbolList:
            pass
        else:
            symbolList.append(row[0])


def mydb():
    RMdb =f'''CREATE TABLE R365MA(
        changeRate int NOT NULL,
        lastmin Bigint NOT NULL,
        lastmax Bigint NOT NULL,
        valmax Bigint NOT NULL,
        valmin Bigint NOT NULL,
        changePercent int NOT NULL,
        degree int NOT NULL
    )'''
    cur2.execute(RMdb)
    conn2.commit()



# mydb()




# for sy in symbolList:

#     changeRate , lastmin , lastmax , valmax , valmin , changePercent = RA.riskCal(sy , 8)

#     if changePercent > 0 and changePercent < 10:
#         degree = 1
#         postgres_insert_query = f''' INSERT INTO R365MA (changeRate , lastmin , lastmax , valmax , valmin , changePercent , degree) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
#         record_to_insert = (changeRate , lastmin , lastmax , valmax , valmin , changePercent , degree)
#         cur2.execute(postgres_insert_query, record_to_insert)
#         conn2.commit()

#     elif changePercent > 10 and changePercent < 20:
#         degree = 2
#         postgres_insert_query = f''' INSERT INTO R365MA (changeRate , lastmin , lastmax , valmax , valmin , changePercent , degree) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
#         record_to_insert = (changeRate , lastmin , lastmax , valmax , valmin , changePercent , degree)
#         cur2.execute(postgres_insert_query, record_to_insert)
#         conn2.commit()

#     elif changePercent >= 20:
#         degree = 3
#         postgres_insert_query = f''' INSERT INTO R365MA (changeRate , lastmin , lastmax , valmax , valmin , changePercent , degree) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
#         record_to_insert = (changeRate , lastmin , lastmax , valmax , valmin , changePercent , degree)
#         cur2.execute(postgres_insert_query, record_to_insert)
#         conn2.commit()

#     elif changePercent < 0 and changePercent > -10:
#         degree = -1
#         postgres_insert_query = f''' INSERT INTO R365MA (changeRate , lastmin , lastmax , valmax , valmin , changePercent , degree) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
#         record_to_insert = (changeRate , lastmin , lastmax , valmax , valmin , changePercent , degree)
#         cur2.execute(postgres_insert_query, record_to_insert)
#         conn2.commit()


#     elif changePercent < -10 and changePercent > -20:
#         degree = -2
#         postgres_insert_query = f''' INSERT INTO R365MA (changeRate , lastmin , lastmax , valmax , valmin , changePercent , degree) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
#         record_to_insert = (changeRate , lastmin , lastmax , valmax , valmin , changePercent , degree)
#         cur2.execute(postgres_insert_query, record_to_insert)
#         conn2.commit()

#     elif changePercent < -20 :
#         degree = -3
#         postgres_insert_query = f''' INSERT INTO R365MA (changeRate , lastmin , lastmax , valmax , valmin , changePercent , degree) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
#         record_to_insert = (changeRate , lastmin , lastmax , valmax , valmin , changePercent , degree)
#         cur2.execute(postgres_insert_query, record_to_insert)
#         conn2.commit()

    




dataset = pd.read_csv("r365ma.csv")

degrees = dataset['degree']

dataset = dataset.drop(['degree'] , axis = 1)

scaleData = scale(dataset)

myDataset = pd.DataFrame(scaleData , index = dataset.index , columns = dataset.columns)

myDataset["degree"] = degrees
dataset = myDataset

x = dataset.iloc[:, :-1].values
y = dataset.loc[: , "degree"].values


x_train , x_test , y_train , y_test = train_test_split(x , y , test_size = 0.1 , shuffle = True)
knn = KNeighborsClassifier(n_neighbors = 3 , metric = "minkowski" , p = 1)
knn.fit(x_train , y_train)


# print(scale([10000,52,1,-815558,577,55554120,-98521150]))


print(knn.score(x_test , y_test))


print(knn.predict([[-0.0676800785122315 , -0.370385182471324 , -0.466231235453143 , -0.248777263727249 , 0.10437556839274 , 0.788120792422413]]))
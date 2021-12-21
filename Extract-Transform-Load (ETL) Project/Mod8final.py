#import drivers
import mysql.connector
import csv
import matplotlib.pyplot as plt

#Turn csv data into a working list
with open('PartialCleanFinal3.csv') as csv_file: #worked 2nd time around after saying it as another .csv in excel
    csvfile = csv.reader(csv_file)
    totalvalue = []
    for row in csvfile:
        value = (row[0],row[1],row[2],row[3],row[4],row[5])
        totalvalue.append(value)

#common info when adding a server to read from
mydb = mysql.connector.connect(
    user='root',
    password='password', #INPUT YOUR PASSWORD FOR YOUR LOCAL MACHINE
    host='localhost',
    auth_plugin='mysql_native_password')

#create database
mycursor = mydb.cursor()

mycursor.execute("DROP DATABASE IF EXISTS testmydb")
mycursor.execute("CREATE DATABASE IF NOT EXISTS testmydb")

mycursor.execute("SHOW DATABASES")
for db in mycursor:
    print(db)
print('')

#create table
mycursor.execute("USE testmydb")
mycursor.execute("CREATE TABLE business (id int NOT NULL,naciscode VARCHAR(30),description VARCHAR(100),year int NOT NULL,month VARCHAR(3),total int NOT NULL)")


mycursor.executemany("INSERT INTO business VALUES(%s,%s,%s,%s,%s,%s)",totalvalue)
mydb.commit()

#check work
mycursor.execute("SHOW COLUMNS IN business")
for cols in mycursor:
    print(cols)

#check output
#mycursor.execute("SELECT * FROM business")
#for data in mycursor:
#    print(data)


#Queries copied over from MySQL into Python
#Query 1
#mycursor.execute("SELECT * FROM business ORDER BY id")
#for output in mycursor:
#    print(output)
#    print('') #create spaces between answers

#Query 2
mycursor.execute("SELECT total FROM business WHERE total IS NULL")
for output in mycursor:
    print(output)
    print('') #create spaces between answers

mycursor.execute("SELECT COUNT(total) FROM business WHERE total IS NOT NULL")
for output in mycursor:
    print(output)
    print('') #create spaces between answers

#Query 3
mycursor.execute("SELECT DISTINCT year FROM business")
for output in mycursor:
    print(output)
    print('') #create spaces between answers

mycursor.execute("SELECT DISTINCT month FROM business")
for output in mycursor:
    print(output)
    print('') #create spaces between answers

# A lot of data populates, but check the bottom of the list to ensure same values from above are present from
# Queries 2 and 3

#GRAPHING DATA
#Trends of retail total sales vs year
query = ('''
SELECT (sum(total)/1000/1000) AS total, year
FROM business
WHERE description = 'Retail and food services sales, total' AND year != 2021
GROUP BY year; 
''')

mycursor.execute(query)

year = []
total = []

for row in mycursor.fetchall():
    #print(row)
    total.append(row[0])
    year.append(row[1])

plt.plot(year,total)
plt.xlabel('Years')
plt.ylabel('Total Sales (trillions)')
plt.title('Retail & Food Service Sales vs Year')
plt.show()
plt.close()

#Same Process as above but with Book stores / Sporting goods stores / Hobby, toy, and game stores
#Trends of retail total sales vs year
#common info when adding a server to read from
query = ('''
SELECT (sum(total)/1000) AS total, year
FROM business
WHERE description = 'Book stores' AND year != 2021
GROUP BY year; 
''')

mycursor.execute(query)

year = []
booktotal = []

for row in mycursor.fetchall():
    #print(row)
    booktotal.append(row[0])
    year.append(row[1])

query = ('''
SELECT (sum(total)/1000) AS total, year
FROM business
WHERE description = 'Sporting goods stores' AND year != 2021
GROUP BY year; 
''')

mycursor.execute(query)

sporttotal = []

for row in mycursor.fetchall():
    #print(row)
    sporttotal.append(row[0])

query = ('''
SELECT (sum(total)/1000) AS total, year
FROM business
WHERE description = 'Hobby, toy, and game stores' AND year != 2021
GROUP BY year; 
''')

mycursor.execute(query)

hobbytotal = []

for row in mycursor.fetchall():
    #print(row)
    hobbytotal.append(row[0])

plt.plot(year,booktotal, label = 'book sales')
plt.plot(year,sporttotal, label = 'sports sales')
plt.plot(year,hobbytotal, label = 'hobby sales')
plt.xlabel('Years')
plt.ylabel('Total Sales (billions)')
plt.title('Book/Sports/Hobby Store Sales vs Year')
plt.legend(loc='upper left')
plt.show()
plt.close()

#PERCENTAGE CHANGE
#Men's clothing stores and Women's clothing stores Percentage Change
#Creation of Query
query = ('''
SELECT (sum(total)/1000) AS total, year
FROM business
WHERE description = "Men's clothing stores" AND year != 2021
GROUP BY year; 
''')

mycursor.execute(query)

year = []
mentotal = []

for row in mycursor.fetchall():
    #print(row)
    mentotal.append(row[0])
    year.append(row[1])

query = ('''
SELECT (sum(total)/1000) AS total, year
FROM business
WHERE description = "Women's clothing stores" AND year != 2021
GROUP BY year; 
''')

mycursor.execute(query)

womentotal = []

for row in mycursor.fetchall():
    #print(row)
    womentotal.append(row[0])


plt.plot(year,mentotal, label = "Men's Clothing")
plt.plot(year,womentotal, label = "Women's Clothing")
plt.xlabel('Years')
plt.ylabel('Total Sales (in billions)')
plt.title('Men/Women Clothing Total Sales vs Year')
plt.legend(loc='upper left')
plt.show()
plt.close()

#Calculate Percent Change for each
import numpy as np
mencentchg = np.array(mentotal,dtype=float)
womencentchg = np.array(womentotal,dtype=float)

mencentchg = np.diff(mencentchg) / mencentchg[:-1] * 100.
womencentchg = np.diff(womencentchg) / womencentchg[:-1] * 100.

mencentchg = mencentchg.tolist()
womencentchg = womencentchg.tolist()

#reshape data
year.pop(0)
year.pop(0)
mencentchg.pop(0)
womencentchg.pop(0)


plt.plot(year,mencentchg, label = "Men's Clothing")
plt.plot(year,womencentchg, label = "Women's Clothing")
plt.xlabel('Years')
plt.ylabel('Percent Change')
plt.title('Men/Women Clothing % Change vs Year')
plt.legend(loc='upper right')
plt.show()
plt.close()

#ROLLING WINDOWS
#Creation of Query
query = ('''
SELECT (total/1000), month, year
FROM business
WHERE description = 'Shoe stores' AND year != 2021
Order by year;
''')

mycursor.execute(query)

year = []
month = []
shoetotal = []

for row in mycursor.fetchall():
    #print(row)
    shoetotal.append(row[0])
    month.append(row[1])
    year.append(row[2])
    
query = ('''
SELECT (total/1000), month, year
FROM business
WHERE description = 'Jewelry stores' AND year != 2021
Order by year;
''')

mycursor.execute(query)

jewelrytotal = []

for row in mycursor.fetchall():
    #print(row)
    jewelrytotal.append(row[0])
   
    
#close MySQL Shell
mycursor.close()
mydb.close()

#create a dataframe
import pandas as pd
df = pd.DataFrame({'shoetotal':shoetotal, 'jewelrytotal':jewelrytotal, 'month':month, 'year':year})
df['shoetotal']=df['shoetotal'].astype(float)
df['jewelrytotal']=df['jewelrytotal'].astype(float)

#check graph
df.plot.line(x='year', y=['shoetotal','jewelrytotal'])

#moving average 
df['MovingAvgShoe'] = df['shoetotal'].rolling(window=12).mean()
df['MovingAvgJewelry'] = df['jewelrytotal'].rolling(window=12).mean()

df.head()

#check moving average plot
df.plot.line(x='year', y=['MovingAvgShoe','MovingAvgJewelry'])

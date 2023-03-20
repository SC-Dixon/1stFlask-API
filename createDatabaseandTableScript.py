import pandas as pd
import os
import mysql.connector as mysql
from mysql.connector import Error

path_to_csv = os.path.join(os.getcwd(), 'Customers.csv')

custdata = pd.read_csv(path_to_csv, index_col=False,delimiter=',')
x = "Not Provided"
custdata["Profession"].fillna(x, inplace=True)
custdata.head()

try:
    conn = mysql.connect(host='127.0.0.1',user='lab3user', password='lab3password')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("DROP DATABASE IF EXISTS lab3cust;")
        cursor.execute("CREATE DATABASE lab3cust;")
        print("Database was successfully created!")
        cursor.close()
    conn.close()
except Error as e:
    print("Error occured while connecting to MySQL", e)

try:
    conn = mysql.connect(host='127.0.0.1', database='lab3cust', user='lab3user', password='lab3password')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You are connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS customer;')
        print('Creating table....')
        cursor.execute("CREATE TABLE customer(CustomerID int NOT NULL, Gender varchar(6), Age int, AnnualIncome int, SpendingScore int, Profession varchar(75), WorkExperience int, FamilySize int, PRIMARY KEY(CustomerID));")
        print("Table was sucesssfully created!")
        for i,row in custdata.iterrows():
            sql = "INSERT INTO lab3cust.customer VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            conn.commit()
        print("VALUES successfully inserted into customer table!!")
        cursor.close()
    conn.close()
except Error as e:
    print("Error occured while connecting to MySQL", e)


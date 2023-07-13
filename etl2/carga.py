import csv
import pymysql
from flask import Flask, request, jsonify
from pymongo import MongoClient
import os


mysql_conn = pymysql.connect(
    host="172.21.0.2",
    port=3306,
    database="my",
    user="root",
    password="mypassword"
)


def insert_data_mysql(data):
    cursor = mysql_conn.cursor()

    for item in data:
        # Realizar las operaciones de inserción en MySQL
        sql = "INSERT INTO etl (LocationAbbr, LocationDesc, DataSource, Topic, Question, DataValueType, DataValue, DataValueAlt, StratificationCategory1, Stratification1, LocationID, TopicID, QuestionID, DataValueTypeID, StratificationCategoryID1, StratificationID1, actualizado_en, Duration, Latitude, Longitude, seguir) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            item['LocationAbbr'],
            item['LocationDesc'],
            item['DataSource'],
            item['Topic'],
            item['Question'],
            item['DataValueType'],
            item['DataValue'],
            item['DataValueAlt'],
            item['StratificationCategory1'],
            item['Stratification1'],
            item['LocationID'],
            item['TopicID'],
            item['QuestionID'],
            item['DataValueTypeID'],
            item['StratificationCategoryID1'],
            item['StratificationID1'],
            item['actualizado_en'],
            item['Duration'],
            item['Latitude'],
            item['Longitude'],
            item['seguir']
        )
        cursor.execute(sql, values)

    mysql_conn.commit()
    cursor.close()


def save_data_csv(data):
    csv_filename = "data.csv"

    # Verifica si el archivo ya existe
    file_exists = os.path.isfile(csv_filename)

    with open(csv_filename, mode='a' if file_exists else 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())

        if not file_exists:
            writer.writeheader()

        writer.writerows(data)


def transform_data(item):
    # transformed_item = {}  # Crea un nuevo diccionario para almacenar el resultado transformado

    # Realiza la transformación del item
    #
    # transformed_item['edad'] = 2023 - item['birth_year']  # Ejemplo: Calcula la edad a partir del año de nacimiento

    return item

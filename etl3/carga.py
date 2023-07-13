from flask import Flask, request, jsonify
from pymongo import MongoClient
import os




def transform_data(item):
    # transformed_item = {}  # Crea un nuevo diccionario para almacenar el resultado transformado

    # Realiza la transformación del item
    #
    # transformed_item['edad'] = 2023 - item['birth_year']  # Ejemplo: Calcula la edad a partir del año de nacimiento

    return item

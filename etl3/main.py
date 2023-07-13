import requests
import json
from datetime import datetime



# URL de la API que deseas llamar
url = "http://127.0.0.1:7000/api/data"

# Realiza la solicitud GET a la API
response = requests.get(url)

# Verifica el código de estado de la respuesta
if response.status_code == 200:
    # La solicitud fue exitosa
    data = response.json()  # Obtiene los datos de la respuesta en formato JSON

    for datau in data:
        if 'height' in datau:
            datau['height'] = float(datau['height'].replace(' m', ''))
        if 'weight' in datau:
            datau['weight'] = float(datau['weight'].replace(' kg', ''))
    # reemplazar "Not in Eggs" por 0 y limpiar ' km' en egg
        if 'egg' in datau:
            if datau['egg'] == 'Not in Eggs':
                datau['egg'] = 0
            else:
                datau['egg'] = float(datau['egg'].replace(' km', '')) if ' km' in datau['egg'] else datau['egg']
        

        datau.pop("_id", None)

    keys = datau.keys()


   
    jdata = json.dumps(data)
    """ json_data = json.loads(jdata)
    print(type(jdata)) """
    #print(keys)
    print(jdata)

else:
    # La solicitud no fue exitosa
    print("Error en la solicitud:", response.status_code)

respuesta = input('¿Desea ejecutar la carga de datos? (y/n): ')
if respuesta.lower() == 'y':
    url2 = "http://localhost:5000/api/load"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url2, jdata, headers=headers)

    
else:
    print('No se ejecutará la carga de datos.')

from flask import Flask, request
import cv2
import face_recognition
import json
import base64
from PIL import Image
from io import BytesIO
import numpy as np
import re
import psycopg2
from psycopg2 import Error

app = Flask(__name__)
if __name__ == '__main__':
    app.debug = True
    app.run()

def get_from_base64(codec):
    byte_data = base64.b64decode(codec)
    image_data = BytesIO(byte_data)
    with Image.open(image_data) as img:
        img = img.convert('RGB')
    return np.array(img)

def buscar_usuario_por_id(usuario):
    try:        
        connection = psycopg2.connect(
            #conexion a la Base de datos
            user="postgres",
            password="airepick123",
            host="localhost",
            port="5433",
            database="gambarte11"
        )

        cursor = connection.cursor()
        query = """SELECT foto FROM usuarios WHERE usuario = %s"""
        cursor.execute(query, (usuario,))
        usuario = cursor.fetchone()
        if usuario:
           return usuario[0]

        else:
            print("No se encontró ningún usuario con ese ID.")

    except (Exception, Error) as error:
        print("Error al conectar a la base de datos:", error)

    finally:
        if connection:
            cursor.close()
            connection.close()



@app.route('/facial', methods=['POST'])
def upload_file():
    file3 = request.get_json()
    json_image = face_recognition.face_encodings(get_from_base64(file3.get("foto")))
    face_encodings_local = face_recognition.face_encodings(get_from_base64(buscar_usuario_por_id(file3.get("usuario"))))
    comparacion = face_recognition.face_distance(np.array([face_encodings_local[0]]), np.array([json_image[0]]))
    if (comparacion.tolist()[0]<0.6):
        return file3 
    else:
        print('No entro papu')

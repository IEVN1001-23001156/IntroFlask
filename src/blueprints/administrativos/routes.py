from flask import Blueprint, jsonify, request
from database import mysql

administrativos_bp = Blueprint(
    'administrativos',
    __name__,
    url_prefix='/api/administrativos'
)

def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))

def leer_admin_bd(numempleado):
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM administrativos WHERE numempleado = {0}".format(numempleado)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            admin = {
                "numempleado": datos[0], 
                "nombre": datos[1],
                "apellidos": datos[2], 
                "telefono": datos[3], 
                "correo": datos[4],  
                "departamento": datos[5]
            }
            return admin
        else:
            return None 
    except Exception as ex:
        raise ex

@administrativos_bp.route('/', methods=['GET'])
def lista_admins():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT numempleado, nombre, apellidos, telefono, correo, departamento
            FROM administrativos
        """)
        datos = cursor.fetchall()
        admins = [
            fila_a_diccionario(cursor, fila)
            for fila in datos
        ]
        return jsonify({
            'admins': admins,
            'mensaje': 'Lista de administrativos',
            'exito': True
        }), 200

    except Exception as ex:
        return jsonify({
            'mensaje': 'Error al consultar los administrativos',
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()
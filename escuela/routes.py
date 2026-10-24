from flask import Blueprint, jsonify, request
from database import mysql

maestros_bp = Blueprint(
    'maestros',
    __name__,
    url_prefix='/api/maestros'
)

def fila_a_diccionario(cursor, fila):
    columnas=[columna[0] for columna in cursor.description]
    return dict(zip(columnas,fila))

@maestros_bp.route("/maestros", methods=['GET'])
def listar_maestros():
    cursor=None
    
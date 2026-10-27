from flask import Blueprint, jsonify, request
from database import mysql

alumnos_bp = Blueprint(
    'alumnos',
    __name__,
    url_prefix='/api/alumnos'
)

def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))

def leer_alumno_bd(matricula):
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM alumnos WHERE matricula = {0}".format(matricula)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            alumno = {
                "matricula": datos[0], 
                "nombre": datos[1],
                "apaterno": datos[2], 
                "amaterno": datos[3], 
                "correo": datos[4]
            }
            return alumno
        else:
            return None 
    except Exception as ex:
        raise ex

# Consultar todo
@alumnos_bp.route('/', methods=['GET'])
def lista_alumnos():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT matricula, nombre, apaterno, amaterno, correo
            FROM alumnos
        """)
        datos = cursor.fetchall()
        alumnos = [
            fila_a_diccionario(cursor, fila)
            for fila in datos
        ]
        return jsonify({
            'alumnos': alumnos,
            'mensaje': 'Lista de alumnos',
            'exito': True
        }), 200

    except Exception:
        return jsonify({
            'mensaje': 'Error al consultar los alumnos',
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

# Consultar  
@alumnos_bp.route('/<mat>', methods=['GET'])
def leer_alumno(mat):
    try: 
        alumno = leer_alumno_bd(mat)
        if alumno != None:
            return jsonify({
                'alumno': alumno,
                'mensaje': 'Alumno encontrado', 
                'exito': True
            })
        else:
            return jsonify({
                'alumno': alumno, 
                'mensaje': 'Alumno no encontrado', 
                'exito': False
            })
    except Exception as ex:
        return jsonify({
            'message': "error {}".format(ex),
            'exito': False
        })

# Registrar 
@alumnos_bp.route('/', methods=['POST'])
def registrar_alumno():
    try:
        alumno = leer_alumno_bd(request.json['matricula'])
        if alumno != None:
            return jsonify({
                'mensaje': 'Alumno ya existente, no se puede registrar', 
                'exito': False
            })
        else:
            cursor = mysql.connection.cursor()
            sql = """INSERT INTO alumnos (matricula, nombre, apaterno, amaterno, correo) 
                     VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')""".format(
                request.json['matricula'],
                request.json['nombre'], 
                request.json['apaterno'],
                request.json['amaterno'], 
                request.json['correo']
            )
            cursor.execute(sql)
            mysql.connection.commit()
            return jsonify({
                'mensaje': "Alumno registrado", 
                'exito': True
            })

    except Exception as ex:
        return jsonify({
            'message': "error {}".format(ex), 
            'exito': False
        })

# Actualizar 
@alumnos_bp.route('/<mat>', methods=['PUT'])
def actualizar_alumno(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if alumno != None:
            cursor = mysql.connection.cursor()
            sql = """UPDATE alumnos SET nombre = '{0}',
            apaterno = '{1}', amaterno = '{2}', correo = '{3}'
            WHERE matricula = {4}""".format(
                request.json['nombre'],
                request.json['apaterno'], 
                request.json['amaterno'],
                request.json['correo'], 
                mat
            )
            cursor.execute(sql)
            mysql.connection.commit() 
            return jsonify({
                'mensaje': "Alumno actualizado.",
                'exito': True
            })
        else:
            return jsonify({
                'mensaje': "Alumno no encontrado.",
                'exito': False
            })
    except Exception as ex:
        return jsonify({
            'message': "error {}".format(ex), 
            'exito': False
        })

# Eliminar 
@alumnos_bp.route('/<mat>', methods=['DELETE'])
def eliminar_alumno(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if alumno != None:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM alumnos WHERE matricula = {0}".format(mat)
            cursor.execute(sql)
            mysql.connection.commit()
            return jsonify({'mensaje': "Alumno eliminado", 'exito': True})
        else:
            return jsonify({'mensaje': "Alumno no encontrado", 'exito': False})

    except Exception as ex:
        return jsonify({
            'message': "error {}".format(ex), 
            'exito': False
        })
from flask import Flask, redirect, url_for, request, render_template, jsonify, json
from flask_mysqldb import MySQL
from requests import post
from sympy import hn1

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'us-cdbr-east-06.cleardb.net'
app.config['MYSQL_USER'] = 'bbd292aa23aeaf'
app.config['MYSQL_PASSWORD'] = 'ece55924'
app.config['MySQL_DB'] = 'heroku_978ea61906c2949'

mysql = MySQL(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

#mostrar los datos de la tabla vehiculo
@app.route('/stock', methods=['GET'])
def get_vehiculo():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('select Id_vehiculo, Nombre, Modelo, Cantidad from heroku_978ea61906c2949.vehiculos')
        datos = cursor.fetchall()
        vehiculos = []
        for fila in datos:
            dato = {'Id_vehiculo': fila[0], 'Nombre': fila[1], 'Modelo': fila[2], 'Cantidad': fila[3]}
            vehiculos.append(dato)
        return jsonify({'vehiculos': vehiculos, 'message': 'ok'})
    except Exception as e:
        return jsonify({'message': 'error'})   
#leer los vehiculos por el Id_vehiculo
@app.route('/stock/<codigo>', methods=['GET'])
def get_vehiculo_id(codigo):
    try:
        cursor = mysql.connection.cursor()
        sql = "select Id_vehiculo, Nombre, Modelo, Cantidad from heroku_978ea61906c2949.vehiculos where Id_vehiculo = '{0}' ".format(codigo)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            vehiculo = {'Id_vehiculo': datos[0], 'Nombre': datos[1], 'Modelo': datos[2], 'Cantidad': datos[3]}
            return jsonify({'vehiculo': vehiculo, 'message': 'ok'})
        else:
            return jsonify({'message': 'error1'})
    except Exception as e:
        return jsonify({'message': 'error'})
#registrar un vehiculo
@app.route('/stock', methods=['POST'])
def post_vehiculo():
    #print(request.json)
    try:
        cursor = mysql.connection.cursor()
        sql = """INSERT INTO heroku_978ea61906c2949.vehiculos(Nombre , Modelo , Tipo , Caracteristica, Cantidad) 
        VALUES ('{0}','{1}','{2}','{3}',{4})""".format(request.json['Nombre'], request.json['Modelo'], request.json['Tipo'], request.json['Caracteristica'], request.json['Cantidad'])
        cursor.execute(sql)
        mysql.connection.commit()#guardar los cambios
        return jsonify({'message': 'vehiculo añadido'})
    except Exception as e:
        return jsonify({'message': 'error'})
#actualizar vehiculo
@app.route('/stock/<codigo>', methods=['PUT'])
def put_vehiculo(codigo):
    try:
        cursor = mysql.connection.cursor()
        sql = """UPDATE heroku_978ea61906c2949.vehiculos SET Nombre = '{0}', Modelo = '{1}', Tipo = '{2}', Caracteristica = '{3}', Cantidad = {4} WHERE Id_vehiculo = '{5}' """.format(request.json['Nombre'], request.json['Modelo'], request.json['Tipo'], request.json['Caracteristica'], request.json['Cantidad'], codigo)
        cursor.execute(sql)
        mysql.connection.commit()
        return jsonify({'message': 'vehiculo actualizado'})
    except Exception as e:
        return jsonify({'message': 'error'})
  
#eliminar un vehiculo
@app.route('/stock/<codigo>',methods=['DELETE'])
def delete_vehiculo(codigo):
    try:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM heroku_978ea61906c2949.vehiculos Where Id_vehiculo = {0}  ".format(codigo)
        cursor.execute(sql)
        mysql.connection.commit()#guardar los cambios
        return jsonify({'message': 'vehiculo borrado'})
    except Exception as e:
        return jsonify({'message': 'error'})  
def pagina_no_encotrada(error):
    return "<h1>esta pagina no ha sido encontrada </h1>", 404     

if __name__ == '__main__':
    app.run(debug=True, port=5000)
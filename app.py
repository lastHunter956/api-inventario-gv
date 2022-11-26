from flask import Flask, request, jsonify #importar librerias
from flask_mysqldb import MySQL #configuracion de la base de datos
from requests import post #configuracion de la base de datos

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'us-cdbr-east-06.cleardb.net'#configuracion de la base de datos host
app.config['MYSQL_USER'] = 'bbd292aa23aeaf'#configuracion de la base de datos usuario
app.config['MYSQL_PASSWORD'] = 'ece55924'#configuracion de la base de datos contraseña
app.config['MySQL_DB'] = 'heroku_978ea61906c2949'#configuracion de la base de datos

mysql = MySQL(app) #se usa para mostrar los datos de la tabla vehiculo

@app.route('/')#ruta de la pagina inicial
def hello_world():#funcion de la pagina inicial
    return 'Hello, World!'

#mostrar los datos de la tabla vehiculo
@app.route('/stock', methods=['GET'])#ruta de la pagina mostrar los datos de la tabla vehiculo
def get_vehiculo():#funcion de la pagina mostrar los datos de la tabla vehiculo
    try:#el try es para que si hay un error no se caiga el programa
        cursor = mysql.connection.cursor()#se usa para conectar con la base de datos
        #select vehiculos.Id_vehiculo, vehiculos.Nombre, vehiculos.Modelo, vehiculos.Tipo, vehiculos.Caracteristica, vehiculos.Precio, vehiculos.Descripcion, vehiculos.Imagen from heroku_978ea61906c2949.vehiculos left outer join heroku_978ea61906c2949.ventas v on vehiculos.Id_vehiculo = v.id_vehiculo where v.id_vehiculo is null
        cursor.execute('select vehiculos.Id_vehiculo, vehiculos.Nombre, vehiculos.Modelo, vehiculos.Tipo, vehiculos.Caracteristica, vehiculos.Precio, vehiculos.Descripcion, vehiculos.Imagen from heroku_978ea61906c2949.vehiculos left outer join heroku_978ea61906c2949.ventas v on vehiculos.Id_vehiculo = v.id_vehiculo where v.id_vehiculo is null')
        datos = cursor.fetchall()#el fetchall es para que se muestren todos los datos de la consulta
        vehiculos = []#se crea una lista vacia donde se guardaran los datos de los vehiculos
        for fila in datos:#se crea un ciclo for para que se muestren todos los datos de la consulta
            dato = {'Id_vehiculo': fila[0], 'Nombre': fila[1], 'Modelo': fila[2] , 'Tipo': fila[3], 'Caracteristica': fila[4], 'Precio': fila[5], 'Descripcion': fila[6], 'Imagen': fila[7]}#se crea un diccionario para que se muestren los datos de los vehiculos
            vehiculos.append(dato)#se agrega los datos de los vehiculos a la lista
        return jsonify({'vehiculos': vehiculos, 'message': 'ok'})#se retorna los datos de los vehiculos y un mensaje de ok
    except Exception as e:#el except es para que si hay un error no se caiga el programa
        return jsonify({'message': 'error'})#en caso de que haya un error se retorna un mensaje de error   
#leer los vehiculos por el Id_vehiculo
@app.route('/stock/<codigo>', methods=['GET'])
def get_vehiculo_id(codigo):#funcion de la pagina leer los vehiculos por el Id_vehiculo
    try:#el try es para que si hay un error no se caiga el programa
        cursor = mysql.connection.cursor()#se usa para conectar con la base de datos
        sql = "select Id_vehiculo, Nombre, Modelo, Precio, Caracteristica, Tipo, Descripcion, Imagen from heroku_978ea61906c2949.vehiculos where Id_vehiculo = '{0}' ".format(codigo)
        cursor.execute(sql)#se ejecuta la consulta
        datos = cursor.fetchone()#el fetchone es para que se muestren solo los datos de la consulta
        if datos != None: #en caso de que el codigo no exista
            vehiculo = {'Id_vehiculo': datos[0], 'Nombre': datos[1], 'Modelo': datos[2], 'Precio': datos[3], 'Caracteristica': datos[4], 'Tipo': datos[5], 'Descripcion': datos[6], 'Imagen': datos[7]}
            return jsonify({'vehiculo': vehiculo, 'message': 'ok'})#se retorna los datos del vehiculo y un mensaje de ok
        else:#en caso de que no se encuentre el vehiculo se retorna un mensaje de error
            return jsonify({'message': 'error1'})#en caso de que haya un error se retorna un mensaje de error
    except Exception as e:#el except es para que si hay un error no se caiga el programa
        return jsonify({'message': 'error'})#en caso de que haya un error se retorna un mensaje de error
#registrar un vehiculo
@app.route('/stock', methods=['POST'])
def post_vehiculo():#funcion de la pagina registrar un vehiculo
    try:# el try es para que si hay un error no se caiga el programa
        cursor = mysql.connection.cursor()#se usa para conectar con la base de datos
        sql = """INSERT INTO heroku_978ea61906c2949.vehiculos(Nombre , Modelo , Tipo , Caracteristica, Precio, Descripcion, Imagen) 
        VALUES ('{0}','{1}','{2}','{3}',{4},'{5}','{6}')""".format(request.json['Nombre'], request.json['Modelo'], request.json['Tipo'], request.json['Caracteristica'], request.json['Precio'], request.json['Descripcion'], request.json['Imagen'])
        cursor.execute(sql)#se ejecuta la consulta
        mysql.connection.commit()#guardar los cambios
        return jsonify({'message': 'vehiculo añadido'})#se retorna un mensaje de vehiculo añadido
    except Exception as e:#el except es para que si hay un error no se caiga el programa
        return jsonify({'message': 'error'})#en caso de que haya un error se retorna un mensaje de error
#actualizar vehiculo
@app.route('/stock/<codigo>', methods=['PUT'])
def put_vehiculo(codigo):
    try:#el try es para que si hay un error no se caiga el programa
        int(codigo)#se convierte el codigo a entero
        cursor = mysql.connection.cursor()#se usa para conectar con la base de datos
        sql = """UPDATE heroku_978ea61906c2949.vehiculos SET Nombre = '{0}', Modelo = '{1}', Tipo = '{2}', Caracteristica = '{3}', Precio = {4} , Descripcion = '{6}', Imagen = '{7}' WHERE Id_vehiculo = '{5}' """.format(request.json['Nombre'], request.json['Modelo'], request.json['Tipo'], request.json['Caracteristica'], request.json['Precio'], codigo, request.json['Descripcion '], request.json['Imagen'])
        cursor.execute(sql)#se ejecuta la consulta
        mysql.connection.commit()#guardar los cambios
        return jsonify({'message': 'vehiculo actualizado'})#se retorna un mensaje de vehiculo actualizado
    except Exception as e:#el except es para que si hay un error no se caiga el programa
        return jsonify({'message': 'error'})#en caso de que haya un error se retorna un mensaje de error
  
#eliminar un vehiculo
@app.route('/stock/<codigo>',methods=['DELETE'])
def delete_vehiculo(codigo):#funcion de la pagina eliminar un vehiculo
    try:#el try es para que si hay un error no se caiga el programa
        int(codigo)#se convierte el codigo a entero
        cursor = mysql.connection.cursor()# el cursor es para conectar con la base de datos
        sql = "DELETE FROM heroku_978ea61906c2949.vehiculos Where Id_vehiculo = {0}  ".format(codigo)#se crea la consulta
        cursor.execute(sql)#se ejecuta la consulta
        mysql.connection.commit()#guardar los cambios
        return jsonify({'message': 'vehiculo borrado'})#se retorna un mensaje de vehiculo borrado
    except Exception as e:#el except es para que si hay un error no se caiga el programa
        return jsonify({'message': 'error'})  #en caso de que haya un error se retorna un mensaje de error
    
def pagina_no_encotrada(error):#funcion de la pagina no encontrada
    return "<h1>esta pagina no ha sido encontrada </h1>", 404  #se retorna un mensaje de pagina no encontrada   

if __name__ == '__main__':#se ejecuta el programa
    app.register_error_handler(404, pagina_no_encotrada)
    app.run(debug=True, port=5000)#se ejecuta el programa en el puerto 5000 y en modo debug
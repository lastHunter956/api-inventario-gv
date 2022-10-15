cursor = conexion.connection.cursor()
        sql = """INSERT INTO heroku_978ea61906c2949.vehiculos (Nombre , Modelo , Tipo , Caracteristica, Cantidad) 
        VALUES ('{0}','{1}','{2}','{3}', {4} )""".format(request.json['Nombre'], 
                                                         request.json['Modelo'], request.json['Tipo'], request.json['Caracteristica'], request.json['Cantidad'])
        cursor.execute(sql)
        conexion.connection.commit()#guardar los cambios
        return jsonify({'message': 'vehiculo registrado'})
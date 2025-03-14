from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_pymongo import PyMongo
import os 
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')


db = MySQL(app)
mongo = PyMongo(app)


@app.route('/addUserMYSQL', methods=['POST'])
def addUserMYSQL():
    nombre = request.json.get('nombre')
    pais = request.json.get('pais')
    ciudad = request.json.get('ciudad')
    cp = request.json.get('cp')


    cur = db.connection.cursor()
    sql = 'INSERT INTO usuarios (nombre,pais,ciudad,cp) VALUES(%s,%s,%s,%s)'
    values = (nombre,pais,ciudad,cp)
    cur.execute(sql,values)
    db.connection.commit()
    return jsonify({'message':'USUARIO AÑADIDO CORRRECTAMENTE'})

@app.route('/getUsersMYSQL', methods=['GET'])
def getUsersMYSQL():

    cur = db.connection.cursor()
    sql = 'SELECT * FROM usuarios'
    cur.execute(sql,)
    users= cur.fetchall()
    return jsonify({'usuarios':users})


@app.route('/editUserMYSQL', methods=['PUT'])
def editUserMYSQL():
    nombre = request.json.get('nombre')
    pais = request.json.get('pais')
    ciudad = request.json.get('ciudad')
    cp = request.json.get('cp')


    cur = db.connection.cursor()
    sql = 'UPDATE usuarios SET pais=%s, ciudad=%s, cp=%s WHERE nombre =%s'
    values = (pais,ciudad,cp,nombre)
    cur.execute(sql,values)
    db.connection.commit()
    return jsonify({'message':'USUARIO EDITADO CORRRECTAMENTE'})

@app.route('/deleteUserMYSQL', methods=['DELETE'])
def deleteUserMYSQL():
    nombre = request.json.get('nombre')

    cur = db.connection.cursor()
    sql = 'DELETE FROM usuarios WHERE nombre =%s'
    cur.execute(sql,(nombre,))
    db.connection.commit()
    return jsonify({'message':'USUARIO ELIMINADO CORRRECTAMENTE'})



#MONGO


@app.route('/addUserMONGO',methods=['POST'])
def addUserMONGO():

    mongo.db.tableuser.insert_one(request.get_json())
    return jsonify({'message':'USUARIO AÑADIDO CORRECTAMENTE'})


@app.route('/getUsersMONGO',methods=['GET'])
def getUsersMONGO():

    users = mongo.db.tableuser.find()
    return jsonify({'message':users})


@app.route('/editUserMONGO',methods=['PUT'])
def editUserMONGO():
    data = request.get_json()
    mongo.db.tableuser.update_one({"nombre":data["nombre"]},{"$set":data})
    return jsonify({'message':'USUARIO ACTUALIZADO'})


@app.route('/deleteUserMONGO',methods=['DELETE'])
def deleteUserMONGO():
    data = request.get_json()
    mongo.db.tableuser.delete_one({"nombre":data["nombre"]})
    return jsonify({'message':'USUARIO ELIMINADO CORRECTAMENTE'})





if __name__ == '__main__':
    app.run(debug=True, port=2000)
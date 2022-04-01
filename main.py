import pymysql
from File1 import app
from File2 import mysql
from flask import jsonify
from flask import flash, request

@app.route("/")
def demo():
     return jsonify("MYSQL_DATABASE CONNECTED SUCCESSFULLY")


@app.route('/datas')
def get():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, fname, email FROM info")
        rows = cursor.fetchall()
        respone = jsonify(rows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/datas/<int:id>')
def id(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, fname, email FROM info WHERE id =%s",id)
        rows= cursor.fetchone()
        respone = jsonify(rows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/datas', methods=['POST'])
def add():
    try:
        json1 = request.json
        fname1 = json1['fname']
        email1 = json1['email']

        if fname1 and email1 and request.method == 'POST':
          sql = "INSERT INTO info(fname, email) VALUES(%s, %s)"
          user = (fname1, email1)
          conn = mysql.connect()
          cursor = conn.cursor()
          cursor.execute(sql,user)
          conn.commit()
          respone = jsonify('added successfully!')
          respone.status_code = 201
          return respone

        else:
          return 'not_found()'

    except Exception as e:
           print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/datas',methods=['PUT'])
def update():
    try:
        json1 = request.json
        id1 = json1['id']
        fname1 = json1['fname']
        email1 = json1['email']
        if fname1 and email1 and id1 and request.method == 'PUT':
            sql= "UPDATE info SET fname=%s, email=%s WHERE id=%s"
            user = (fname1, email1, id1)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql,user)
            conn.commit()
            respone = jsonify('updated successfully!')
            respone.status_code = 201
            return respone
        else:
            return 'not_found()'
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/datas/<int:id>', methods=['DELETE'])
def delete(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM info WHERE id =%s", (id,))
        conn.commit()
        respone = jsonify('deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(debug=True,port=5004)

    """@app.errorhandler(404)
    def not_found(error=None):
        message = {
            'status': 404,
            'message': 'Record not found: ' + request.url,
        }
        respone = jsonify(message)
        respone.status_code = 404
        return respone"""





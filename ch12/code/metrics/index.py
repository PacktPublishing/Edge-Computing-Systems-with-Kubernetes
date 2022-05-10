from flask import Flask, request
import mysql.connector
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'It works'

def insert(data):
    conn = mysql.connector.connect(
     host=os.environ['HOST'],
     user=os.environ['MYSQL_USER'],
     password=os.environ['MYSQL_PASSWORD'],
     database=os.environ['MYSQL_DATABASE']
    )

    cursor = conn.cursor()
    sql = "INSERT INTO metric "+\
          "(device,temperature_c,temperature_f,humidity,time) "+\
          "VALUES (%s,%s,%s,%s,now());"
    val = (data["d"],data["t"],data["t_f"],data["h"])
    cursor.execute(sql,val)
    conn.commit()

    cursor.close()
    conn.close()


@app.route('/device',methods = ['POST'])
def device():
    data = request.json
    print(data)

    #Process data in some way
    t_farenheit = float(data["t"])*(9/5)+32
    data["t_f"] = t_farenheit
    insert(data)

    return "processed"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)

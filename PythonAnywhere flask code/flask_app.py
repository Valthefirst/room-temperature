# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import request
from flask import jsonify

import mysql.connector

app = Flask(__name__)

@app.route('/', methods=["GET"])
def default_response():
    mydb = mysql.connector.connect(host="valthefirst.mysql.pythonanywhere-services.com", user="valthefirst", password="raspberrypi", database="valthefirst$iot2-project")
    my_cursor = mydb.cursor()
    my_cursor.execute("SELECT * FROM temp;")
    data = my_cursor.fetchall()
    my_cursor.close()
    mydb.close()
    # for x in data:
    #    return print(x)
    #return "done"
    return jsonify(data)


@app.route('/new', methods = ["POST"])
def new_record():
    content = request.get_json()

    date_time = content.get("date_time")
    temperature = content.get("temperature")
    humidity = content.get("humidity")
    temperature_unit = content.get("temperature_unit")

    # date_time = request.form.get("date_time")
    # temperature = request.form.get("temperature")
    # humidity = request.form.get("humidity")
    # temperature_unit = request.form.get("temperature_unit")

    if date_time is None or temperature is None or humidity is None or temperature_unit is None:
        return "MISSING A VALUE"
    else:
        mydb = mysql.connector.connect(host="valthefirst.mysql.pythonanywhere-services.com", user="valthefirst", password="raspberrypi", database="valthefirst$iot2-project")
        my_cursor = mydb.cursor()
        add_values = ("insert into temp (date_time, temperature, humidity, temperature_unit) values (%s, %s, %s, %s)")
        data_name = (date_time, temperature, humidity, temperature_unit)
        my_cursor.execute(add_values, data_name)
        mydb.commit()
        my_cursor.close()
        mydb.close()
        return "done for " + date_time




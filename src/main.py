#!/usr/bin/python

import bme280
import mh_z19
import smbus2
import time
import board
import adafruit_dht
import mysql.connector

sensorTH = 'dht11'

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="user_cli",
  passwd="pass",
  database='product',
    port = "3306"
)
mycursor = mydb.cursor()

temp = 0
humidity = 0
co_2 = 0
year = 0
month = 0
day = 0

sql_insert = "INSERT INTO sensors_data (temperature, humidity, co2) VALUES (%s, %s, %s)"
sql_avg = f"SELECT avg(temperature), avg(humidity), avg(co2) FROM sensors_data where date_format(insertion_date,'%Y-%m-%d') = date '{year}-{month}-{day}'"

def avg_val(y, m, d):
    if y.isdigit() and len(y) == 4 and m.isdigit() and len(m) <= 2 and d.isdigit() and len(d) <= 2:
        try:
            year = int(y)
            month = int(m)
            day = int(d)
            mycursor.execute(sql_avg)
            result = mycursor.fetchall()
            if result[0][0] == None and result[0][1] == None and result[0][2] == None:
                print("No values for that day")
            else:
                print(f"Average temperature: {round(result[0][0], 2)}, Average humidity: {round(result[0][1], 1)}, Average co2: {round(result[0][2], 0)}")
        except Exception as error:
            print(f"Incorrect date: {error}")
    else:
        print("Incorrect input format")

def upd_values():
    mycursor.execute("SELECT temperature, humidity, co2 FROM sensors_data where id = (select max(id) from sensors_data)")
    myresult = mycursor.fetchall()
    temp = round(float(myresult[0][0]),2)
    humidity = int(myresult[0][1])
    co_2 = int(myresult[0][2])
    print("Last inserted value")
    print("Temperature: {}*C   Humidity: {}%  CO2: {}ppm".format(temp, humidity, co_2))

if sensorTH == 'dht11':
    sensor = adafruit_dht.DHT11(board.D23) #GPIO 27
else:
    port = 1
    address = 0x76 #GPIO 3
    bus = smbus2.SMBus(port)
    calibration_params = bme280.load_calibration_params(bus, address)
    data = bme280.sample(bus, address, calibration_params)

while True:
    try:
        co2 = mh_z19.read()
        co_2 = co2['co2']
        if sensorTH == 'dht11':
            temp = sensor.temperature
            humidity = sensor.humidity
        else:
            temp = data.temperature
            humidity = data.humidity
        val = (temp, humidity, co2['co2'])
        mycursor.execute(sql_insert, val)
        print("Temperature: {}*C   Humidity: {}%    CO2: {}ppm".format(temp, humidity, co_2))
        mydb.commit()
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(10.0)
        continue
    except Exception as error:
        raise error
    time.sleep(10.0)
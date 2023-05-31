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

sql_insert = "INSERT INTO sensors_data (temperature, humidity, co2) VALUES (%s, %s, %s)"

def upd_values(myresult):
    temp = float(myresult[0][0])
    humidity = float(myresult[0][1])
    co_2 = float(myresult[0][2])
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
        sensor.exit()
        raise error
    time.sleep(10.0)
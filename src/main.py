import bme280
import mh_z19
import smbus2
import time
import board
import adafruit_dht

port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

data = bme280.sample(bus, address, calibration_params)

co2 = mh_z19.read()

while True:
    try:
        temp = sensor.temperature
        humidity = sensor.humidity
        print("Temperature: {}*C   Humidity: {}%    CO2: {}ppm"
                .format(data.temperature, data.humidity, co2['co2']))
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(10.0)
        continue
    except Exception as error:
        sensor.exit()
        raise error
    time.sleep(10.0)
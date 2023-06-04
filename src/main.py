#!/usr/bin/python

import bme280
import mh_z19
import smbus2
import time
import board
import adafruit_dht
import mysql.connector
from tkinter import *
from tkinter import ttk

window = Tk()
window.title("Project")
window.geometry('1280x600')
lbl1 = ttk.Label(window, text="Температура,°C     ", font=("Arial Bold", 32), compound="top")
lbl2 = ttk.Label(window, text="Влажность, %     ", font=("Arial Bold", 32), compound="top")
lbl3 = ttk.Label(window, text="СО2, ppm", font=("Arial Bold", 32), compound="top")
lbl_temp = ttk.Label(window, text=" ", font=("Arial Bold", 12), compound="top")
lbl_temp2 = ttk.Label(window, text=" ", font=("Arial Bold", 12), compound="top")
lbl_temp3 = ttk.Label(window, text=" ", font=("Arial Bold", 12), compound="top")
lbl_temp4 = ttk.Label(window, text=" ", font=("Arial Bold", 12), compound="top")

temp_lbl = ttk.Label(window, text="     ", font=("Arial Bold", 24), foreground="#B71C1C")
humid_lbl = ttk.Label(window, text="     ", font=("Arial Bold", 24), foreground="#0000ff")
co2_lbl = ttk.Label(window, text="     ", font=("Arial Bold", 24), foreground="#00ff00")

temp_avg_lbl = ttk.Label(window, text="     ", font=("Arial Bold", 24), foreground="#B71C1C")
humid_avg_lbl = ttk.Label(window, text="     ", font=("Arial Bold", 24), foreground="#0000ff")
co2_avg_lbl = ttk.Label(window, text="     ", font=("Arial Bold", 24), foreground="#00ff00")

lbl4 = ttk.Label(window, text="Ср. Температура, °C      ", font=("Arial Bold", 32), compound="top")
lbl5 = ttk.Label(window, text="Ср. Влажность, %     ", font=("Arial Bold", 32), compound="top")
lbl6 = ttk.Label(window, text="Ср. СО2, ppm", font=("Arial Bold", 32), compound="top")

combo = ttk.Combobox(window)
combo['values'] = ("dht11", "bme280")
combo.current(0)
combo.grid(column=5, row=0)

year_lbl = ttk.Label(window, text="Год", font=("Arial Bold", 20), compound="top")
month_lbl = ttk.Label(window, text="Месяц", font=("Arial Bold", 20), compound="top")
day_lbl = ttk.Label(window, text="День", font=("Arial Bold", 20), compound="top")

year_txt = Entry(window, width=10)
month_txt = Entry(window, width=10)
day_txt = Entry(window, width=10)

temp_lbl.grid(column=5, row=5)
humid_lbl.grid(column=15, row=5)
co2_lbl.grid(column=25, row=5)

lbl_temp3.grid(column=15, row=8)

lbl1.grid(column=5, row=1)
lbl2.grid(column=15, row=1)
lbl3.grid(column=25, row=1)

year_lbl.grid(column=5, row=20)
month_lbl.grid(column=10, row=20)
day_lbl.grid(column=15, row=20)

lbl_temp2.grid(column=15, row=23)

year_txt.grid(column=5, row=25)
month_txt.grid(column=10, row=25)
day_txt.grid(column=15, row=25)


lbl_temp.grid(column=5, row=15)

lbl_temp4.grid(column=5, row=30)

lbl4.grid(column=5, row=35)
lbl5.grid(column=15, row=35)
lbl6.grid(column=25, row=35)

temp_avg_lbl.grid(column=5, row=40)
humid_avg_lbl.grid(column=15, row=40)
co2_avg_lbl.grid(column=25, row=40)


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
sql_avg = f"""SELECT avg(temperature), avg(humidity), avg(co2) 
              FROM sensors_data 
              WHERE date_format(insertion_date,'%Y-%m-%d') = date '{year}-{month}-{day}'"""

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
                temp_avg_lbl.configure(text=round(result[0][0], 2) + "     ")
                humid_avg_lbl.configure(text=round(result[0][1], 2) + "     ")
                co2_avg_lbl.configure(text=round(result[0][2], 2))
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
    temp_lbl.configure(text=temp + "     ")
    humid_lbl.configure(text=humidity + "     ")
    co2_lbl.configure(text=str(co_2))
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
        sensorTH = combo.get()
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
        temp_lbl.configure(text=temp + "     ")
        humid_lbl.configure(text=humidity + "     ")
        co2_lbl.configure(text=str(co_2))
        print("Temperature: {}*C   Humidity: {}%    CO2: {}ppm".format(temp, humidity, co_2))
        mydb.commit()
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(10.0)
        continue
    except Exception as error:
        raise error
    time.sleep(10.0)

btn = Button(window, text="""
Ср. арифметическое данных за день
""", command=avg_val)
btn['activebackground'] = '#555555'
btn['fg'] = '#000000'
btn['bg'] = '#5783db'
btn.grid(column=5, row=10)

btn2 = Button(window, text="""
    Обновить значения     
""", command=upd_values)
btn2['activebackground'] = '#555555'
btn2['fg'] = '#000000'
btn2['bg'] = '#C3372C'
btn2.grid(column=15, row=10)

window.mainloop()
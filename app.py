# -*- coding: utf-8 -*-
from flask import Flask, render_template
import cv2
import numpy
import csv
import glob
import  math
from collections import Counter
from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
import time
import os

print("Programma sāk darbu")

# _________________________________
# Nolasa datus
TirsVert = []
NeTirsVert = []

with open('dati.csv', 'r') as file:
    csv_reader = csv.reader(file, delimiter=',')

    for row in csv_reader:
        TirsVert.append([float(row[0]),float(row[1]),float(row[2])])
        NeTirsVert.append([float(row[3]),float(row[4]),float(row[5])])


def Most_Common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]

# Saņemt tīrību?!?
def TirVert():

    camera = PiCamera()
    camera.resolution = (640, 360)
    rawCapture = PiRGBArray(camera)
    # allow the camera to warmup
    time.sleep(0.1)
    # grab an image from the camera
    camera.capture(rawCapture, format="bgr")
    myimg = rawCapture.array
    # display the image on screen and wait for a keypress
   

    MinVert = [10**5,10**5,10**5,10**5,10**5]
    MinVertPied = ["","","","",""]
    avg_color_per_row = numpy.average(myimg, axis=0)
    avg_color = numpy.average(avg_color_per_row, axis=0)
    print(avg_color)
    for i in TirsVert:
        
        norma = math.sqrt( (i[0]-avg_color[0])**2 + (i[1]-avg_color[1])**2 + (i[2]-avg_color[2])**2 )
        if max(MinVert) > norma:
            indeks = MinVert.index(max(MinVert))
            MinVert[indeks] = norma
            MinVertPied[indeks] = "tirs"

    for i in NeTirsVert:
        norma = math.sqrt( (i[0]-avg_color[0])**2 + (i[1]-avg_color[1])**2 + (i[2]-avg_color[2])**2 )
        if max(MinVert) > norma:
            indeks = MinVert.index(max(MinVert))
            MinVert[indeks] = norma
            MinVertPied[indeks] = "netirs"
    cv2.waitKey(0)
    camera.close()

    return Most_Common(MinVertPied)

print("Aplikācijas sāk darbu")

app = Flask(__name__)


@app.route('/')
def home():
    print(TirVert())
    return render_template('sakums.html')


@app.route('/assistent')
def assistent():
    return render_template('Assistent.html')

@app.route('/history')
def history():
    return render_template('History.html')
@app.route('/settings')
def settings():
    return render_template('Settings.html')

@app.route('/info')
def info():
    return render_template('Info.html')


if __name__ == '__main__':
    print(123)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    print("Programma beidz darbu")

 
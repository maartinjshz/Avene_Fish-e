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

camera = PiCamera()
camera.resolution = (640, 360)

# _________________________________
# Nolasa datus
global TirsVert, NeTirsVert, VidVrtTirs, NeVidVrtTirs
TirsVert = []
NeTirsVert = []
VidVrtTirs = [0,0,0]
VidVrtNeTirs = [0,0,0]
with open('dati.csv', 'r') as file:
    csv_reader = csv.reader(file, delimiter=',')

    for row in csv_reader:
        TirsVert.append([float(row[0]),float(row[1]),float(row[2])])
        NeTirsVert.append([float(row[3]),float(row[4]),float(row[5])])
    


    
def Vid_vertiba_makoniem(TirsVert,NeTirsVert):
    n = len(NeTirsVert)
    for i in range(0,n):
        VidVrtTirs[0] =   VidVrtTirs[0] + TirsVert[i][0]
        VidVrtTirs[1] =   VidVrtTirs[1] + TirsVert[i][1]
        VidVrtTirs[2] =   VidVrtTirs[2] + TirsVert[i][2]


        VidVrtNeTirs[0] =   VidVrtNeTirs[0] + NeTirsVert[i][0]
        VidVrtNeTirs[1] =   VidVrtNeTirs[1] + NeTirsVert[i][1]
        VidVrtNeTirs[2] =   VidVrtNeTirs[2] + NeTirsVert[i][2]

    VidVrtTirs[1] = VidVrtTirs[1] / n
    VidVrtTirs[2] = VidVrtTirs[2] / n
    VidVrtTirs[0] = VidVrtTirs[0] / n
    
    VidVrtNeTirs[0] = VidVrtNeTirs[0] / n
    VidVrtNeTirs[1] = VidVrtNeTirs[1] / n
    VidVrtNeTirs[2] = VidVrtNeTirs[2] / n

    

    return [VidVrtTirs, VidVrtNeTirs]


    

def Most_Common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]


def procenti(punkts,VidVrtTirs, VidVrtNeTirs):
    VidTirsNorma = math.sqrt(  (punkts[0]-VidVrtTirs[0])**2 + (punkts[2]-VidVrtTirs[2])**2  + (punkts[1]-VidVrtTirs[1])**2 )
    VidNeTirsNorma = math.sqrt(  (punkts[0]-VidVrtNeTirs[0])**2 + (punkts[2]-VidVrtNeTirs[2])**2  + (punkts[1]-VidVrtNeTirs[1])**2 )

    Attalums = VidNeTirsNorma +  VidTirsNorma 
    return  round(VidTirsNorma/  Attalums * 100 , 3)

# Saņemt tīrību?!?
def TirVert():

    
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

    Prcneti_Tiriba = procenti(avg_color ,VidVrtTirs, VidVrtNeTirs)
    print("Tīrības procenti")
    print(Prcneti_Tiriba)
    print("Tīrība:")
    Biezakais = Most_Common(MinVertPied)
    print(Biezakais)
    cv2.waitKey(1)

    print("Apprēķini ir veikti")
    return Biezakais

print("Aplikācijas sāk darbu")

VidVrtTirs, VidVrtNeTirst=Vid_vertiba_makoniem(TirsVert,NeTirsVert)

app = Flask(__name__)


@app.route('/')
def home():
    TirVert()
    return render_template('sakums.html')


@app.route('/assistent')
def assistent():
    return render_template('Assistent.html')

# off - neiet
@app.route('/history')
def history():
    return render_template('History.html')

    # Tas ir ejošs
@app.route('/settings')
def settings():
    return render_template('Settings.html')

# 
@app.route('/info')
def info():
    return render_template('Info.html')


if __name__ == '__main__':
    print(123)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    print("Programma beidz darbu")

 
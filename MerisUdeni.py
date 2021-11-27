import cv2
import numpy
import csv
import glob
import  math
from collections import Counter
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

TirsVert = []
NeTirsVert = []

MinVert = [10**5,10**5,10**5]
MinVertPied = ["","",""]


camera = PiCamera()
rawCapture = PiRGBArray(camera)
time.sleep(0.1)

with open('dati.csv', 'r') as file:
    csv_reader = csv.reader(file, delimiter=',')

    for row in csv_reader:
        TirsVert.append([float(row[0]),float(row[1]),float(row[2])])
        NeTirsVert.append([float(row[3]),float(row[4]),float(row[5])])


def Most_Common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]

# Paņem sample attēla vidējo vērtību, lai salīdzinatu
while True:
    

    camera.capture(rawCapture, format="bgr", size = (640,360))
    myimg = rawCapture.array

    avg_color_per_row = numpy.average(myimg, axis=0)
    avg_color = numpy.average(avg_color_per_row, axis=0)

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
    time.sleep(50)
    print(Most_Common(MinVertPied))

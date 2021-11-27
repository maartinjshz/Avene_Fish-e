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


cap = cv2.VideoCapture(0)
fps = cap.get(cv2.CAP_PROP_POS_FRAMES)


camera = PiCamera()
camera.resolution = (640, 360)
rawCapture = PiRGBArray(camera, size=(640, 360))
time.sleep(0.1)

with open('dati.csv', 'r') as file:
    csv_reader = csv.reader(file, delimiter=',')

    for row in csv_reader:
        TirsVert.append([float(row[0]),float(row[1]),float(row[2])])
        NeTirsVert.append([float(row[3]),float(row[4]),float(row[5])])


def Most_Common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]

# APŗēķina pašreizējo ūdens stāvokli
def Kamera(myimg):
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
    return Most_Common(MinVertPied)


# Paņem sample attēla vidējo vērtību, lai salīdzinatu
while cap.isOpened():
    
   
    frame = cap.read()
    #camera.capture(rawCapture, format="bgr")
    #myimg = rawCapture.array
    myimg = frame
    Stavoklis = Kamera(myimg)
    print(Stavoklis)
    cv2.imshow("orginal with line", myimg)	
    
    
    rawCapture.truncate(0)
    cf = cap.get(cv2.CAP_PROP_POS_FRAMES) - 1
    cap.set(cv2.CAP_PROP_POS_FRAMES, cf+50)
    # cv2.setTrackbarPos("pos_trackbar", "Frame Grabber", 
    int(cap.get(cv2.CAP_PROP_FPS))
    time.sleep(2)
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break
  

cap.release()
cv2.destroyAllWindows()
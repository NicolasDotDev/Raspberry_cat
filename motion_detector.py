import cv2
import numpy as np
from datetime import datetime, time

CONTOUR_THRESHOLD = 3000

def in_between(now, start, end):
    if start <= end:
        return start <= now < end
    else: # over midnight e.g., 23:30-04:15
        return start <= now or now < end
    
def isContoursEnough(contours) :
    for contour in contours:
        if cv2.contourArea(contour) > CONTOUR_THRESHOLD:
            return True
    return False

cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('OPENCVmotiondetection.avi')
i= 0
ret, frame1 = cap.read()
ret, frame2 = cap.read()
last_ten_countours = []
start = None
mouvement = None
log_name = datetime.now().strftime("%m_%d_%Y_%Hh%Mm%Ss") + ".txt"
print(log_name)
file = open(log_name, "x")
#file = open("monFichier", "x")


print(file.__getattribute__)


while cap.isOpened():
    i += 1
    #print("i= " + str(i))
    #print("isRecording : " + str(mouvement))
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(last_ten_countours) < 10 :
        last_ten_countours.append(len(contours))
        continue
    #print(last_ten_countours)

    if last_ten_countours.count(0) < 4 :
        size = (int(cap.get(3)), int(cap.get(4)))

        if start == None or mouvement == False :
            print("CREATE VIDEO RECORDER")
            vid = cv2.VideoWriter( datetime.now().strftime("%m_%d_%Y_%Hh%Mm%Ss" + "_"+str(i)+".avi"), cv2.VideoWriter_fourcc(*'MJPG'), 10, size)
            start = datetime.now()
            print("Start at : " + start.strftime("%m/%d/%Y, %H:%M:%S"))
            file.write("Start at : " + start.strftime("%m/%d/%Y, %H:%M:%S")+"\n")
            
            vid.write(frame1)
        mouvement = True
        vid.write(frame1)
        #print ("MOUVEMENT")    
    else :
        if mouvement == True :
            print("end at : " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            file.write("End at : " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") +"\n\n -----------------------------------\n\n" )
            print("CLOSE VIDEO RECORDER")
            vid.release()
            start = None
        mouvement = False
        #print ("NONONONONONONONO MOUVEMENT")
    last_ten_countours.insert(0, len(contours))
    last_ten_countours.pop()
    
    #print(len(contours))
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < CONTOUR_THRESHOLD:
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()
    #print("night" if in_between(datetime.now().time(), time(16), time(17)) else "day")
    if cv2.waitKey(40) == 27 or not in_between(datetime.now().time(), time(16), time(17)):
        print("out of time")
        break





cap.release()
file.close()
if vid :
    vid.release()

cv2.destroyAllWindows()

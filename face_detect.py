import os
import cv2
import glob
import time

name = "pic"

cascPath = "haarcascade_frontalface_default.xml"

faceCascade = cv2.CascadeClassifier(cascPath)

time.sleep(1)
for i in range(10):
    os.system("./capture.sh " + name + str(i))
    #time.sleep(0.5)

images = [cv2.imread(file) for file in glob.glob('../images/*.jpg')]

file_names = [str(file.split("/images/")[1]) for file in glob.glob('../images/*.jpg')]

def identifyFaces(img, name):
    found = False
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
        #flags = cv2.CV_HAAR_SCALE_IMAGE
    )
    if(len(faces) > 0):
        found = True
    #print("image: " + name +  str(len(faces)) + " found")
    
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    #cv2.imshow("Faces found", img)

    new_name = "../proc/" + name.split('.')[0] + "_proc" + ".jpg"
    

    cv2.imwrite(new_name, img)
    
    return found
    

counter = 0
for i in range(len(images)):
    if identifyFaces(images[i], file_names[i]):
        counter += 1
        print("found")
    else:
        print("not found")
if(counter > 0):
    print("Face is found")
print("done.")
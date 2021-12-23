import os
import cv2
import glob
import time

from skimage.metrics import structural_similarity

name = "pic"

cascPath = "haarcascade_frontalface_default.xml"

faceCascade = cv2.CascadeClassifier(cascPath)

time.sleep(1)
for i in range(2):
    os.system("./capture.sh " + name + str(i))
    #time.sleep(0.5)

images = [cv2.imread(file) for file in glob.glob('../images/*.jpg')]

file_names = [str(file.split("/images/")[1]) for file in glob.glob('../images/*.jpg')]

def identifyMovement(image1, image2, output_file_name_diff, display = False):
    #use structural similarity rather than direct pixel matching
    difference = cv2.subtract(image1, image2)
    gray_diff = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(gray_diff, 0, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)

    #visually show difference with red marking
    difference[mask != 255] = [0, 0, 255]

    ratio = float(len(difference[mask != 255])/len(difference))


    print("Red: ", len(difference[mask != 255]))
    print("Entire image: " , len(difference))

    print("Ratio: ", ratio)
    '''
    font = cv2.FONT_HERSHEY_SIMPLEX
  
    # org
    org = (50, 50)
    
    # fontScale
    fontScale = 1
    
    # Blue color in BGR
    color = (255, 0, 0)
    
    # Line thickness of 2 px
    thickness = 2

    cv2.putText(difference, ("Ratio: " + str(ratio)), org, font, 
                   fontScale, color, thickness, cv2.LINE_AA)
    '''
    cv2.imwrite(output_file_name_diff, difference)

    #overlay differences on image
    image1[mask != 255] = [0, 0, 255]
    image2[mask != 255] = [0, 0, 255]

    if(display):
        cv2.imshow("image 1", image1)
        cv2.waitKey()
        cv2.imshow("image 2", image2)
        cv2.waitKey()
        cv2.destroyAllWindows()

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
    
'''
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

'''


image1 = cv2.imread("../images/pic0.jpg")
image2 = cv2.imread("../images/pic1.jpg")

identifyMovement(image1, image2, "../proc/diff.jpg", display = True)
import os
import cv2
import glob
import time
import csv

from skimage.metrics import structural_similarity

def get_counter():
    f = open('counter.csv', 'r')
    counter = f.readlines()[0]
    return(int(counter))
def increment_counter():
    x = get_counter() + 1
    with open ('counter.csv','w') as f:
        write = csv.writer(f)
        write.writerow([str(x)])
def play_alarm():
    while(True):
        os.system('./sound.sh ' + str('piano2') + ' 50')

def capture_images(number = 10, prefix = "pic", delay = 0.5, forever = False):

    name = prefix
    if(forever):
        while(True):
            increment_counter()
            os.system("./capture.sh " + name + str(get_counter()))
            time.sleep(delay)
    else:
        for i in range(number):
            increment_counter()
            os.system("./capture.sh " + name + str(get_counter()))
            time.sleep(delay)

    # images = [cv2.imread(file) for file in glob.glob('../images/*.jpg')]

    # file_names = [str(file.split("/images/")[1]) for file in glob.glob('../images/*.jpg')]

def clear_images():
    filepath = "../images"
    for file in os.scandir(filepath):
        os.remove(file.path)
    with open ('counter.csv','w') as f:
        write = csv.writer(f)
        write.writerow([str(0)])

def identifyMovement_ssim(image1, image2, output_file_name_diff, display = False):
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

def IdentifyMovement(img1, img2):
    diff = cv2.absdiff(img1, img2)
    print(diff)


def identifyFaces(img, name, model = "haarcascade_frontalface_default.xml"):
    
    cascPath = model

    faceCascade = cv2.CascadeClassifier(cascPath)
    
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
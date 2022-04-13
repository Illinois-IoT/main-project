import os
import cv2
import glob
import time
import csv

from skimage.metrics import structural_similarity as compare_ssim
        
def play_sound(file_name = None, length = -1, volume = 50):
    if(file_name == None):
        raise Exception("No File Provided")
    if(int(length) == -1):
        while(True):
            os.system('./sound.sh ' + str(file_name) + " " + volume)
    elif(int(length) < 0):
        raise Exception("Time cannot be negative")
    else:
        os.system('./sound_timeout.sh ' + str(file_name) + " " + volume + " " + length)
        

def capture_images(name = "pic"):
    
    os.system("./capture2.sh " + name)
def convert_to_grayscale(read = "pic", write = "output"):
    img = cv2.imread("../images/" + read)
    #print(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    write_address = "../images/" + write + ".png"
    cv2.imwrite(write_address, gray)

def clear_images():
    filepath = "../images"
    for file in os.scandir(filepath):
        os.remove(file.path)
    with open ('counter.csv','w') as f:
        write = csv.writer(f)
        write.writerow([str(0)])




import threading
import sys

'''
preliminary project:
runs alarm until movement at door is seen

'''
from utils import *


def MostRecentMovement():
    index = get_counter()
    img1 = cv2.imread('../images/pic' + str(index - 1), cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread('../images/pic' + str(index), cv2.IMREAD_GRAYSCALE)
    if(IdentifyMovement(img1, img2) != None):
        #movement is found
        sys.exit()
        
    


#first thread takes pictures at given time intervals until result from second thread is found
'''
thread1 = threading.Thread(target = capture_images, args = {delay=2.0, forever=True} )

thread2 = threading.Thread(target = MostRecentMovement)

thread3 = threading.Thread(target = play_alarm)

thread1.start()
thread2.start()
thread2.start()

thread1.join()
thread2.join()
thread3.join()

'''

img1 = cv2.imread('../images/pic2.jpg', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('../images/pic3.jpg', cv2.IMREAD_GRAYSCALE)

cv2.imshow("mm", img1)
cv2.waitKey()

#print(img1)
#print(img2)
print(identifyMovement_ssim(img1, img2))

import threading

'''
preliminary project:
runs alarm until movement at door is seen

'''
from utils import *


def MostRecentMovement():
    index = get_counter()
    img1 = cv2.imread('../images/pic' + str(index - 1), cv2.IMREAD_GRAYSCALE)
    img1 = cv2.imread('../images/pic' + str(index), cv2.IMREAD_GRAYSCALE)
    

#first thread takes pictures at given time intervals until result from second thread is found
thread1 = threading.Thread(target = capture_images, args = [delay = 2.0, forever = True])

thread2 = thread


'''
img1 = cv2.imread('../images/pic20', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('../images/pic2', cv2.IMREAD_GRAYSCALE)


IdentifyMovement(img1, img2)
'''
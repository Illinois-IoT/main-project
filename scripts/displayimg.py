
import cv2
import glob

images = [cv2.imread(file) for file in glob.glob('../images/*.jpg')]

print(len(images))
cv2.imshow("Image", images[0])
cv2.waitKey()


'''
for image in images:
    cv2.imshow("Image", image)
    cv2.waitKey()
cv2.destroyAllWindows() 
'''

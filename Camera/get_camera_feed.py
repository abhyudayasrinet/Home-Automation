import cv2
camera = cv2.VideoCapture(0)
retval, im = camera.read()
print(retval)
print(im)
file = "image2.jpg"
cv2.imwrite(file, im)
del(camera)

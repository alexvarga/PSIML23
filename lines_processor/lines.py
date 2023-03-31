'''
There are a sequence of steps to achieve this:

    Find the optimum threshold to binarize your image. I used Otsu threshold.
    Find the suitable morphological operation that will form a single region along the horizontal direction. Choose a kernel that is larger in width than the height.
    Draw bounding boxes over the resulting contours

https://pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/ deskew text in an image
'''

import cv2
import numpy as np




path = "case-17.jpg"  # 41 r
path = "case-16.jpg"  # 41 contours problem
path = "Case_10.png" # 29 ok 
path = "case-0.png"  # 8
path = "case-15.jpg"  # 29 r problem
path = "case-6.jpg"  # 38
path = "case-3.jpg"  # 18 r
path = "case-4.jpg"  # 28 




img = cv2.imread(path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  

#cv2.imshow('gray',gray )



#gaussian blur #dont know if it's needed
kernel = np.ones((4,4),np.float32)/16
dst = cv2.filter2D(gray,-1,kernel)

cv2.imshow('blurred',dst )


#--- performing Otsu threshold ---
ret,thresh1 = cv2.threshold(dst, 0, 255,cv2.THRESH_OTSU|cv2.THRESH_BINARY_INV)

cv2.imshow('thresh1', thresh1)



# detecting the angle
coords = np.column_stack(np.where(thresh1>0))

angle = cv2.minAreaRect(coords)[-1]


if angle >30: #nemam ideju šta sam uradila 
    angle = (angle-90)
if angle < -45:
    angle = -(90 + angle) 
else:
    angle = -angle 


print(angle, "angle")


#rotating the image
(h, w) = img.shape[:2]
center = (w//2, h//2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(thresh1, M, (w, h), flags = cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
final = cv2.warpAffine(img, M, (w, h), flags = cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

#cv2.imshow('rotated', rotated)


#dilation
rect_kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (50, 4))

dilation = cv2.dilate(rotated, rect_kernel, iterations = 1)

cv2.imshow('dilation', dilation)

#finding the contoursyhg
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)



im2 = final #img.copy()
for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
cv2.imshow('final', im2)

cv2.waitKey(10000)
cv2.destroyAllWindows()

print(len(contours), "broj kontura")
cntsSorted = sorted(contours, key=lambda x: cv2.contourArea(x))

for cnt in cntsSorted:
    #print(cv2.contourArea(cnt))

    area = cv2.contourArea(cnt)
    x,y,w,h = cv2.boundingRect(cnt)
    print(x, y)
    # rect_area = w*h
    # extent = float(area)/rect_area
    # equi_diameter = np.sqrt(4*area/np.pi)

    pass

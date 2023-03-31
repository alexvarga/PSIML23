import cv2  
import numpy as np  
image = cv2.imread("map.png")  
template = cv2.imread("0.png")  
result = cv2.matchTemplate(image,template,cv2.TM_CCOEFF_NORMED)  
print(np.unravel_index(result.argmax(),result.shape))


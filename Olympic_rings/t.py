import numpy as np
import matplotlib.pyplot as plt


theta = np.arange(0,360)*np.pi/180

r=5

x=0
y=0
bprint = np.zeros((2*(r+1),2*(r+1)))
(m,n) = (r+1,r+1)      
for angle in theta:
            x = int(np.round(r*np.cos(angle)))
            y = int(np.round(r*np.sin(angle)))
            # bprint[m+x,n+y] = 1
            bprint[m+x, n+y] = 1 #slice

constant = np.argwhere(bprint)

plt.plot(bprint)
plt.show()

print(constant.shape)
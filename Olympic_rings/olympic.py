from PIL import Image, ImageOps, ImageFilter
import numpy as np
import matplotlib.pyplot as plt
import time

t0 = time.time()


width = 768
height = 768

#imgPath = input()
imgPath = 'set\\03.png'


img = Image.open(imgPath)
imgnp = np.array(img)
imgray = img.convert('L')

imgray = imgray.point(lambda p: p > 254 and 255)


inverted_image = ImageOps.invert(imgray)
print(inverted_image)
# inverted_image.show()

edges = imgray.filter(ImageFilter.FIND_EDGES)

edges = edges.convert('1')

puxels = inverted_image.load()
# plt.plot(edges)
# plt.show()


pixels=edges.load()



pxy = []
pxy2= []



for x in range(10, width-10):
    for y in range(10, height-10):
        if pixels[x,y]==255:
            pxy.append((x,y))


for x in range(width):
    for y in range(height):
        if puxels[x,y]==255:
            pxy2.append((x,y))
            pxy2.append((x+1,y+1))






print(len(pxy))
print(len(pxy2))


# pxy = pxy[::2]
# print(pxy[0:10])


def detectCircles(edges, region):

    (M, N) = (768, 768)

    R_min = 20
    R_max = 90

    R = R_max-R_min

    #for overflow
    A = np.zeros((R_max,M+2*R_max,N+2*R_max))
    B = np.zeros((R_max,M+2*R_max,N+2*R_max))

    theta = np.arange(0, 360)*np.pi/180

    for val in range(R):
        r = R_min+val
        bprint = np.zeros((2*(r+1), 2*(r+1))) #bluepring
        (m, n) = (r+1, r+1) #center of blueprint

        for angle in theta:
            x = int(np.round(r*np.cos(angle)))
            y = int(np.round(r*np.sin(angle)))
            bprint[m+x,n+y] = 1

        # print(bprint.shape)

        # print(edges[200:220])

        for x, y in edges:
            X = [x-m+R_max,x+m+R_max]
            Y= [y-n+R_max,y+n+R_max]   


            A[r,X[0]:X[1],Y[0]:Y[1]] += bprint

        
        A[r][A[r]<256] = 0



    for r,x,y in np.argwhere(A):
        temp = A[r-region:r+region,x-region:x+region,y-region:y+region]
        try:
            p,a,b = np.unravel_index(np.argmax(temp),temp.shape)
        except:
            print("except")
            continue
        B[r+(p-region),x+(a-region),y+(b-region)] = 1

    print(sum(sum(sum(B))))
    return (B[:,R_max:-R_max,R_max:-R_max])



asdf = detectCircles(pxy, 15)

coords = np.argwhere(asdf)
print(coords)

t1 = time.time()

print(t1-t0, "VREME")

y=0
b=0
k=0
g=0
r=0


for px in img.getdata():
    if px == (0, 0, 0): 
        k += 1
    elif px == (255, 0, 0):
        r += 1
    elif px == (0, 255, 0):
        g += 1
    elif px == (0, 0, 255):
        b += 1
    elif px == (255, 255, 0):
        y += 1

print(y, b, k, g, r)



from PIL import Image


imgPath = input()
img = Image.open(imgPath)
pixels = img.load()

def findPos(positions, xForMinY):
    output = []
    for position in positions:
        if xForMinY[0] == position[0] and xForMinY[1]<=position[1] :
            output.append(position)
    return output

def distances(positions):
    psiibleRadii = []
    for i in range(len(positions)-1):
        for j in range(i+1, len(positions)):
            d = abs(positions[i][1]-positions[j][1])
            d2 = d//2
            if d<768/4 and d2>5:
                if(d2 not in psiibleRadii):
                    psiibleRadii.append(d2)
    return psiibleRadii

def getCenter(verticalPositions, possibleRadiiK, allPositions):
    centers = []
    for x, y in verticalPositions:
        for i in possibleRadiiK:
            if i>1:
                lx = x-i
                ly = y+i
                rx = x+i
                ry = y+i
                dx = x
                dy = y+2*i
                if (lx, ly)in allPositions and (rx, ry)in allPositions and (dx, dy)in allPositions :
                    centers.append((x, y+i, i))
    return centers   


def countPixelsOfColor(pixels, color, xStart=0, xRange=768, yStart=0, yRange=768): #verovatno mi ne trebaju pozicije
    c=""
    count = 0
    positions = []
    if color == "k":
        c = (0, 0, 0)
    elif color == "r":
        c = (255, 0, 0)
    elif color =="g":
        c = (0, 255, 0)
    elif color == "b":
        c = (0, 0, 255)
    elif color == "y":
        c=(255, 255, 0)

    for x in range(xStart, xRange):
        for y in range(yStart, yRange):
            if pixels[x, y][:3]==c:
                count+=1
                positions.append((x,y))
    return count

def countPixels(pixels, xStart=0, xRange=768, yStart=0, yRange=768):
    ye=0
    b=0
    k=0
    g=0
    r=0

    blackPositions =[]
    redPositions =[]
    greenPositions = []
    bluePositions = []
    yellowPositions = []


    for x in range(0, xRange):
        for y in range(0, xRange):
            if pixels[x,y][:3]==(0, 0, 0):
                k += 1
                blackPositions.append((x,y))
            if pixels[x,y][:3]==(255, 0, 0):
                r += 1
                redPositions.append((x,y))
            if pixels[x,y][:3]==(0, 255, 0):
                g += 1
                greenPositions.append((x,y))
            if pixels[x,y][:3]==(0, 0, 255):
                b += 1
                bluePositions.append((x,y))
            if pixels[x,y][:3]==(255, 255, 0):
                ye += 1
                yellowPositions.append((x,y))            

    return ye, b, k, g, r, blackPositions, redPositions, greenPositions, bluePositions, yellowPositions


def getPixelsOfInterest(colorPositions):
    pixelsofinterest = []
    for pixel in range(767):
        z = [item for item in colorPositions if item[0] == pixel]
        if len(z)>0:
            pixelsofinterest.append(min(z))
            
    return pixelsofinterest


def getCircle(pixels):
    circles=[]
    pixelsofinterest = getPixelsOfInterest(pixels)
    
    for xForMinY in (pixelsofinterest):
        vp = findPos(pixels, xForMinY)
        if len(vp):
            possibleRadiiK = distances(vp)
            if len(possibleRadiiK)>0:
                a = getCenter(vp, possibleRadiiK, pixels)
                if a:
                    circles.append(a)
            else:
                pass
    flat=list()
    for sub in circles:
        flat += sub

    return flat


def getRegionBounds(circles):
    regions=[]
    for b in circles:
        l = b[0]-b[2]*3.5
        r = b[0]+b[2]*3.5
        u = b[1]-b[2]*3.5
        d = b[1]+b[2]*3.5

        l=l*int(l>1)
        u=u*int(u>1)
        if r>767:
            r=767
        if d>767:
            d=767

        
        regions.append((l, r, u, d, b[0], b[1], b[2]))
    return regions
    


def getCircleInBounds(circles, regionBounds, color=""):
    for circle in circles:
        cx = circle[0]
        cy = circle[1]
        cradius = circle[2]
        if cx-cradius >regionBounds[0] and cx+cradius< regionBounds[1] and cy-cradius>regionBounds[2] and cy+cradius<regionBounds[3]:
            return circle

   


def getRegionLogos(bounds, rC, gC, bC, yC):
    possibleLogos=[]
    r = None
    g = None
    bl = None
    y = None
    
    for b in bounds:
        r = getCircleInBounds(rC, b, "r")
        g = getCircleInBounds(gC, b, "g")
        bl = getCircleInBounds(bC, b, "bl")
        y = getCircleInBounds(yC, b, "y")
        if r and g and bl and y:
            possibleLogos.append([y, bl, (b[4], b[5], b[6]), g, r])
    return possibleLogos


ye, b, k, g, r, blackPositions, redPositions, greenPositions, bluePositions, yellowPositions = countPixels(pixels)
redCircles = getCircle(redPositions)
gCircles = getCircle(greenPositions)
bCircles = getCircle(bluePositions)
blackCircles = getCircle(blackPositions)
yCircles = getCircle(yellowPositions)

print("Y", ye)
print("B", b)
print("K", k)
print("G", g)
print("G", r)

bounds = getRegionBounds(blackCircles) 

possibleLogos = getRegionLogos(bounds, redCircles, gCircles, bCircles, yCircles)

# y b k g r
def validateLogos(possibleLogos):
    logos = possibleLogos
    valid = []

    for i in range(len(logos)):
        
        cyellow = logos[i][0]
        ryellow = cyellow[2] 
        cblue = logos[i][1]
        rblue = cblue[2] 
        cblack = logos[i][2]
        rblack = cblack[2] 
        cgreen = logos[i][3]
        rgreen = cgreen[2]
        cred = logos[i][4]
        rred = cred[2]

        ehBlack = countPixelsOfColor(pixels, 'k', cblack[0]-rblack, cblack[0]+rblack, cblack[1]-rblack, cblack[1]+rblack)
        ehBlue = countPixelsOfColor(pixels, 'b', cblue[0]-rblue, cblue[0]+rblue, cblue[1]-rblue, cblue[1]+rblue)
        ehRed = countPixelsOfColor(pixels, 'r', cred[0]-rred, cred[0]+rred, cred[1]-rred, cred[1]+rred)
        ehGreen = countPixelsOfColor(pixels, 'g', cgreen[0]-rgreen, cgreen[0]+rgreen, cgreen[1]-rgreen, cgreen[1]+rgreen)
        ehYellow = countPixelsOfColor(pixels, 'y', cyellow[0]-ryellow, cyellow[0]+ryellow, cyellow[1]-ryellow, cyellow[1]+ryellow) 
        avg = (ehBlack + ehBlue + ehRed + ehGreen + ehYellow)/5
        help = avg/10
        
        if countPixelsOfColor(pixels, "g", cyellow[0]-ryellow, cyellow[0]+ryellow, cyellow[1]-ryellow, cyellow[1]+ryellow)>help or \
           countPixelsOfColor(pixels, "r", cyellow[0]-ryellow, cyellow[0]+ryellow, cyellow[1]-ryellow, cyellow[1]+ryellow)>help or \
           countPixelsOfColor(pixels, "r", cblue[0]-rblue, cblue[0]+rblue, cblue[1]-rblue, cblue[1]+rblue)>help or \
           countPixelsOfColor(pixels, "g", cblue[0]-rblue, cblue[0]+rblue, cblue[1]-rblue, cblue[1]+rblue)>help or \
           countPixelsOfColor(pixels, "k", cblue[0]-rblue, cblue[0]+rblue, cblue[1]-rblue, cblue[1]+rblue)>help or \
           countPixelsOfColor(pixels, "r", cblack[0]-rblack, cblack[0]+rblack, cblack[1]-rblack, cblack[1]+rblack)>help or \
           countPixelsOfColor(pixels, "b", cblack[0]-rblack, cblack[0]+rblack, cblack[1]-rblack, cblack[1]+rblack)>help  or \
           countPixelsOfColor(pixels, "y", cgreen[0]-rgreen, cgreen[0]+rgreen, cgreen[1]-rgreen, cgreen[1]+rgreen)>help or \
           countPixelsOfColor(pixels, "b", cgreen[0]-rgreen, cgreen[0]+rgreen, cgreen[1]-rgreen, cgreen[1]+rgreen)>help or\
           countPixelsOfColor(pixels, "k", cred[0]-rred, cred[0]+rred, cred[1]-rred, cred[1]+rred)>help or \
           countPixelsOfColor(pixels, "y", cred[0]-rred, cred[0]+rred, cred[1]-rred, cred[1]+rred)>help or \
           countPixelsOfColor(pixels, "b", cred[0]-rred, cred[0]+rred, cred[1]-rred, cred[1]+rred)>help :
            continue

        valid.append(logos[i])
    return valid

validLogos = validateLogos(possibleLogos)
print(len(validLogos))

for l in validLogos:
    print("Y", l[0][0], l[0][1])
    print("B", l[1][0], l[1][1])
    print("K", l[2][0], l[2][1])
    print("G", l[3][0], l[3][1])
    print("R", l[4][0], l[4][1])
import numpy as np
import sys

sys.stdout = open("log.txt", "w")

folder = "inputs"
filePath = "10.txt"
lines = []
with open(folder+"\\"+filePath) as my_file:
    for line in my_file:
        lines.append(line)
       

pnt = [[0, 0, 0], [0, 0, 1], [0,1,0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]
edgePnt = [[0, 0],[0, 1], [1, 0], [1, 1] ]
voxPositions = []
for l in lines:
    voxPositions.append(eval(l))

points = []
for i in voxPositions:
    vox = []
    for a in pnt:
        vox.append((i[0]+a[0],i[1]+a[1],i[2]+a[2]))
    points.append(vox)



def getMinMaxForXY(points):
    minx = min(points, key=lambda x:x[0])[0]
    miny = min(points, key=lambda x:x[1])[1]
    maxx = max(points, key=lambda x:x[0])[0]
    maxy = max(points, key=lambda x:x[1])[1]
    

    return minx, miny, maxx, maxy


def countSquares(points):
    count = 0
    for item in points:
        if (item[0], item[1]+1) in points and (item[0]+1, item[1]) in points and(item[0]+1, item[1]+1) in points and item in points:
            count+=1    

    return count


def getAllSides(voxel):
    v = np.array(voxel)
    left = np.array([[0, 0, 0],[1, 0, 0],[1, 1, 0],[0, 1, 0]])
    right = np.array([[0, 0, 1],[1, 0, 1],[1, 1, 1],[0, 1, 1]])
    face  = np.array([[0, 0, 0],[1, 0, 0],[1, 0, 1],[0, 0, 1]])
    back =  np.array([[0, 1, 0],[1, 1, 0],[1, 1, 1],[0, 1, 1]])
    up =    np.array([[1, 0, 0],[1, 1, 0],[1, 1, 1],[1, 0, 1]])
    down =  np.array([[0, 0, 0],[0, 1, 0],[0, 1, 1],[0, 0, 1]])
    
    sides = [left+v, right+v, face+v, back+v, up+v, down+v]
    return sides



def getTotalArea(voxPositions):
    a = getAllSides(voxPositions[0])
    for i in range(1, len(voxPositions)):
        a=np.concatenate((a, getAllSides(voxPositions[i])))
    ss, counts = np.unique(a, axis=0, return_counts=True)
    indices = np.where(counts>1)

    outerSides = np.delete(ss, indices, axis=0)
    return outerSides


outerSides = getTotalArea(voxPositions)

xx =[]
yy =[]
zz =[]
for i in outerSides:
    if i[0][0] == i[1][0] == i[2][0] == i[3][0]:
        xx.append(i)
    if i[0][1] == i[1][1] == i[2][1] == i[3][1]:
        yy.append(i)
    if i[0][2] == i[1][2] == i[2][2] == i[3][2]:
        zz.append(i)



def getDict(sides, position):
    d = {}
    for subarray in sides:
        key = subarray[0][position]
        if key not in d:
            d[key] = [subarray]
        else:
            d[key].append(subarray)


    return d

dxx = getDict(xx, 0)
dyy = getDict(yy, 1)
dzz = getDict(zz, 2)

def getCntArr(ps):
    cnts=[]
    cnt=[]

    for p in ps:
        if ([p[0]+1, p[1]+0]) in ps:
            
            if(p[0], p[1]) not in cnt:
                cnt.append((p[0], p[1]))

            if(p[0]+1, p[1]+0) not in cnt:
                cnt.append((p[0]+1, p[1]+0))
    
        elif ([p[0]+0, p[1]+1]) in ps:
            if(p[0], p[1]) not in cnt:
                cnt.append((p[0], p[1]))

            if(p[0]+0, p[1]+1) not in cnt:
                cnt.append((p[0]+0, p[1]+1))

        elif (([p[0]+1, p[1]+0]) not in ps) and (([p[0]+0, p[1]+1]) not in ps):
            cnts.append(cnt)
            cnt=[]
    return cnts

def heleprArray(l):
    x = np.arange(l+1)
    y = np.arange(l+1)
    X, Y = np.meshgrid(x, y)
    coords = np.stack((X.ravel(), Y.ravel())).T
    
    return coords


def isInSquare(pomocni, allpoints):

    for elem in pomocni:
    # Check if the element is in b_arr
        if not np.any(np.all(allpoints == elem, axis=1)):
            print("Element", elem, "is not contained in b.")
            return False
    else:
        print("All elements in a are contained in b.")
        return True



def getSquareIfAny(cntPoints):
    square = 1
    p = []
    for p in cntPoints:
        if len(cntPoints)>1:
            i = 1
            s=1
            p1 = [p[0], p[1]]
            while i !=-1:
                pomocni = np.add(heleprArray(i), p1)
                if isInSquare(pomocni, cntPoints):
                    s=s+1
                    i=i+1
                if s>square:
                    square=s
                    print("square", square)
                else:
                    i=-1
                    break
                # print("\n __________pomocxni________\n", pomocni, "\n------cntpoints---------", cntPoints, "\n+++++++++++++++++++++++++++++++++\n\n")
                # a = np.apply_along_axis(lambda dx: np.array_equiv(dx, pomocni), 1, cntPoints)
                # print("ASSSS", a)
                
                # if (np.isin(pomocni, cntPoints).all(axis=1)).all(axis=0):
                # if np.apply_along_axis(lambda x: np.array_equiv(x, pomocni), 1, cntPoints).any():
                    # s=s+1
                    # i=i+1
                    


                print("p1: ", p1)
                print("I, s", i, s)

    print("THIS IS THE SQUARE I RETURN", square)
    return square



def getLargestConArea(dict, level):
    largestContArea = 0
    maxSquare=1
    
    for key in dict:
        pnts = []
        arr = []
        for item in dict[key]:
            cnt = []

            point =  np.min(item, axis = 0)
            if level == 0:
                pnts.append([point[1], point[2]])
            elif level==1:
                pnts.append([point[0], point[2]])
            elif level==2:
                pnts.append([point[0], point[1]])
            
        arr = getCntArr(pnts)
        for item in arr:
            newSquare = getSquareIfAny(item)
            print("this is the SQUARE I GTO DUDE", newSquare)
            if newSquare>maxSquare:
                print("newSquare is bigger than maxSquare here they are", newSquare, maxSquare)
                maxSquare=newSquare
                print(maxSquare)
            if len(item)>largestContArea:
                largestContArea = len(item)
                
    print("this is the square that i return, i think i have a problem", maxSquare)
    return largestContArea, maxSquare



a, asq = getLargestConArea(dxx, 0)
b, bsq = getLargestConArea(dyy, 1)
c, csq = getLargestConArea(dzz, 2)


print(asq, bsq, csq)

maxabc = max(a,b,c)
maxsq = max(asq, bsq, csq)

landing = ((maxsq/2)**2)*np.pi

print(outerSides.shape[0], maxabc, landing)



sys.stdout.close()
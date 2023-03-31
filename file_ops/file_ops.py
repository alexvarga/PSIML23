import os

def checkCount(pathToFile, count):   
    counter = 0 
    with open (pathToFile, 'r') as flj:
        a = flj.readlines()
        for i in a:
            counter = counter + i.count("PSIML")
    return int(count) == counter



putanja=input()
numberOfCorrectFiles=0
for path, subdirs, files in os.walk(putanja):
    print(  files, "files")
    for name in files:
        if "PSIML" in name:
            numberOfCorrectFiles = numberOfCorrectFiles+ int(checkCount(os.path.join(path, name), name.split('_')[1].split('.')[0]))


print(numberOfCorrectFiles)

import numpy as np
import matplotlib.pyplot as plt


MORSE_CODE_DICT = { 'a':'.-', 'b':'-...', 'c':'-.-.',
                    'v':'-.-.', 'd':'-..', 'e':'.',
                    'f':'..-.', 'g':'--.', 'h':'....',
                    'i':'..', 'j':'.---', 'k':'-.-',
                    'l':'.-..', 'm':'--', 'n':'-.',
                    'o':'---', 'p':'.--.', 'q':'--.-',
                    'r':'.-.', 's':'...', 't':'-',
                    'u':'..-', 'v':'...-', 'w':'.--',
                    'x':'-..-', 'y':'-.--', 'z':'--..'}


morse_file = input()
with open (morse_file, 'r') as f:
    lines = f.readlines()

print(float(lines), "---------------------------")


sum =0
min = 0
max=0
d = len(lines)
asdf=[]
for line in lines:  #traži min i max u signalu 
    if(float(line))<min:
        min = float(line)
    if float(line)>max:
        max = float(line)
    sum=sum+float(line)
    asdf.append(float(line))


thresh = (min+max)/2


def scaled(a):
    return (float(a) - min) / (max - min)

y=0
for i in range(1,d-1):
    if scaled(asdf[i-1])<thresh and scaled(asdf[i+1])<thresh and scaled(asdf[i])>thresh:
        asdf[i] = (asdf[i-1]+asdf[i+1])/2
        print('hello')
    if scaled(asdf[i-1])>thresh and scaled(asdf[i+1])>thresh and scaled(asdf[i])<thresh:
        asdf[i] = (asdf[i-1]+asdf[i+1])/2
        print("hello2")
       





durationUnit =0
nule = 0 #brojači za 0 i 1
jedinice = 0
ticksArray = [] 

for line in asdf:
    ev_scaled = scaled(line)
    if ev_scaled < (min+max)/2:  #ako je manje od tresholda povećavam broj nula
        nule+=1
        if jedinice<0: # ako smo naišli na nulu, a imamo da je broj jedinica (jedinice brojim unazad -1, -2....) veći od 0, upisujem jedinice u array 
            ticksArray.append(jedinice)
        jedinice =0 # resetujem broj jedinica 

    else:  #ako je veće od tresholda povećavam broj jedinica dole
        if nule>0: #ako smo imali izbrojane nule upisujemo ih
            ticksArray.append(nule)
            if durationUnit==0 or nule<durationUnit: #ovo je nepotrebno, durationUnit računam na drugi način dole
                durationUnit=nule
        jedinice-=1 #povećavam broj jedinica
        nule = 0 #resetujem broj nula...
        
if jedinice<0: # for line in line petlja izađe pre nego što upiše poslednje izbrojano pa to radimo ovde na kraju
    ticksArray.append(jedinice)
if nule>0:
    ticksArray.append(nule)

print(ticksArray)

lst = abs(np.array(ticksArray)) #konvertujem python list u np.array tip za lakše pronalaženje najčešće vrednosti 


#nalazi najčešću vrednost z ticksArray. pretpostavljam da će mi to biti dužina kratkog tona . 
def mostFrequent(arr, n):
  maxcount = 0;
  element_having_max_freq = 0;
  for i in range(0, n):
    count = 0
    for j in range(0, n):
      if(arr[i] == arr[j]):
        count += 1
    if(count > maxcount):
      maxcount = count
      element_having_max_freq = arr[i]
    
  return element_having_max_freq;


durationUnit= (mostFrequent(lst, len(lst))) #jedinica dužine je vrednost koja se najćešće pojavljuje u nizu


def decrypt(message): #funkcija za prevođenje .- u tekst
    message += ' '
    decipher = ''
    citext = ''
    for letter in message:

        if (letter != ' '):
            i = 0
            citext += letter
        else:
            i += 1
            if i == 2 :
                decipher += ' '
            else:
                try:
                # accessing the keys using their values (reverse of encryption)
                    decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT
                    .values()).index(citext)]
                    citext = ''
                except:
                    pass #ovo se ne radi ovako xD

    return decipher



def noiseReduction(arrayic): #pedestrian way
#ako nešto iz niza nije deljivo jedinicom vremena sabiram sa sledećim elementom. Pretpostavljam da je razdvojeno zbnog šuma. 
#brute force način. ne funkcioniše za test slučaj 8 i 9

    newArr = []
    temp = 0
    for i in arrayic:
        if i%durationUnit != 0:
            temp+=abs(i)
        elif i/durationUnit!=float(1) and i/durationUnit!=float(-1) and \
             i/durationUnit!=float(3) and i/durationUnit!=float(-3) and \
             i/durationUnit!=float(7) and i/durationUnit!=float(-7):

            temp+=abs(i)
            
        else:
            if temp != 0:
                if i>0:
                    newArr.append(-temp)
                elif i<0:
                    newArr.append(temp)
                temp=0
            newArr.append(i)
    return newArr


a = noiseReduction(ticksArray)


print(a)

letter =''        
morse_message = ''
for item in a:     #for item in ticksArray ako želimo da preskočimo "noise reduciton"
    if item/durationUnit == -1:
        morse_message+='.'
    elif item/durationUnit==-3:
        morse_message+='-'
    elif item/durationUnit==1:
        morse_message+=''
    elif item/durationUnit==3:
        morse_message+=' '
    elif item/durationUnit==7:
        morse_message+='  '

print(morse_message)
print(decrypt(morse_message))
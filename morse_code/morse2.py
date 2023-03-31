import numpy as np

MORSE_CODE_DICT = { 'a':'.-', 'b':'-...', 'c':'-.-.',
                    'v':'-.-.', 'd':'-..', 'e':'.',
                    'f':'..-.', 'g':'--.', 'h':'....',
                    'i':'..', 'j':'.---', 'k':'-.-',
                    'l':'.-..', 'm':'--', 'n':'-.',
                    'o':'---', 'p':'.--.', 'q':'--.-',
                    'r':'.-.', 's':'...', 't':'-',
                    'u':'..-', 'v':'...-', 'w':'.--',
                    'x':'-..-', 'y':'-.--', 'z':'--..'}

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

#nalazi najčešću vrednost z ticksArray. pretpostavljam da će mi to biti dužina kratkog tona . 
def mostFrequent(arr, n):
  maxcount = 0;
  element_having_max_freq = 0;
  for i in range(0, n):
    count = 0
    for j in range(0, n):
      if(abs(arr[i]) == abs(arr[j])):
        count += 1
    if(count > maxcount):
      maxcount = count
      element_having_max_freq = abs(arr[i])
    
  return element_having_max_freq;

#readfile
morse_file = input()
with open (morse_file, 'r') as f:
    lines = f.readlines()


#get min and max and make a list of float values
min = -1
max = -1
inputElements=[]
for i in range(len(lines)):
    element = float(lines[i])
    if i == 0:
        min = element
        max = element
    else:
        if element<min:
            min=element
        if element>max:
            max=element
    inputElements.append(element)
    
print(min, max)

npInputElements = np.array(inputElements)
arrayavg = np.average(npInputElements)

durationUnit =0
nule = 0 #brojači za 0 i 1
jedinice = 0
ticksArray = [] 

## searching for unit of time
for item in npInputElements:
    ev_scaled = item
    if ev_scaled < (arrayavg):  #ako je manje od tresholda povećavam broj nula
        nule+=1
        if jedinice<0: # ako smo naišli na nulu, a imamo da je broj jedinica (jedinice brojim unazad -1, -2....) veći od 0, upisujem jedinice u array 
            ticksArray.append(jedinice)
        jedinice =0 # resetujem broj jedinica 

    else:  #ako je veće od tresholda povećavam broj jedinica dole
        if nule>0: #ako smo imali izbrojane nule upisujemo ih
            ticksArray.append(nule)
            # if durationUnit==0 or nule<durationUnit: #ovo je nepotrebno, durationUnit računam na drugi način dole
            #     durationUnit=nule
        jedinice-=1 #povećavam broj jedinica
        nule = 0 #resetujem broj nula...
        
if jedinice<0: # for line in line petlja izađe pre nego što upiše poslednje izbrojano pa to radimo ovde na kraju
    ticksArray.append(jedinice)
if nule>0:
    ticksArray.append(nule)

durationUnit= (mostFrequent(ticksArray, len(ticksArray))) #jedinica dužine je vrednost koja se najćešće pojavljuje u nizu
#print(ticksArray, durationUnit)



messageString = ''
print(len(npInputElements), "what now")
for i in range(int(len(npInputElements)/durationUnit)):
    value = ((np.average(inputElements[i*durationUnit: i*durationUnit+durationUnit]))>arrayavg)
    messageString=messageString+str(int(value))

messageString=messageString.replace('111', '-')
messageString=messageString.replace('0000000', '   ')
messageString=messageString.replace('000', ' ')
messageString=messageString.replace('0', '')
messageString=messageString.replace('1', '.')




print(messageString)
print(decrypt(messageString))



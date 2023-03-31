lines = input().split('\\n')


cntD = 0
cntF = 0
for i in lines:
    cntd = i.count('(d)')
    cntf = i.count('(f)')
    
    cntD=cntD+cntd
    cntF=cntF+cntf

  

print(cntD, cntF)
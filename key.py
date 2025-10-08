import random as r
def key(length:int,th:int):
    chars=[]
    for i in range(0,length):
        c=chr(r.randint(0,th))
        chars.append(c)
    re=''.join(i for i in chars)
    return re
a={'message':'hi','key':key(1000,1000)}
def dekeya():
    global a
    chars=[]
    char=''
    j=0
    for i in range(0,len(set(a['key']))):
     while char!=a['key'][i]:
         char=chr(r.randint(0,1000))
         j+=1
     chars.append(char)
    re=''.join(i for i in chars)
    return re,j
def dekey(a):
    chars=[]
    char=''
    j=0
    for i in range(0,len(set(a))):
        while char!=a[i]:
            char=chr(r.randint(0,1000))
            j+=1
        chars.append(char)
    re=''.join(i for i in chars)
    return re,j

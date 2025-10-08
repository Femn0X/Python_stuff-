import math
NaN=math.nan
class num:
    def __init__(self,ex:int|float|complex):
        errors=[]
        self.ex=ex
        if isinstance(ex,(int,float,complex)):
            pass
        else:
            try:
                num(int(self.ex,base=10))
            except Exception as e:
                errors.append(e)
        self.errors=errors
        if len(errors)>0:
            self.Error()
    def Error(self):
        raise Exception(f'errors:{self.errors}')
    def imag(self):
        return self.ex.imag
    def __repr__(self):
        return f'Num:{self.ex}'
    def __str__(self):
        return f'Num:{self.ex}'
    def __add__(self,other):
        if isinstance(other,num):
            return num(self.ex+other.ex)
        else:
            return num(self.ex+other)
    def __radd__(self,other):
        return self.__add__(other)
    def __sub__(self,other):
        if isinstance(self,other):
            return num(self.ex-other)
class realNum:
    def __init__(self,ex:int|float):
        if not isinstance(ex,(int,float)):
            raise TypeError(f'{ex} is not a real nummber')
        self.ex=num(ex)
    def __repr__(self):
        return f'ReaNum:{self.ex}'
def sum(a:list[realNum]):
    c=0
    for char in a:
        c+=char
    re=c/len(a)
    return re,c
def charInput(prompt):
    return input(prompt)[0]
def _ascii(char='',number:num=0):
    i=0
    for _char in char:
        i+=1
    if  i>1:
        raise Exception('not a single chareter')
    if char:
        return ord(char)
    if number:
        return chr(number)
def asciiPrint(ex='',ey=0):
    re=_ascii(ex,ey)
    print(re)
def asciiInput(prompt):
    a=input(prompt)
    try:
        re=_ascii(number=int(a,base=10))
        return re
    except Exception:
        pass
    re=_ascii(char=a[0])
    return re
def log(base,x):
    return math.log(x,base)
def pow(x,y):
    return math.pow(x,y)
def sqrt(base,x):
    for i in range(0,base):
        x=math.sqrt(x)
    return x
def instanceBuiltIn(obj:any)->str:
    __doc__='return class of obj as a string'
    re='notBiuldIn'
    if isinstance(obj,int):
        re='int'
    if isinstance(obj,float):
        re='float'
    if isinstance(obj,complex):
        re='complex'
    if isinstance(obj,str):
        re='str'
    if isinstance(obj,tuple):
        re='tuple'
    if isinstance(obj,list):
        re='list'
    if isinstance(obj,dict):
        re='dict'
    if isinstance(obj,set):
        re='set'
    if isinstance(obj,range):
        re='range'
    if isinstance(obj,bool):
        re='bool'
    if isinstance(obj,bytes):
        re='bytes'
    if isinstance(obj,bytearray):
        re='bytearray'
    if isinstance(obj,classmethod):
        re='classmethod'
    if isinstance(obj,enumerate):
        re='enumerate'
    if isinstance(obj,Exception):
        re='exception'
    if isinstance(obj,filter):
        re='filter'
    if isinstance(obj,frozenset):
        re='frozenset'
    if isinstance(obj,map):
        re='map'
    if isinstance(obj,memoryview):
        re='memoryview'
    if isinstance(obj,object):
        re+=',object'
    if isinstance(obj,property):
        re='property'
    if isinstance(obj,range):
        re='range'
    if isinstance(obj,reversed):
        re='reversed'
    if isinstance(obj,slice):
        re='slice'
    if isinstance(obj,super):
        re='super'
    if isinstance(obj,type):
        re='type'
    if isinstance(obj,Warning):
        re='waring'
    if isinstance(obj,zip):
        re='zip'
    return re
def subfac(n):
    i=1
    re=0 if n>0 else 1
    while n:
        re+=i
        i+=1
        n-=1
    return re
def nsubfac(x,max=1000):
    re=0
    i=1
    if x>0:
     while True:
        if x==subfac(i):
            re=i
            break
        i+=1
        if i>max:
            break
    return re
def pytagoras(a=0,b=0,c=0): 
    if a:
        if b:
            if c:
                return ValueError
            else:
                re=sqrt(1,a**+b**2)
        elif c:
            re=a-sqrt(1,c)
        else:
            return ValueError
    elif b:
        if c:
            re=b-sqrt(1,c)
        else:
            return ValueError
    else:
        return ValueError
    return re
def fac(n):
    i=1
    re=1
    while n:
        re*=i
        i+=1
        n-=1
    return re
def nfac(x,max=1000):
    re=0
    i=i
    if x>0:
        while True:
            if x==fac(i):
                re=i
                break
            i+=1
            if i>max:
                break
    return re
def getStrLen(a:str|num|realNum|complex):
    re=0
    for e in str(a):
        re+=1
    if isinstance(a,complex):
        re-=2
    if isinstance(a,num):
        if a.imag():re-=6
        else:re-=4
    if isinstance(a,realNum):
        re-=11
    if isinstance(a,(list,set,dict)):raise TypeError(f'type:{instanceBuiltIn(a)} is not supported')
    return re
def numify(a:str):
    errors=[]
    re=NaN
    try:
        re=int(a,base=10)
    except Exception as e:
        errors.append(e)
    if isinstance(re,(int,float)):
        return num(re)
    try:
        re=float(a)
    except Exception as e:
        errors.append(e)
    if isinstance(re,(int,float)):
        return num(re)
    try:
        re=complex(a)
    except Exception as e:
        errors.append(e)
    if isinstance(re,complex):
        return num(re)
    raise Exception(f'could not convert {a} to a number,errors:{errors}')
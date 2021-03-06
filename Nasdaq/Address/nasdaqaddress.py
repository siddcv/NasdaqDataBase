import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import ssl
import time
import re
from re import search

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def camel_case_split(str):
    start_idx = [i for i, e in enumerate(str)
                 if e.isupper()] + [len(str)]

    start_idx = [0] + start_idx
    return [str[x: y] for x, y in zip(start_idx, start_idx[1:])]

def validateString(s):
    letter_flag = False
    number_flag = False
    for i in s:
        if i.isalpha():
            letter_flag = True
        if i.isdigit():
            number_flag = True
    return letter_flag and number_flag

symbol=list()

#filling symbol from txt file***************************************************
f=open("nasdaqsymbol.txt")
for line in f:
    sym=line.split()
    symbol.append(sym[0])
#******************************************************************************
i=1701
ctr=0
address=list()
sector=list()
industry=list()
fte=list()
ceo=list()
ceosalary=list()
phone=list()
while i<=2000:
#building url***************************************************************
    url="https://finance.yahoo.com/quote/"
    url1=symbol[i]
    url2="/profile?p="
    url3=url+url1+url2+url1
    print(url3)
#***************************************************************************
#Cursor on html**************************************************************
    req = Request(url3, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = BeautifulSoup(html, "html.parser")
#***********************************************************************************
#getting address, phone number, email***********************************************
    tags= soup("p",{"D(ib) W(47.727%) Pend(40px)"})
    if len(tags)==0:
        address.append("N/A")
    if symbol[i]=="NICE" or symbol[i]=="PZZA":
        address.append("N/A")
        i+=1
        continue
    for tag in tags:
        y=tag.text
        print(y)
        str=y.split()
        print(str)
        j=0
        flagadd=0

        add=" "
        for j in range(len(str)):
            print(add)
            print(str[j])
            if flagadd==0:
                add=str[j]
                flagadd=1
                continue
            check=validateString(str[j])
            print(check)
            if check == True:
                t=re.split('(\d+)',str[j])
                print(t)
                for s in range(len(t)):
                    if s==0:
                        add=add+t[s]
                    else:
                        add=add+" "+t[s]
                continue
            up=0
            low=0
            for k in str[j]:
                if k.isupper():
                    up+=1
                if k.islower():
                    low+=1
            print(up)
            print(low)
            if up==1:
                add=add+" "+str[j]
                continue
            if up>1 and low!=0:
                n=camel_case_split(str[j])
                print(n)
                for s in range(len(n)):
                    if s==0:
                        add=add+n[s]
                    else:
                        add=add+" "+n[s]
                continue
            if low==0:
                add=add+" "+str[j]
                continue
        address.append(add)
    i+=1
    time.sleep(3)
print(address)

i=1701
ctr=0
f=open("nasdaqaddress.txt","a")
while i<=2000:
    statement=symbol[i]+" "+address[ctr]
    f.write(statement)
    f.write("\n")
    i+=1
    ctr+=1
f.close()

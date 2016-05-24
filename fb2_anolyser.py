import os,glob,re,codecs,sys
import xml.etree.ElementTree as ET

def dirs(d):
    return next(os.walk(d))[1]

STD_LIST_CHARS = 46 * 59
	
print("F2b analyser")
d=dirs('.')
for i in range(0,len(d)): print ('('+str(i)+')',d[i]) 
while True:
             try:
                s=input('_->')
                w=d[int(s)]
             except Exception as e:
                 continue
             break
t= glob.glob(w+'/*.fb2')  
print("loaded :",len(t))
charcnt=0
for e in t:
    text = ET.fromstring(codecs.open(e, 'r',encoding='utf8').read())
    for i in range(0,2**16):
        try:
            if not "binary" in text[i].tag:
                charcnt=charcnt+len(ET.tostring(text[1], encoding='utf8', method='text').decode('utf-8'))
        except Exception:
            break
print("total :",round(charcnt/STD_LIST_CHARS),"pages")
input()
    


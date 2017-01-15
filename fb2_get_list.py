import os,glob,re,codecs,sys

def dirs(d):
    return next(os.walk(d))[1]

def sty(_str,begin,end):
    start = _str.find(begin)
    stop = _str.find(end)
    if start != -1 and stop != -1:
        return _str[start+len(begin):stop]
    else:
        return ""
    
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
i=0
for e in t:
 i +=1
 print(str(i)+". ", end="")
 try:
     text = codecs.open(e, 'r',encoding='utf8').read()
     print(sty(text,"<book-title>","</book-title>")+" - ",sty(text,"<first-name>","</first-name>"),sty(text,"<middle-name>","</middle-name>"),sty(text,"<last-name>","</last-name>"))
 except Exception:
     print(e)


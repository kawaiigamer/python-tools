import os,glob

def dirs(d):
    return next(os.walk(d))[1]

def dirc(d):
    return len([f for f in os.listdir(d)if os.path.isfile(os.path.join(d, f))])

print("ckdir v1.0")
d=dirs('.')
for i in range(0,len(d)): print ('('+str(i)+')',d[i]) 
while True:
             try:
                s=input('_->')
                w=d[int(s)]
             except Exception as e:
                 continue
             break
t=dirs(w)
print("folders with file count < 15 :")
for vol in t:
    files = dirc(w+'/'+vol)
    if  files < 15:
        print('|',vol,' -> ',files)
input("press Enter to continue...")

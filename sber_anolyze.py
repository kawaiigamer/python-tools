import re

PLUS_REGEX = "SBOL.+?([\d+]+).00CR"
MINUS_REGEX = "QIWI WALLET.+?([\d+]+).[\d+]+$"

def sber_anolyze(file,regex,start_at,stop_at,minv,maxv):
    numbers = []
    data = [line.strip() for line in open(file, 'r')]
    if stop_at is 0:
        stop_at = len(data)
    for l in data[start_at:stop_at]:
        r = re.search(regex, l) 
        if r:
            numbers.append( int (r.group(1)) )
    numbers = [x for x in numbers if x > minv and x < maxv]
    print (numbers)      
    print ("\nSUM: ", end="")
    print (  sum (numbers ))
    return numbers


sber_anolyze("15081_Jan19.txt",PLUS_REGEX,0,0,500,2**32)
sber_anolyze("15081_Jan19.txt",MINUS_REGEX,0,0,500,2**32)
input()

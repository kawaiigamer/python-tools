import urllib.request,re

def RemoteContentHttpDownload(s):
 return str(urllib.request.urlopen( s,timeout = 10).read())

def ParseCharAll(s,w): # "https://vndb.org/i296?m=0;fil=tagspoil-0.trait_inc-296;p="
    Links = []
    for i in range(1,w):
        h=RemoteContentHttpDownload(s + str(i))
        Links += re.findall("tc2\"><a href=\"(.+?)\" title=\".+?\">(.+?)<\/a><b",h)
    return Links

def GetCharDetal(arr): 
     New = []
     for i in range(len(arr)):
         h=RemoteContentHttpDownload("https://vndb.org" + arr[i][0])
         m = re.search("(\/v\d+\/chars)", h).group(1)
         try:
             d = "https://" + re.search("rc=\"//(.+?)\" a", h).group(1)
         except:
             d = ""
         New.append(   (arr[i][0],arr[i][1],m,d)  )
     return New

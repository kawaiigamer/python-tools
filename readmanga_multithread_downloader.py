from concurrent.futures import ThreadPoolExecutor
from time import gmtime, strftime
import os,sys,urllib.request,re,socket,time

def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def get_time():
      return "[".append(strftime("%Y-%m-%d %H:%M:%S", gmtime())).append("] ")
    
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]

def RemoteContentHttpDownload(s):
 return urllib.request.urlopen( s,timeout = 10).read()

def input_check(ar,s,d,m):
     if len(sys.argv) > ar :
         return int(sys.argv[ar])
     else:
         _ = input(s + " ->(" + str(d) + ") ")
         return int(_) if len(_) > 0 and int(_) > 0 and int(_) < m else d

def remove_url_augruments(u): 
    l = u.find("?")
    return u[:l] if not l == -1 else u


def ConcurrentMangaChapterDownload(task):
    _ = task.split("/" )
    _ = _manga_name + "\\" +(_[len(_)-2]+"_"+_[len(_)-1])
    os.makedirs(_,exist_ok=True)
    d=_url_base + task + "?mature=1"
    while True:
             try:
                 raw = str(RemoteContentHttpDownload(d))
             except Exception as e:
                 print (get_time(),_,str(e),d)
                 continue
             break
    ImgLinks = re.findall("\'(.+?)'..(.+?)'.\"(.+?)\"",raw[raw.index('.init'):][:5500])
    for i in range(len(ImgLinks)):
        url  = ImgLinks[i][1] + ImgLinks[i][0] + ImgLinks[i][2]
        while True:
             try:
                 image_url = url[1:].replace("\\","")
                 image_save_path = remove_url_augruments(_ + "\\" + url.split('/')[-1])
                 urllib.request.urlretrieve(image_url, image_save_path)
             except Exception as e:
                 print (get_time(),_,str(e), url[1:].replace("\\",""))
                 continue
             break
    downloaded_size.append(get_size(_))

# -- Main
downloaded_size = []
socket.setdefaulttimeout(30)

# -- Vars
_url = sys.argv[1] if len(sys.argv) > 1  else  input("url -> ") # "http://readmanga.me/bleach_"
_url_base = _url[:_url.rindex('/')] # http://readmanga.me
_manga_name = remove_url_augruments(_url[_url.rindex('/'):]) # bleach_

    
# -- Chapters catalog
rawCatalog = RemoteContentHttpDownload(_url)
print("downloaded:",len(rawCatalog),"bytes")
chapterList = list(set(re.compile("<a href=\"(" + _manga_name + "/vol\d+/\d+)", re.M).findall(str(rawCatalog))))
chapterList.sort(key=natural_keys)
_manga_name = _manga_name[1:] # remove slash at start
print("found:",len(chapterList),"chapters")

# -- Input
_from = input_check(2,"start from",0,len(chapterList))
_to = input_check(3,"stop at",len(chapterList),len(chapterList))
_threads = input_check(4,"threads",10,1000)
os.makedirs(_manga_name,exist_ok=True)
print("creating new folder :",_manga_name)

# -- Downloading
start = time.time()
with ThreadPoolExecutor(max_workers=_threads) as executor:
    i = _from
    while i < _to:
        executor.submit(ConcurrentMangaChapterDownload, chapterList[i])
        i += 1
    executor.shutdown()

# -- Final
size = round(sum(downloaded_size)/1048576,3)
rtime = int(time.time() - start)
print(size,"MB downloaded from",rtime,"seconds",round(size/rtime,3),"MB per second")
if len(sys.argv) == 1:
    input("press Enter to continue...")

import shutil
import os.path
from os import path
import fileinput
import threading

def convert(item, color):
    if ".png" in item:
        os.system("convert " + item  + " -colorspace Gray -fill \"rgb" + color + "\" -tint 100 " + "-set filename:basename \"%[basename]\" \"%[filename:basename].png\"")
    else:
        os.system("convert " + item  + " -colorspace Gray -fill \"rgb" + color + "\" -tint 100 " + "-set filename:basename \"%[basename]\" \"%[filename:basename].jpg\"")
    return
    
def skinini(path):
    f=open("/home/abrahamr/.cache/wal/colors")
    lines=f.readlines()
    strings = []

    for x in range(1,len(lines)):
        h = (lines[x]).lstrip('#')
        rgb = tuple(int(h[i:i+2], 16) for i in (0,2,4)) 
        strings.append(((str(rgb)).lstrip('('))[:-1])

    for i in range(1,len(strings)):
        if os.path.exists(path + "Skin.ini"):
            x = fileinput.input(files= path + "Skin.ini", inplace=1)
        else:
            x = fileinput.input(files=path + "skin.ini", inplace=1)
        text = "Combo" + str(i) + ":"
        for line in x:
            if text in line:
                line = "Combo" + str(i) + ": " + strings[i-1]  
            print ((line).strip())
        x.close()
    return

f=open("/home/abrahamr/.cache/wal/colors")
lines=f.readlines()

h = (lines[1]).lstrip('#')
rgb1 = tuple(int(h[i:i+2], 16) for i in (0,2,4))

#Variable creation
path = '/home/abrahamr/Desktop/osu!/Skins/BubbleGum/'
newpath = "/home/abrahamr/Desktop/osu!/Skins/done/"
images,judges,rest,judgepath,restpath,threads = [],[],[],[],[],[]

for root, directories, files in os.walk(path, topdown=True):
    for name in files:
        #if "2x" in name: used to only process 2x images.
            if ".jpg" in name:
                images.append(os.path.join(root, name))
            if ".png" in name:
                if "hit" not in name:
                    images.append(os.path.join(root, name))
                if "circle" in name:
                    rest.append(os.path.join(root, name))
                    restpath.append(newpath + name)
                elif "hit" in name:
                    if "circle" not in name:
                        judges.append(os.path.join(root, name))
                        judgepath.append(newpath + name)
            else:
                rest.append(os.path.join(root, name))
                restpath.append(newpath + name)

os.chdir(newpath)
for item in images:
    t = threading.Thread(target=convert,args=(item,str(rgb1)))
    threads.append(t)
    t.start()

for n in range(0,len(judges)):
    if (os.path.isfile(judgepath[n])) != 1:
        shutil.copyfile(judges[n], judgepath[n])
    
for n in range(0,len(rest)):
    if (os.path.isfile(restpath[n])) != 1:
        shutil.copyfile(rest[n], restpath[n])

skinini(newpath)



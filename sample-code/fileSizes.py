import os

totalSize = 0
for filename in os.listdir('C:\\Files'): #will include folders
    if not os.path.isfile(os.path.join(os.path.join('c:\\Files', filename))): #if filename is not a file (is a folder)
        continue
    totalSize = totalSize + os.path.getsize(os.path.join('c:\\Files', filename)) #add the size of the file

print(totalSize) #displayed in bytes

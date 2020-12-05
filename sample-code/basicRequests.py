import requests

res = requests.get('https://automatetheboringstuff.com/files/rj.txt')
res.status_code #prints status code, 200 is good
print(len(res.text)) #text length of page
#print(res.text[:500]) #prints some text
res.raise_for_status #will error if bad request, like 404, could try/except if utilized to quit out
playFile = open('RomeoAndJuliet.txt', 'wb') #must open as write-binary mode instead of just write to preserve unicode, all web pages
for chunk in res.iter_content(100000): #returns chunks in bytes
    playFile.write(chunk)
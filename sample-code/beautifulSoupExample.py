import bs4 #import beautiful soup 4 library
import requests #import requests library

#prepare web request
URL = "https://pypi.org/project/beautifulsoup4/"
agent = {"User-Agent":"Defined"} #tells the page who's asking
#google for your agent in other browsers, can be used to spoof

#make the connection
res = requests.get(URL, headers=agent) 
res.raise_for_status() #make sure connection was successful
print(res.status_code) #optional printout of above - 200 is OK

#soup fuckery goes here
soup = bs4.BeautifulSoup(res.text, 'html.parser') #second argument tells it ok to parse html
text = soup.select("#description > div > h1:nth-child(2)")
print(text[0].text)
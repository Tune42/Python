import requests

def getUsers(url):
  r = requests.get(url)
  events = r.json()
  length = len(events)
  x=1
  while x < length:
    actor = events[x].get("actor")
    print(actor.get("login"))
    x += 1

# getUsers("https://api.github.com/events")


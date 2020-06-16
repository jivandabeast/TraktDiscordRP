from urllib.request import urlopen, Request
from pypresence import Presence
import time
import json
import credentials

headers = {
  'Content-Type': 'application/json',
  'trakt-api-version': '2',
  'trakt-api-key': credentials.traktclientid
}

RPC = Presence(credentials.discordclientid)
RPC.connect()
# RPC.close()

def updateRPC(state, details, starttime, endtime):
    RPC.update(state=state, details=details, start=starttime, end=endtime, large_image="trakt", small_image="trakt")

while True:
    request = Request('https://api.trakt.tv/users/jivandabeast/watching', headers=headers)
    response_body = urlopen(request).read()
    data = json.loads(response_body)

    if(data['type'] == 'episode'):
        print('The episode title is:', data['episode']['title'])
        print('The show is:', data['show']['title'])
        print('The TVDB ID is:', data['show']['ids']['tvdb'])
        newstate="Watching a Show."
    elif(data['type'] == 'movie'):
        print('The name of the movie is:', data['movie']['title'])
        print('The TMDB ID is:', data['movie']['ids']['tmdb'])
        newstate="Watching a Movie"
    else:
        print('Ya fucked bud')
    time.sleep(15)

#!/usr/bin/env python3
from urllib.request import urlopen, Request
from pypresence import Presence
import dateutil.parser as dp
import pytz
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
gmt = pytz.timezone('GMT')
est = pytz.timezone('US/Eastern')

def updateRPC(state, details, starttime, endtime, media):
    if media == 'tv':
        large = "tv"
    elif media == 'movie':
        large = "movie"
    else:
        print('media type error')
    RPC.update(state=state, details=details, start=starttime, end=endtime, large_image=large, small_image="trakt")

while True:
    try:
        request = Request('https://api.trakt.tv/users/jivandabeast/watching', headers=headers)
        response_body = urlopen(request).read()
    except:
        print("Error trying to process API request")
    try:
        data = json.loads(response_body)
        if(data['type'] == 'episode'):
            print('The episode title is:', data['episode']['title'])
            print('The show is:', data['show']['title'])
            print('The IMDB ID is:', data['show']['ids']['imdb'])
            newdetails=data['show']['title']
            newstate=data['episode']['title']
#            newstate='https://www.imdb.com/title/' + data['show']['ids']['imdb']
            media='tv'
        elif(data['type'] == 'movie'):
            print('The name of the movie is:', data['movie']['title'])
            print('The IMDB ID is:', data['movie']['ids']['imdb'])
            newdetails=data['movie']['title']
            newstate='https://www.imdb.com/title/' + data['movie']['ids']['imdb']
            media='movie'
        else:
            print('Ya fucked bud')
        starttime = data['started_at']
        starttime = dp.parse(starttime)
        starttime = starttime.astimezone(est)
        starttime = starttime.strftime('%s')
        endtime = data['expires_at']
        endtime = dp.parse(endtime)
        endtime = endtime.astimezone(est)
        endtime = endtime.strftime('%s')
        print(starttime, endtime)
        updateRPC(newstate, newdetails, starttime, endtime, media)
    except:
        print('Nothing is being played')
        RPC.clear()
    time.sleep(15)

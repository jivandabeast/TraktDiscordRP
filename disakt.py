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
    RPC.update(state=state, details=details, start=starttime, end=endtime, large_image=media, small_image="trakt")

def extractData(data):
    if(data['type'] == 'episode'):
        print('Watching', data['show']['title'], 'episode ', data['episode']['title'])
        details=data['show']['title']
        state='S' + str(data['episode']['season']) + 'E' + str(data['episode']['number']) + ' - ' + str(data['episode']['title'])
        media='tv'
    elif(data['type'] == 'movie'):
        print('Watching', data['movie']['title'])
        details=data['movie']['title']
        state='https://www.imdb.com/title/' + data['movie']['ids']['imdb']
        media='movie'
    else:
        print('Error determining media type')
    
    start = dp.parse(data['started_at']).astimezone(est).timestamp()
    end = dp.parse(data['expires_at']).astimezone(est).timestamp()

    return details, state, media, start, end

status = 0
while True:
    try:
        request = Request('https://api.trakt.tv/users/' + credentials.traktusername + '/watching', headers=headers)
        response_body = urlopen(request).read()
        try:
            if response_body == b'':
                if status == 1:
                    print('Nothing is being played')
                    RPC.clear()
                    status = 0
                else:
                    pass
            else:
                data = json.loads(response_body)
                try:
                    details, state, media, start, end = extractData(data)
                    updateRPC(state, details, start, end, media)
                    status = 1
                except Exception as e:
                    print('Error updating status ', e)
                
        except Exception as e:
            print('Error processing data: ', e)
            print('Response Body: ')
            print(response_body)
            status = 1

    except Exception as e:
        print("Error trying to process API request", e)
        status = 1
    
    time.sleep(60)

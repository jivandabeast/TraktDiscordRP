#!/usr/bin/env python3
from urllib.request import urlopen, Request
from pypresence import Presence, InvalidID
import dateutil.parser as dp
import pytz
import time
import json
import credentials

def connectRPC():
    RPC = Presence(credentials.discordclientid)
    RPC.connect()
    return RPC

def updateRPC(state, details, starttime, endtime, media, links):
    RPC.update(state=state, details=details, start=starttime, end=endtime, large_image=media, small_image="trakt", buttons=links)

def getMovieRating(slug):
    try:
        request = Request('https://api.trakt.tv/movies/' + str(slug) + '?extended=full', headers=headers)
        response_body = urlopen(request).read()
        return json.loads(response_body)['rating']
    except Exception as e:
        print('Could not retrieve movie rating, ' + e)
        return ('Not Found')

def extractData(data):
    if(data['type'] == 'episode'):
        print('Watching', data['show']['title'], 'episode ', data['episode']['title'])
        details=data['show']['title']
        state='S' + str(data['episode']['season']) + 'E' + str(data['episode']['number']) + ' - ' + str(data['episode']['title'])
        link='https://www.imdb.com/title/' + data['show']['ids']['imdb']
        media='tv'
    elif(data['type'] == 'movie'):
        print('Watching', data['movie']['title'])
        details=data['movie']['title']
        link='https://www.imdb.com/title/' + data['movie']['ids']['imdb']
        state='Rating: ' + str(round(getMovieRating(data['movie']['ids']['slug']), 2)) + '/10'
        media='movie'
    else:
        print('Error determining media type')
    
    start = dp.parse(data['started_at']).astimezone(est).timestamp()
    end = dp.parse(data['expires_at']).astimezone(est).timestamp()

    return details, state, media, start, end, link

headers = {
  'Content-Type': 'application/json',
  'trakt-api-version': '2',
  'trakt-api-key': credentials.traktclientid
}

RPC = connectRPC()
gmt = pytz.timezone('GMT')
est = pytz.timezone('US/Eastern')

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
                    details, state, media, start, end, link = extractData(data)
                    links = [{'label': 'IMDB', 'url': link}]
                    updateRPC(state, details, start, end, media, links)
                    status = 1
                except InvalidID:
                    print('Invalid ClientID ... reconnecting')
                    RPC = connectRPC()
                except Exception as e:
                    template = "Error updating status. An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(e).__name__, e.args)
                    print(message)
                
        except Exception as e:
            print('Error processing data: ', e)
            print('Response Body: ')
            print(response_body)
            status = 1

    except Exception as e:
        print("Error trying to process API request", e)
        status = 1
    
    time.sleep(60)
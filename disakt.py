from urllib.request import urlopen, Request
import json
import credentials

clientID=credentials.clientid

headers = {
  'Content-Type': 'application/json',
  'trakt-api-version': '2',
  'trakt-api-key': clientID
}
request = Request('https://api.trakt.tv/users/jivandabeast/watching', headers=headers)
response_body = urlopen(request).read()


data = json.loads(response_body)
print(data)
print()
print('The content type is:', data['type'])
print('The episode title is:', data['episode']['title'])
print('The show is:', data['show']['title'])

import requests
import json
import os
from random import randint, random
from threading import * 

token = ''

if not os.path.exists('response'): os.mkdir('response')
if not os.path.exists('response/atts'): os.mkdir('response/atts')

def dwnldAtts(id, message_id, url):
    try:
        if not os.path.exists(f'response/atts/{id}'): os.mkdir(f'response/atts/{id}')
        img_data = requests.get(url).content
        with open(f'response/atts/{id}/{message_id}.jpg', 'wb') as handler:    
            handler.write(img_data)
    except Exception as e:
        print(e)

lastPeers = requests.get(f'https://api.vk.com/method/messages.getConversations?access_token={token}&v=5.131')
for i in json.loads(lastPeers.text)['response']['items']:
    if i['conversation']['peer']['type'] == 'user':
        peerHistory = requests.get(f'https://api.vk.com/method/messages.getHistory?count=200&user_id={str(i["conversation"]["peer"]["id"])}&access_token={token}&v=5.131')
        for i_ in json.loads(peerHistory.text)['response']['items']:
            open('./response/' + str(i["conversation"]["peer"]["id"]) + '.txt', 'a', encoding='utf-8').write((str(i_['from_id']) + ': ' + i_['text']) + '\n')

        historyAtts = requests.get(f'https://api.vk.com/method/messages.getHistoryAttachments?count=200&peer_id={str(i["conversation"]["peer"]["id"])}&media_type=photo&access_token={token}&v=5.131')
        for photo in json.loads(historyAtts.text)['response']['items']:
            try:
                Thread(target=dwnldAtts, args=(str(i["conversation"]["peer"]["id"]), photo['message_id'], photo['attachment']['photo']['sizes'][2]['url'],)).start()
            except:
                Thread(target=dwnldAtts, args=(str(i["conversation"]["peer"]["id"]), photo['message_id'], photo['attachment']['photo']['sizes'][1]['url'],)).start()

savePhotos = requests.get(f'https://api.vk.com/method/photos.getAll?count=200&access_token={token}&v=5.131')
for i in json.loads(savePhotos.text)['response']['items']:
    Thread(target=dwnldAtts, args=(str(i['owner_id']) + '_saves', str(randint(1000, 1000000)), i['sizes'][3]['url'],)).start()

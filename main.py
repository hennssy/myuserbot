import requests
import json
import keep_alive
import config
import functions
from commands import *
from replit import db

while True:
  res = requests.post(f'{config.url}?act=a_check&key={db["key"]}&ts={db["ts"]}&wait=25&mode=2&version=3').json()
  print(res)

  if 'failed' in res:
    error_code = res['failed']
    
    if error_code == 1:
      db['ts'] = res['ts']
      
    if error_code == 2:
      key_res = requests.post(f'{config.api_url}messages.getLongPollServer?access_token={config.token}&lp_version=3&v=5.131').json()
      db['key'] = key_res['response']['key']
      continue
    
  try:
    updates = res['updates']
  except:
  	continue
    
  for update in updates:
    print(update)
    code = update[0]
      
    if code == 4:
      flags = functions.get_flags(update[2])
	                  
      if 2 in flags:
        message_text = update[5]

        try:
          if message_text.split()[0] != '.к':
            break
        except:
          pass

        try:
          command = message_text.split()[1]
          message_id = update[1]
          peer_id = update[3]
        except:
          continue
        
        if command == 'ку':
          functions.edit_message([peer_id, message_id, 'привет, зайка'])

        if command == 'инфо':
          Info.get_info(update, [peer_id, message_id, message_text])

        if command == 'стики':
          Stickers.get_sticks(update, [peer_id, message_id, message_text])
          
  db['ts'] = res['ts']
  keep_alive.keep_alive()

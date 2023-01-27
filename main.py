import requests
import keep_alive
import config
import functions
from threading import Thread
from commands import *
from replit import db

def main(updates):
    for update in updates:
      code = update[0]
        
      if code == 4:
        print(update)
        flags = functions.get_flags(update[2])
        message_text = update[5]
        message_id = update[1]
        from_id = None
        peer_id = None
        
        try:
          if message_text.split()[0] != '.к':
            continue
        except:
          pass
          
        try:
          peer_id = int(update[3])
          
          if peer_id > 2000000000:
            from_id = int(update[6]['from'])
            
            if str(from_id) not in db['allowed'] and from_id != 480656577:
              continue
          else:
            if 2 not in flags:
              from_id = peer_id
            else:
              from_id = 480656577
        except:
          pass

        if from_id != None:
          try:
            command = message_text.split()[1]
          except:
            continue

          if command == '+доступ':
            if from_id == 480656577:
              try:
                id = message_text.split()[2]
              except:
                functions.edit_message([peer_id, message_id, 'Введите ID!'])
                continue

              Access.cmd(id, '+', [peer_id, message_id])

          elif command == '-доступ':
            if from_id == 480656577:
              try:
                id = message_text.split()[2]
              except:
                functions.edit_message([peer_id, message_id, 'Введите ID!'])
                continue

              Access.cmd(id, '-', [peer_id, message_id])
                
          elif command == 'ку':
            if from_id == 480656577:
              functions.edit_message([peer_id, message_id, 'привет, зайка'])
            else:
              functions.send_message([peer_id, 'привет, зайка'])

          elif command == 'инфо':
            Info.get_info(update, [peer_id, message_id, message_text, from_id])

          elif command == 'стики':
            Stickers.get_sticks(update, [peer_id, message_id, message_text, from_id])

while True:
  res = requests.post(f'{config.url}?act=a_check&key={db["key"]}&ts={db["ts"]}&wait=25&mode=2&version=3').json()

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
  
  if len(updates) == 0:
    db['ts'] = res['ts']
    keep_alive.keep_alive()
    continue
  
  multiprocess = Thread(target = main, args = (updates, ))
  multiprocess.start()
          
  db['ts'] = res['ts']
  keep_alive.keep_alive()

import functions
import config
import requests
import json

def get_info(update, args): 
  try:
    info_id = args[2].split()[2]
  except:
    try:
      info_id = requests.post(f'{config.api_url}/messages.getByConversationMessageId?access_token={config.token}&peer_id={args[0]}&conversation_message_ids={json.loads(update[7]["reply"])["conversation_message_id"]}&v=5.131').json()['response']['items'][0]['from_id']
    except:
      info_id = requests.post(f'{config.api_url}/messages.getById?access_token={config.token}&message_ids={args[1]}&v=5.131').json()['response']['items'][0]['from_id']
  
  if '@' in str(info_id):
    info_id = info_id.split('|')[1].replace('@', '').replace(']', '')

  info_result = requests.post(f'{config.api_url}/users.get?access_token={config.token}&user_ids={info_id}&fields=counters,screen_name,sex&v=5.131').json()
  text = ''
  
  try:
    if info_result['response'][0]['is_closed'] == False:
      profile_status = 'открыт'
    elif info_result['response'][0]['is_closed'] == True:
      profile_status = 'закрыт'

    if info_result['response'][0]['sex'] == 1:
      sex = 'женский'
    elif info_result['response'][0]['sex'] == 2:
      sex = 'мужской'
    elif info_result['response'][0]['sex'] == 0:
      sex = 'не указан'
    
    text += f'Информация о пользователе {info_result["response"][0]["first_name"]} {info_result["response"][0]["last_name"]}:\n' \
    f'- Идентификатор: {info_result["response"][0]["id"]}\n' \
    f'- Короткое имя: @{info_result["response"][0]["screen_name"]}\n' \
    f'- Пол: {sex}\n' \
    f'- Профиль: {profile_status}'
    
    if profile_status == 'открыт':
      text += f'\n- Друзей: {info_result["response"][0]["counters"]["friends"]}\n' \
      f'- Подписчиков: {info_result["response"][0]["counters"]["followers"]}'

    if args[3] == 480656577:
      functions.edit_message([args[0], args[1], text])
    else:
      functions.send_message([args[0], text])
  except:
    if args[3] == 480656577:
      functions.edit_message([args[0], args[1], 'Неверный ID!'])
    else:
      functions.send_message([args[0], 'Неверный ID!'])

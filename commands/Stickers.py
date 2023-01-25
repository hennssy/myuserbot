import config
import functions
import json
import requests

def get_sticks(update, args):
  try:
    stick_id = args[2].split()[2]
  except:
    try:
      stick_id = requests.post(f'{config.api_url}/messages.getByConversationMessageId?access_token={config.token}&peer_id={args[0]}&conversation_message_ids={json.loads(update[7]["reply"])["conversation_message_id"]}&v=5.131').json()['response']['items'][0]['from_id']
    except:
      stick_id = requests.post(f'{config.api_url}/messages.getById?access_token={config.token}&message_ids={args[1]}&v=5.131').json()['response']['items'][0]['from_id']
            
  if '@' in str(stick_id):
    stick_id = stick_id.split('|')[1].replace('@', '').replace(']', '')
            
  response = requests.get(f'https://stickers.loupg.one/user/{stick_id}', headers=config.headers).json()
  
  try:
    text = ''
    name = response["user"]["name"]
    all_count = len(response["all"]["items"]) + len(response["all"]["styles"]["items"])
    sticks = all_count - len(response["all"]["styles"]["items"])
    paid_sticks = len(response["paid"]["items"])
    free_sticks = sticks - paid_sticks
    styles = all_count - sticks
    paid_styles = len(response["paid"]["styles"]["items"])
    free_styles = styles - paid_styles
    rubles_cost = response["paid"]["price"] + response["paid"]["styles"]["price"]
    text += f'{name} имеет всего {functions.pluralForm(all_count, ["стикерпак", "стикерпака", "стикерпаков"])}, из них:\n' \
    f'- {functions.pluralForm(sticks, ["стикерпак", "стикерпака", "стикерпаков"])}\n' \
    f'ㅤ- {functions.pluralForm(paid_sticks, ["платный", "платных", "платных"])}\n' \
    f'ㅤ- {functions.pluralForm(free_sticks, ["бесплатный", "бесплатных", "бесплатных"])}\n' \
    f'- {functions.pluralForm(styles, ["стиль", "стиля", "стилей"])}\n' \
    f'ㅤ- {functions.pluralForm(paid_styles, ["платный", "платных", "платных"])}\n' \
    f'ㅤ- {functions.pluralForm(free_styles, ["бесплатный", "бесплатных", "бесплатных"])}\n\n' \
    f'Общая стоимость (в голосах/в рублях): {int(rubles_cost/7)} / {rubles_cost} ₽'
  except:
    functions.edit_message([args[0], args[1], 'Неверный ID!'])
  
  functions.edit_message([args[0], args[1], text])

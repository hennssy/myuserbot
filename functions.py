import config
import requests
import random

def pluralForm(amount, variants):
  amount = abs(amount)

  if amount % 10 == 1 and amount % 100 != 11:
      variant = 0
  elif 2 <= amount % 10 <= 4 and (amount % 100 < 10 or amount % 100 >= 20):
    variant = 1
  else:
    variant = 2

  return f"{amount} {variants[variant]}"

def get_flags(flag):
  flags = []

  for number in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 65536]:
    if flag & number:
      flags.append(number)

  return flags

def edit_message(args):
  requests.post(f'{config.api_url}/messages.edit?access_token={config.token}&peer_id={args[0]}&message={args[2]}&message_id={args[1]}&keep_forward_messages=1&v=5.131')

def send_message(args):
  res = requests.post(f'{config.api_url}/messages.send?access_token={config.token}&random_id={random.randint(1, 10000)}&peer_id={args[0]}&message={args[1]}&v=5.131').json()

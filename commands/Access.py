import functions
from replit import db

def check_id(id):
  if id in db['allowed']:
    return True
  else:
    return False

def give_access(id, args):
  if not check_id(id):
    db['allowed'].append(id)
    functions.edit_message([args[0], args[1], 'Юзеру выдан доступ к боту!'])
  else:
    functions.edit_message([args[0], args[1], 'Юзер уже может пользоваться ботом!'])

def take_access(id, args):
  if check_id(id):
    db['allowed'].remove(id)
    functions.edit_message([args[0], args[1], 'Юзер лишился доступа к боту!'])
  else:
    functions.edit_message([args[0], args[1], 'Юзер и так не имеет доступа к боту!'])

def cmd(id, type, args):
  if type == '+':
    give_access(id, args)
  if type == '-':
    take_access(id, args)

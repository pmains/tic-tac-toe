'''
Controller functions to be mapped to URL patterns by urls entries
Each controller function should represent one url mapping
'''

import logic
from handle import *
import json

def choose_game(m):
  '''Choose game mode (e.g. 1 Player, 2 Player, 2 Player Remote)'''
  template = 'index.html'
  context = None
  return render_template_response(context, template)

def play_one(m):
  '''Play 1 Player Tic Tac Toe Game'''
  template = 'play_one.html'
  context = None  
  return render_template_response(context, template)

def play_two(m):
  '''Play 2 Player Tic Tac Toe Game'''
  template = 'play_two.html'
  context = None  
  return render_template_response(context, template)

def play_remote(m):
  '''Play a 2 Player Remote Game'''
  template = 'play_remote.html'
  context = None
  return render_template_response(context, template)

def check_winner(m, data):
  '''Check if the game has a winner'''
  grid = json.loads(data)
  response_body = json.dumps(logic.check_winner(grid))
  return response(OK, JSON, response_body)

def find_best_move(m, data):
  '''Find the best possible move given the current board state'''
  marker = m.group("marker")
  grid = json.loads(data)
  response_body = json.dumps(logic.find_best_move(grid, marker))
  return response(OK, JSON, response_body)

def is_alive(m):
  '''Return True if server is running''' 
  response_body = json.dumps(True)  
  return response(OK, JSON, response_body)

# Players API
def add_player(m):
  '''Add new player to list of available players'''
  player = m.group("player")
  status = OK
  result = logic.add_player(player)
  if not result:
    status = CONFLICT
  response_body = json.dumps(result)
  
  return response(status, JSON, response_body)

def remove_player(m):
  '''Remove player from list of available players'''
  player = m.group("player")
  response_body = json.dumps(logic.delete_player(player))
  return response(OK, JSON, response_body)
  
def get_players(m):
  '''Find all current player sessions'''
  response_body = json.dumps(logic.get_players())
  return response(OK, JSON, response_body)
  
def flush_players(m):
  '''Terminate all player sessions'''
  response_body = json.dumps(logic.flush_players())
  return response(OK, JSON, response_body)

def find_opponents(m):
  '''Find opponents looking to start games'''
  status = OK
  player = m.group("player")
  result = logic.find_opponents(player)
  if not result:
    status = ERROR
  response_body = json.dumps(result)
  
  return response(status, JSON, response_body)

# Games API
def start_game(m):
  '''Given two player names, start a new game of Tic Tac Toe'''  
  player1 = m.group("player1")
  player2 = m.group("player2")
  
  result = logic.start_game(player1, player2)
  
  status = OK
  if not result:
    status = ERROR
  
  response_body = json.dumps(result)
  return response(status, JSON, response_body)

def end_game(m):
  '''Terminate a game'''
  game_is = m.group("game_id")
  
  status = OK
  result = logic.end_game(game_id)
  if not result:
    status = ERROR
  
  response_body = json.dumps(result)  
  return response(status, JSON, response_body)

def save_game(m, data):
  '''Save the board and game status'''
  game_id = m.group("game_id")
  player = m.group("player")
  print "data: %s " % data
  result = logic.save_game(game_id, player, json.loads(data))

  status = OK
  if not result:
    status = ERROR

  response_body = json.dumps(result)
  return response(status, JSON, response_body)

def get_game(m):
  '''Find existing games of Tic Tac Toe'''
  game_id = m.group("game_id")
  response_body = json.dumps(logic.get_game(game_id))
  return response(OK, JSON, response_body)

def get_games(m):
  '''Find existing games of Tic Tac Toe'''
  response_body = json.dumps(logic.get_games())
  return response(OK, JSON, response_body)

def my_turn(m):
  '''Determine if it is the current player's turn'''
  game_id = m.group("game_id")
  player = m.group("player")
  response_body = json.dumps(logic.my_turn(game_id, player))
  return response(OK, JSON, response_body)
  
def find_game(m):
  '''Given a player name, find an existing game of Tic Tac Toe'''
  player = m.group("player")
  response_body = json.dumps(logic.find_game(player))
  return response(OK, JSON, response_body)

def flush_games(m):
  response_body = json.dumps(logic.flush_games())
  return response(OK, JSON, response_body)

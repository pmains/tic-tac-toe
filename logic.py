'''
Contains business logic for the application.
Allows the functions to be used by multiple controllers
e.g. both HTML pages and REST services
'''

from copy import deepcopy
import json
import settings
import uuid
import os

PLAYERS_FILE = settings.HOME_DIR + "players.json"
PLAYERS_FILE_LOCKED = False

GAMES_FILE = settings.HOME_DIR + "games.json"
GAMES_FILE_LOCKED = False

def lock_players():
  '''Lock the players file so no changes can be made'''
  PLAYERS_FILE_LOCKED = True

def unlock_players():
  '''Unlock the players file so additional changes may be made'''
  PLAYERS_FILE_LOCKED = False

def lock_games():
  '''Lock the games file so no changes can be made'''
  GAMES_FILE_LOCKED = True

def unlock_games():
  '''Unlock the games file so additional changes may be made'''
  GAMES_FILE_LOCKED = False

def start_game(player1, player2):
  # Call fails if other game or player data being written
  if GAMES_FILE_LOCKED or PLAYERS_FILE_LOCKED:
    print "files locked"
    return None
    
  # verify that players are available
  players = get_players()
  if player1 not in players or player2 not in players or \
    not players[player1]['available'] or not players[player2]['available']:
    return None

  # Lock files
  lock_games()
  lock_players()

  # Create new game and add to games
  game_id = str(uuid.uuid4())
  games = get_games()
  games[game_id] = {
    'player1': player1,
    'player2': player2
  }
  save_games(games)
  unlock_games()
  print "saved game %s" % game_id

  # Save server-side game file
  try:
    game = get_game_file(game_id, "w+")
    board = [ ["", "", ""], ["", "", ""], ["", "", ""] ]
    data = {
      "board": board,
      "turn": player1
    }
    game.write(json.dumps(data))
    game.close()
  except IOError:
    print "unable to save game %s" % game_id

  # Make players unavailable
  players = get_players()
  players[player1]['available'] = False
  players[player2]['available'] = False
  save_players(players)

  # Unlock files
  unlock_players()
  return game_id

def get_game_file(game_id, mode="r"):
  '''Open a game's file and return the file handle'''
  try:
    return open(settings.HOME_DIR + "game-%s.json" % game_id, mode)
  except IOError:
    raise
  return None

def get_game(game_id):
  '''Return the data contained in a game's file'''
  try:
    game = get_game_file(game_id, "r")
    game_data = json.loads(game.read())
  except IOError:
    game.close()
    return None
  
  game.close()
  return game_data

def save_game(game_id, player, board):
  '''Save game state'''
  # No lock is needed, since only one user can play at a time
  games = get_games() # Information about all current games

  # Do not let other players save the game status
  if games[game_id]['player1'] != player and games[game_id]['player2'] != player:
    return False
  
  game_data = get_game(game_id) # Data for current game
  game_data['board'] = board
  
  # Find whose turn is next by finding which player is not the current player
  opponent = games[game_id]['player1']
  if opponent == player:
    opponent = games[game_id]['player2']
  game_data['turn'] = opponent
  
  # Write the new game data to the game file
  try:
    game = get_game_file(game_id, "w")
    game.write( json.dumps(game_data) )
  except IOError:
    # Make sure that the game file is closed no matter what
    game.close()
    return False
  
  # Close the game file and report success
  game.close()
  return True

def my_turn(game_id, player):
  '''Determine if it is the given player's turn'''
  game = get_game(game_id)
  if game['turn'] == player:
    return True
  return False

def find_game(player):
  '''Find active game of which player is a member'''
  # Fetch only, so no data locks needed
  games = get_games()
  for game_id in games:
    if games[game_id]['player1'] == player or games[game_id]['player2'] == player:
      return { 'game_id': game_id, 'game': games[game_id] }
  return None

def end_game(game_id):
  # Call fails if other game or player data being written
  if GAMES_FILE_LOCKED or PLAYERS_FILE_LOCKED:
    return None
  
  lock_games()
  lock_players()

  # Delete game from games list
  games = get_games()
  player1 = games[game_id]['player1']
  player2 = games[game_id]['player2']
  del games[game_id]
  save_games(games)

  # Mark players are available
  players = get_players()
  players[player1]['available'] = True
  players[player2]['available'] = True
  save_players(players)
  
  unlock_games()
  unlock_players()
  return True

def get_games():
  '''Return all current games'''
  try:
    f = open(GAMES_FILE, "r")
    games = json.loads(f.read())
    f.close()
    return games
  except IOError:
    return None

def save_games(games):
  '''Save contents of dict passed to the games file'''
  try:
    games_json = json.dumps(games)
    f = open(GAMES_FILE, "w")
    f.write(games_json)
    f.close()
  except IOError:
    f.close()
    return None

  return True

def flush_games():
  '''Delete all existing games'''
  # find all games
  try:
    f = open(GAMES_FILE)
    games = json.loads(f.read())
    for game_id in games:
      game_file_name = "game-%s.json" % game_id
      if os.path.isfile(game_file_name):
        os.remove(game_file_name)
    f.close()
  except IOError:
    f.close()
    return False
  
  return save_games({})

def add_player(player):
  '''Add new player to the list of eligible players'''
  if PLAYERS_FILE_LOCKED:
    return None
  lock_players()

  players = get_players()
  result = False
  if player not in players:
    players[player] = {'available': True}
    result = save_players(players)

  unlock_players()
  return result

def delete_player(player):
  '''Delete a player from the list of eligible players'''
  if PLAYERS_FILE_LOCKED:
    return None
  lock_players()

  players = get_players()
  if player in players:
    del players[player]
  result = save_players(players)
  
  unlock_players()
  return result

def save_players(players):
  '''Save contents of dict passed to the players file'''
  try:
    players_json = json.dumps(players)
    f = open(PLAYERS_FILE, "w")
    f.write(players_json)
    f.close()
  except IOError:
    f.close()
    return None

  return True

def flush_players():
  '''Terminate all players sessions'''
  if PLAYERS_FILE_LOCKED:
    return None
  lock_players()
  result = save_players({})
  unlock_players()
  return result

def get_players():
  '''Return all current players'''
  try:
    f = open(PLAYERS_FILE, "r")
    players = json.loads(f.read())
    f.close()
    return players
  except IOError:
    return None

def find_opponents(player):
  '''Find all available players excluding the requesting player'''
  opponents = []
  
  try:
    f = open(PLAYERS_FILE)
    players = json.loads(f.read())
    
    for p in players:
      if p != player:
        opponents.append(p)
  except IOError:
    print "Cannot open"
  
  return opponents

def mark(grid, square, marker):
  '''Return copy of grid with square marked with marker'''
  x, y = square[0], square[1]
  dupe = deepcopy(grid) # deepcopy so that duplicate nested variables are copied
  dupe[x][y] = marker
  return dupe

def check_winner(grid):
  '''Given grid representing the game board, determine if there is a winner'''
  # Check rows
  for i in range(3):
    if( grid[i][0] != "" and grid[i][0] == grid[i][1] and grid[i][1] == grid[i][2] ):
      return grid[i][0]
  # Check columns
  for i in range(3):
    if( grid[0][i] != "" and grid[0][i] == grid[1][i] and grid[1][i] == grid[2][i] ):
      return grid[0][i]
  # Check diagonal
  if( grid[0][0] != "" and grid[0][0] == grid[1][1] and grid[1][1] == grid[2][2] ):
    return grid[0][0]
  if( grid[0][2] != "" and grid[0][2] == grid[1][1] and grid[1][1] == grid[2][0] ):
    return grid[0][2]

  return None

def find_opp_marker(marker):
  '''Given a marker (X or O), return the opponent's marker'''
  if marker == "O":
    return "X"
  return "O"

def find_empty_squares(grid):
  '''Find empty squares on the board'''
  empty_squares = []

  # Cycle through rows
  for x in range(3):
    # Cycle through columns
    for y in range(3):
      # If square is empty
      if grid[x][y] == "":
        # Add to list of empty squares
        empty_squares.append([x,y])
  
  return empty_squares

def find_kills(grid, marker, empty_squares=None):
  '''Find winning ("kill") moves'''
  if empty_squares is None:
    empty_squares = find_empty_squares(grid)
  
  kill_squares = []

  # Try moving to each empty square
  for square in empty_squares:
    dupe = mark(grid, square, marker)
    # Check if move is a "kill" move
    if check_winner(dupe) == marker:
      # Add to list of kill moves
      kill_squares.append(square)
  
  return kill_squares

def find_fork(grid, marker, empty_squares=None):
  '''
  Find moves that set up a fork. A fork is a game state where a player has two
  or more winning ("kill") moves.
  '''
  if empty_squares is None:
    empty_squares = find_empty_squares(grid)

  # look at two-step combinations that would create a fork
  for square in empty_squares:
    dupe = mark(grid, square, marker)
    
    # find possible kills
    kills = len(find_kills(dupe, marker))
    if kills >= 2: # if fork has been found
      return square
  
  return None

def find_diversion(grid, marker, empty_squares):
  '''Find move that will force the opponent to block.'''
  if empty_squares is None:
    empty_squares = find_empty_squares(grid)
  
  opp_marker = find_opp_marker(marker)

  for square in empty_squares:
    dupe = mark(grid, square, marker)
    # if move constitutes a force
    kills = find_kills(dupe,marker)
    if len(kills) > 0:
      for kill in kills:
        # verify that force is not a fork for the opponent
        opp_dupe = mark(dupe, kill, opp_marker)
        opp_kills = find_kills(opp_dupe, opp_marker)
        if len(opp_kills) < 2:
          return square
  
  return None

def find_best_move(grid, marker):
  '''Find the best possible move for the given player.'''
  empty_squares = find_empty_squares(grid)
  opp_marker = find_opp_marker(marker)
  len_empty_squares = len(empty_squares)

  # if no squares left, cat's game
  if len_empty_squares == 0:
    return None

  # if only one square left, take it
  if len_empty_squares == 1:
    print "only square"
    return empty_squares[0]

  # if empty board, take top left corner
  if len_empty_squares == 9:
    print "empty board"
    return [0,0]

  # if winning move available, take it
  kill_squares = find_kills(grid, marker)
  if len(kill_squares) > 0:
    print "kill"
    return kill_squares[0]
    
  # if losing move available, block it
  for square in empty_squares:
    dupe = mark(grid, square, opp_marker)
    if check_winner(dupe) == opp_marker:
      print "block"
      return square
  
  # if there is a fork possibility, take it
  square = find_fork(grid, marker, empty_squares)
  if square is not None:
    print "fork"
    return square
  
  # if opponent can create fork, block it
  square = find_fork(grid, opp_marker, empty_squares)
  if square is not None:
    diversion = find_diversion(grid, marker, empty_squares)
    if diversion is not None:
      print "divert fork"
      return diversion
    else:
      print "block fork"
      return square

  # if center available, take it
  if grid[1][1] == "":
    print "center"
    return [1,1]

  # if opponent has taken a corner,
  # and opposing corner is available, take it
  if grid[0][0] == opp_marker and grid[2][2] == "":
    print "opp corner"
    return [2,2]
  if grid[2][2] == opp_marker and grid[0][0] == "":
    print "opp corner"
    return [0,0]
  if grid[0][2] == opp_marker and grid[2][0] == "":
    print "opp corner"
    return [2,0]
  if grid[2][0] == opp_marker and grid[0][2] == "":
    print "opp corner"
    return [0,2]

  # check if any corner squares are available
  corner_squares = [[0,0],[0,2],[2,0],[2,2]]
  for square in corner_squares:
    if square in empty_squares:
      print "corner square"
      return square

  # if no other good option, take first available
  print "side square"
  return empty_squares[0]

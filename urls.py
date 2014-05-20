'''
Map URL patterns to controllers

Entries should be in the following format:
{ 'path': r'[URL pattern]',
  'controller': [controller function],
  'method': '[HTTP method in capital letters]'
}
'''
import controllers

# urls list contains urls entries
urls = [
  # Page view mappings
  { 'path': r'^/?$',
    'controller': controllers.choose_game,
    'method': 'GET'
  },
  { 'path': r'^/one/?$',
    'controller': controllers.play_one,
    'method': 'GET'
  },
  { 'path': r'^/two/?$',
    'controller': controllers.play_two,
    'method': 'GET'
  },
  { 'path': r'^/remote/?$',
    'controller': controllers.play_remote,
    'method': 'GET'
  },

  # Computer Player mappings
  {
    'path': r'^/check_winner/?$',
    'controller': controllers.check_winner,
    'method': 'PUT'
  },
  {
    'path': r'^/find_best_move/(?P<marker>\w)/?$',
    'controller': controllers.find_best_move,
    'method': 'PUT'
  },
  {
    'path': r'^/is_alive/?$',
    'controller': controllers.is_alive,
    'method': 'GET'
  },

  # Player API mappings
  {
    'path': r'^/player/?$',
    'controller': controllers.get_players,
    'method': 'GET'
  },
  {
    'path': r'^/player/(?P<player>\w+)/?$',
    'controller': controllers.add_player,
    'method': 'PUT'
  },
  {
    'path': r'^/add_player/(?P<player>\w+)/?$',
    'controller': controllers.add_player,
    'method': 'GET'
  },
  {
    'path': r'^/flush_players/?$',
    'controller': controllers.flush_players,
    'method': 'GET'
  },
  {
    'path': r'^/find_opponents/(?P<player>\w+)/?$',
    'controller': controllers.find_opponents,
    'method': 'GET'
  },

  # Game API mappings
  {
    'path': r'^/game/(?P<player1>\w+)/(?P<player2>\w+)/?$',
    'controller': controllers.start_game,
    'method': 'PUT'
  },
  {
    'path': r'^/game/(?P<player>\w+)/?$',
    'controller': controllers.find_game,
    'method': 'GET'
  },
  {
    'path': r'^/game/?$',
    'controller': controllers.get_games,
    'method': 'GET'
  },
  {
    'path': r'^/game/(?P<game_id>\w+)/?$',
    'controller': controllers.end_game,
    'method': 'DELETE'
  }
]
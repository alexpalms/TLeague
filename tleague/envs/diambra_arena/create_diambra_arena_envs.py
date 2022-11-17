import diambra.arena
from tleague.envs.diambra_arena.wrapper import TLeagueWrapper
import os

def create_diambra_arena_env(game_id):

  # Check if game id is present
  games_data = diambra.arena.available_games(print_out=False)
  game_ids = []
  for k, v in games_data.items():
    game_ids.append(v["id"])

  #assert game_id in game_ids
  # Only doapp for now
  assert game_id in ["doapp"]

  # Settings
  settings = {}
  settings["player"] = "P1P2"
  settings["step_ratio"] = 6
  settings["frame_shape"] = [128, 128, 1]
  settings["hardcore"] = False
  settings["characters"] = [["Random"], ["Random"]]
  settings["char_outfits"] = [2, 2]
  settings["action_space"] = "discrete"
  settings["attack_but_combination"] = False

  # Gym wrappers settings
  wrappers_settings = {}
  wrappers_settings["reward_normalization"] = True
  wrappers_settings["reward_normalization_factor"] = 0.5
  wrappers_settings["frame_stack"] = 4
  wrappers_settings["scale"] = True

  print("({}) Creating env".format(os.getpid()))
  env = diambra.arena.make(game_id, settings, wrappers_settings)
  print("({}) Env Created".format(os.getpid()))

  env = TLeagueWrapper(env, ["ownSide", "ownHealth", "oppHealth", "ownChar", "oppChar"])

  return env


def diambra_arena_env_space(game_id):
  env = create_diambra_arena_env(game_id)
  env.reset()
  ac_space = env.action_space.spaces[0]
  ob_space = env.observation_space.spaces[0]
  # TODO(pengsun): something wrong with .close()
  #env.close()
  return ob_space, ac_space
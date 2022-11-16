from tleague.envs.diambra_arena.create_diambra_arena_envs import create_diambra_arena_env
from tleague.utils.gym_space import assert_matched


def diambra_arena_2p_test():
  env = create_diambra_arena_env('doapp')
  obs = env.reset()
  print("Obs type = ", type(obs))
  print("obs stage = ", obs["stage"])
  print("Obs = ", obs)
  #assert_matched(env.observation_space, obs)
  for i in range(5000):
    act = env.action_space.sample()
    print("Action = ", act)
    #assert_matched(env.action_space, act)
    obs, rwd, done, info = env.step(act)
    print("Obs = ", obs)
    input("Press button")
    #assert_matched(env.observation_space, obs)
    print('step: {}, rwd: {}, done: {}'.format(i, rwd, done))
    if done:
      obs = env.reset()
      #assert_matched(env.observation_space, obs)


if __name__ == '__main__':
  diambra_arena_2p_test()
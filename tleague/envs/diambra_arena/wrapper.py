import gym
from gym import spaces
import numpy as np

# Convert ram states to additional observation channel and
# create multi agent style observation and action spaces
class TLeagueWrapper(gym.Wrapper):
    def __init__(self, env, key_to_add):
        gym.Wrapper.__init__(self, env)

        assert self.env.env_settings["player"] == "P1P2",\
               "TLeagueWrapper can only be used with 2P mode"
        assert self.env.env_settings["hardcore"] is False,\
               "TLeagueWrapper can only be used with hardcore mode off"

        shp = self.env.observation_space["frame"].shape
        self.key_to_add = key_to_add

        self.box_high_bound = self.env.observation_space["frame"].high.max()
        self.box_low_bound = self.env.observation_space["frame"].low.min()
        assert (self.box_high_bound == 1.0),\
               "Observation space max bound must be 1.0 to use Additional Obs"
        assert (self.box_low_bound == 0.0),\
               "Observation space min bound must be 0.0 to use Additional Obs"

        self.observation_space = spaces.Tuple([spaces.Box(low=self.box_low_bound, high=self.box_high_bound,
                                                         shape=(shp[0], shp[1], shp[2] + 1),
                                                         dtype=np.float32),
                                              spaces.Box(low=self.box_low_bound, high=self.box_high_bound,
                                                         shape=(shp[0], shp[1], shp[2] + 1),
                                                         dtype=np.float32)])
        self.action_space = spaces.Tuple([self.action_space["P1"], self.action_space["P2"]])

        keys_count = 0
        self.n_chars = len(self.env.char_names)
        for key in self.key_to_add:
            if "Char" in key:
                keys_count += self.n_chars
            else:
                keys_count += 1
        self.elems_per_key = int(shp[0] / keys_count)*shp[1]

    # Observation modification (adding one channel to store additional info)
    def process_obs(self, obs, player_side):

        # Adding a channel to the standard image, it will be in last position and
        # it will store additional obs
        shp = obs["frame"].shape
        obs_new = np.zeros((shp[0], shp[1], shp[2] + 1), dtype=self.observation_space[0].dtype)

        # Storing standard image in the first channel leaving the last one for
        # additional obs
        obs_new[:, :, 0:shp[2]] = obs["frame"]

        # Adding new info to the additional channel, on a very
        # long line and then reshaping into the obs dim
        new_data = np.zeros((shp[0] * shp[1]))

        # Adding new info
        idx = 0
        for key in self.key_to_add:
            if "Char" in key:
                for jdx in range(self.n_chars):
                    new_data[idx * self.elems_per_key:(idx + 1) * self.elems_per_key] = obs[player_side][key][jdx]
                    idx += 1
            else:
                new_data[idx * self.elems_per_key:(idx + 1) * self.elems_per_key] = obs[player_side][key]
                idx += 1

        new_data = np.reshape(new_data, (shp[0], -1))

        obs_new[:, :, shp[2]] = new_data

        return obs_new

    def two_player_obs(self, obs):

        return (self.process_obs(obs, "P1"), self.process_obs(obs, "P2"))

    def reset(self, **kwargs):

        obs = self.env.reset()

        return self.two_player_obs(obs)

    def step(self, action):
        obs, reward, done, info = self.env.step(np.append(action[0], action[1]))

        return self.two_player_obs(obs), (reward, -reward), done, info

    def show_ram_states_channel(self, obs):

        column_elems_per_key = int(self.elems_per_key / obs[0].shape[1])
        idx_end = obs[0].shape[0] - (obs[0].shape[0] % column_elems_per_key)

        for idx in range(2):
            print("P{} - RAM States in Channel:".format(idx+1))

            obs1 = np.reshape(obs[idx][0:idx_end, 0, -1], (int(idx_end / column_elems_per_key), -1))
            irow = 0
            for key in self.key_to_add:
                if "Char" in key:
                    for jdx in range(self.n_chars):
                        print("{} (One-hot | {}) - {}".format(key, self.env.char_names[jdx], obs1[irow, :]))
                        irow += 1
                else:
                    print("{} - {}".format(key, obs1[irow, :]))
                    irow += 1




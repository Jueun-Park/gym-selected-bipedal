from gym.envs.registration import register

register(
    id='selected-bipedal-grass-v0',
    entry_point='gym_selected_bipedal.env:SelectedStateBipedalWalker',
    kwargs={"selected_state": 0},
    max_episode_steps=2000,
    reward_threshold=300,
)

register(
    id='selected-bipedal-stump-v0',
    entry_point='gym_selected_bipedal.env:SelectedStateBipedalWalker',
    kwargs={"selected_state": 1},
    max_episode_steps=2000,
    reward_threshold=300,
)

register(
    id='selected-bipedal-stairs-v0',
    entry_point='gym_selected_bipedal.env:SelectedStateBipedalWalker',
    kwargs={"selected_state": 2},
    max_episode_steps=2000,
    reward_threshold=300,
)

register(
    id='selected-bipedal-pit-v0',
    entry_point='gym_selected_bipedal.env:SelectedStateBipedalWalker',
    kwargs={"selected_state": 3},
    max_episode_steps=2000,
    reward_threshold=300,
)

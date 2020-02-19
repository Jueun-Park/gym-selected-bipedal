# gym-selected-bipedal

From [`BipedalWalkerHardcore`](https://github.com/openai/gym/blob/master/gym/envs/box2d/bipedal_walker.py) env in openAI gym. Train an agent in the selected obstacle environment of bipedal walker hardcore. (really simple editing from original env)

## Usage

To setup the custom module, do

```sh
pip install -e gym_selected_bipedal/
```

(Using `virtualenv` or `miniconda` is recommended)

Then make `Env` object.

```python
import gym
import gym_selected_bipedal
env = gym.make("selected-bipedal-grass-v0")
```

Four selected obstacle environment are available. (grass is same to `BipedalWalker` env.)

```python
"selected-bipedal-grass-v0"
"selected-bipedal-stump-v0"
"selected-bipedal-stairs-v0"
"selected-bipedal-pit-v0"
```

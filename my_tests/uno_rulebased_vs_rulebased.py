# rule based against rule based

import rlcard
from rlcard import models

env = rlcard.make('uno')

crf_agent_1 = models.load('uno-rule-v1').agents[0]  # first rule based agent
crf_agent_2 = models.load('uno-rule-v1').agents[0]  # second rule based agent

# Set the agents
env.set_agents([
    crf_agent_1,
    crf_agent_2,
])


print(env.num_actions)  # 61
print(env.num_players)  # 2
print(env.state_shape)  # [[4, 4, 15], [4, 4, 15]]
print(env.action_shape)  # [None, None]

# Run the game
trajectories, payoffs = env.run(is_training=False)

last_state = trajectories[0][-1]

print("Payoffs:", payoffs)
print("Played Cards:", last_state["raw_obs"]["played_cards"])
print("Num Cards:", last_state["raw_obs"]["num_cards"])
print("Actions played:", last_state["action_record"])

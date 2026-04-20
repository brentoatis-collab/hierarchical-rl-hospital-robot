from env_hospital import HospitalGridWorld

env = HospitalGridWorld()
state = env.reset()

print("Initial State:", state)
env.render()

# Manual test actions
# right, right, right, down, down
test_actions = [3, 3, 3, 1, 1]

for action in test_actions:
    state, reward, done, info = env.step(action)
    print(f"Action: {action}, Reward: {reward}, Done: {done}")
    print("State:", state)
    env.render()

    if done:
        break
import numpy as np
import gym
import random
import matplotlib.pyplot as plt

def main():
    # Create Taxi environment
    env = gym.make('Taxi-v3')

    # Initialize Q-table
    state_size = env.observation_space.n
    action_size = env.action_space.n
    qtable = np.zeros((state_size, action_size))

    # Hyperparameters
    learning_rates = [ x  for x in np.arange(0.1, 1.0, 0.1) ]
    discount_rates = [ x  for x in np.arange(0.1, 1.0, 0.2) ]# Different discount rates to test
    epsilon = 1.0
    decay_rate = 0.005

    # Training variables
    num_episodes = 1000
    max_steps = 99  # per episode

    # Convergence threshold
    convergence_threshold = 0.01  # Adjust this threshold as needed

    # Store Q-values for each discount rate
    episodes = {rate: [] for rate in discount_rates}
    for q in episodes:
        episodes[q] = {rate: 0 for rate in learning_rates}
    for discount_rate in discount_rates:
        print(f"Training for learning rate {discount_rate}")
        required_episodes=[]
        for learning_rate in learning_rates:
            qtable = np.zeros((state_size, action_size))
            prev_qtable = np.copy(qtable)

            for episode in range(num_episodes):
                # Reset the environment
                state = env.reset()[0]
                done = False

                for s in range(max_steps):
                    # Exploration-exploitation tradeoff
                    if random.uniform(0, 1) < epsilon:
                        # Explore
                        action = env.action_space.sample()
                    else:
                        # Exploit
                        action = np.argmax(qtable[state, :])

                    # Take action and observe reward
                    new_state, reward, done, info, test = env.step(action)

                    # Q-learning algorithm
                    qtable[state, action] = qtable[state, action] + learning_rate * (
                        reward + discount_rate * np.max(qtable[new_state, :]) - qtable[state, action])

                    # Update to our new state
                    state = new_state

                    if done:
                        break

                # Store Q-values for the current episode

                episodes[discount_rate][learning_rate] = episode

                # Check for convergence
                if np.all(np.isclose(qtable, prev_qtable, atol=convergence_threshold)):
                    print(f"Convergence reached for learning rate {learning_rates} at episode {episode}")
                    break
                prev_qtable = np.copy(qtable)

                # Decrease epsilon
                epsilon = np.exp(-decay_rate * episode)

            # episodes[learning_rate].append(required_episodes.copy())
    print(f"Training completed over {num_episodes} episodes")
    input("Press Enter to watch trained agent...")
    print(episodes)

    # Plot episdoe at which convergence was reached for each discount rate

    #plot a line graph
    for discount_rate in discount_rates:
        # plt.figure()
        # plt.plot([q[action] for q in q_values], label=f'Action {action}')
        plt.plot(list(episodes[discount_rate].keys()), list(episodes[discount_rate].values()),label=f'Discount : {discount_rate}')


    plt.xlabel("Learning  Rate")
    plt.ylabel("Episode")
    plt.title("Episode at which Convergence was Reached")
    plt.legend()
    plt.show()

    # plt.bar(range(len(episodes)), list(episodes.values()), align='center')
    # plt.xticks(range(len(episodes)), list(episodes.keys()))
    # plt.xlabel("Discount Rate")
    # plt.ylabel("Episode")
    # plt.title("Episode at which Convergence was Reached")
    # plt.show()



if __name__ == "__main__":
    main()
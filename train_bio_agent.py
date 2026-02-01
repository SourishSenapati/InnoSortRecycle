"""
Training script for the RADORDENA-BIO-01 Process Control Agent.
Uses Reinforcement Learning (PPO) to optimize bio-reactor conditions.
"""
import gymnasium as gym
import numpy as np
from stable_baselines3 import PPO


class BioReactorEnv(gym.Env):
    """
    Custom Environment that follows gym interface.
    Simulates a Bioleaching Reactor for RL training.
    """
    metadata = {"render_modes": ["human"]}

    def render(self):
        """
        Render the environment. No-op for this simulation.
        """

    def __init__(self):
        super(BioReactorEnv, self).__init__()
        # Actions: [Dose Acid, Dose Base, Heater On/Off, Aeration]
        self.action_space = gym.spaces.Box(
            low=-1, high=1, shape=(4,), dtype=np.float32)

        # Observations: [Current pH, Temp, Dissolved Oxygen, Bacteria Health]
        # Using a broader observation space to avoid boundary issues during training
        self.observation_space = gym.spaces.Box(
            low=0, high=200, shape=(4,), dtype=np.float32)

        # Initial State
        self.state = np.array([7.0, 25.0, 5.0, 100.0], dtype=np.float32)

    def step(self, action):
        # Physics Logic (Simplified for training)
        acid_dose, base_dose, heat, _ = action

        # Update pH (Acid lowers it, Base raises it)
        # Scaling factor adjusted for simulation stability
        # pH limits are naturally physical, but we let the agent discover them
        self.state[0] += (base_dose * 0.5) - (acid_dose * 0.5)

        # Update Temp
        self.state[1] += heat * 1.0

        # Add some noise/drift to simulate real sensors
        self.state[0] += np.random.normal(0, 0.05)
        self.state[1] += np.random.normal(0, 0.1)

        # Calculate Reward: Target pH 1.8, Target Temp 30
        ph_error = abs(self.state[0] - 1.8)
        temp_error = abs(self.state[1] - 30.0)
        reward = - (ph_error + temp_error)  # Negative reward for error

        # Check if "Crash" (Bacteria die)
        done = False
        if self.state[0] < 1.0 or self.state[0] > 9.0:
            reward -= 100
            done = True

        # Truncate if too long (optional, but good for training loops)
        truncated = False

        return self.state, reward, done, truncated, {}

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.state = np.array([7.0, 25.0, 5.0, 100.0], dtype=np.float32)
        return self.state, {}

# --- TRAINING THE AGENT ---


def train_bio_agent():
    """
    Main function to initialize environment and train the PPO agent.
    """
    env = BioReactorEnv()

    # Initialize PPO Agent on RTX 4050
    # Uses 'MlpPolicy' because inputs are vector numbers, not images
    model = PPO("MlpPolicy", env, verbose=1, device="cuda")

    # Train for 100,000 steps (Simulation)
    print("Training Bio-Agent in Digital Twin...")
    model.learn(total_timesteps=100000)

    # Save the brain
    model.save("radordena_bio_controller")
    print("Training Complete. Agent Saved.")


if __name__ == '__main__':
    try:
        train_bio_agent()
    except KeyboardInterrupt:
        print("\nTraining interrupted by user. Saving checkpoint...")
        # Note: In a real implementation with stable-baselines3, we would need
        # a callback to save the *current* state. For this script, we'll cleanly exit.
        print("Progress not saved automatically without ChecksCallback. Exiting.")

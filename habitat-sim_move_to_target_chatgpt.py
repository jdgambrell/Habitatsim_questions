import habitat_sim
import habitat
import numpy as np
import time


#set sim settings using format in habitat-sim tutorial
#sim_settings = 

# Step 1: Set up the simulator configuration
sim_cfg = habitat_sim.SimulatorConfiguration()

# Specify the scene path (replace with your specific scene file)
sim_cfg.scene_id = "/home/jerry/habitat-matterport-3dresearch/example/hm3d-example-semantic-annots-v0.2/00861-GLAQ4DNUx5U/GLAQ4DNUx5U.semantic.glb"
#Set the scene config file ()
    #config = habitat.get_config("config.yaml")
    #config = "/home/jerry/habitat-matterport-3dresearch/example/hm3d-example-semantic-annots-v0.2/00861-GLAQ4DNUx5U/GLAQ4DNUx5U.semantic.txt"
# Disable GPU
sim_cfg.gpu_device_id = -1


# Step 2: Create the agent configuration
agent_cfg = habitat_sim.AgentConfiguration()

# Step 3: Set up sensor specification for the agent
# sensor_spec = habitat_sim.SensorSpec()  # Create a default sensor specification
# agent_cfg.sensor_specifications = [sensor_spec]  # Assigning the sensor specification to the agent

# Step 3: Set up sensor specification for the agent

# Create a SensorSpec for each sensor type
rgb_sensor = habitat_sim.SensorSpec()
rgb_sensor.uuid = "RGB_SENSOR"
rgb_sensor.sensor_type = habitat_sim.SensorType.COLOR
rgb_sensor.resolution = [256, 256]

depth_sensor = habitat_sim.SensorSpec()
depth_sensor.uuid = "DEPTH_SENSOR"
depth_sensor.sensor_type = habitat_sim.SensorType.DEPTH
depth_sensor.resolution = [256, 256]

semantic_sensor = habitat_sim.SensorSpec()
semantic_sensor.uuid = "SEMANTIC_SENSOR"
semantic_sensor.sensor_type = habitat_sim.SensorType.SEMANTIC
semantic_sensor.resolution = [256, 256]

# Now assign these sensor specifications to the agent configuration
agent_cfg.sensor_specifications = [rgb_sensor, depth_sensor, semantic_sensor]
#agent_cfg.sensor_specifications = [rgb_sensor, semantic_sensor]



# Step 4: Initialize the simulator with the agent configuration
# Habitat-Sim automatically handles the agent configuration during simulator initialization
agents = [agent_cfg]
hab_config = habitat_sim.Configuration(sim_cfg, agents)
sim = habitat_sim.Simulator(hab_config)
#sim = habitat_sim.Simulator(sim_cfg)

# Step 5: Retrieve the default agent (ID 0) from the simulator
# The first agent (ID 0) is created automatically when initializing the simulator
agent = sim.get_agent(0)  # Default first agent

# Step 6: Define target coordinates for the agent (example target)
target_coordinates = np.array([5.0, 0.0, 5.0])  # Example target

# Step 7: Define a function to navigate to the target
def navigate_to_target(agent, target_coordinates, max_steps=500):
    for step in range(max_steps):
        # Get current agent state (position)
        agent_state = agent.get_state()  # This updates the agent's state
        current_position = np.array(agent_state.position)

        # Compute direction to target
        direction = target_coordinates - current_position
        distance_to_target = np.linalg.norm(direction)

        # If the agent is close to the target, stop
        if distance_to_target < 0.5:
            print(f"Arrived at target in {step} steps!")
            break

        # Normalize direction and move in that direction
        direction_normalized = direction / distance_to_target
        new_position = current_position + direction_normalized * 0.1
        agent.set_state(habitat_sim.AgentState(position=new_position))

        # Optionally render the scene to visualize agent's movement
        # sim.render()  # Uncomment to visualize

        time.sleep(0.1)  # Simulate a small time delay between steps

    else:
        print(f"Target not reached in {max_steps} steps")

# Step 8: Start navigation
navigate_to_target(agent, target_coordinates)

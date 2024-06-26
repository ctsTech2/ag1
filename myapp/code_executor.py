# This was an example from the auto Gen docs. I didn't end up using it because I used my docker_setup.py file. 
from autogen.coding import DockerCommandLineCodeExecutor
import tempfile

# Create a temporary directory to store the code files.
temp_dir = tempfile.TemporaryDirectory()

# Create a Docker command line code executor.
executor = DockerCommandLineCodeExecutor(
    
    image="python:3.12-slim",  # Execute code using the given docker image name.
    timeout=10,  # Timeout for each code execution in seconds.
    work_dir=temp_dir.name,  # Use the temporary directory to store the code files.
)

# Create an agent with code executor configuration that uses docker.
code_executor_agent_using_docker = ConversableAgent(
    "code_executor_agent_docker",
    llm_config=False,  # Turn off LLM for this agent.
    code_execution_config={"executor": executor},  # Use the docker command line code executor.
    human_input_mode="ALWAYS",  # Always take human input for this agent for safety.
)

# Placeholder for code execution logic, if needed.
# Example: code_executor_agent_using_docker.execute("print('Hello, World!')")

# When the code executor is no longer used, stop it to release the resources.
executor.stop()

# Clean up the temporary directory.
temp_dir.cleanup()


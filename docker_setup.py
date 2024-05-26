from pathlib import Path
from autogen import UserProxyAgent
from autogen.coding import DockerCommandLineCodeExecutor

# Create a directory for code execution
work_dir = Path("coding")
work_dir.mkdir(exist_ok=True)
print("Directory for code execution created at:", work_dir)

# Set up the Docker command line code executor with a specified Docker image
with DockerCommandLineCodeExecutor(
    image="autogen_custom_img",  # Specify the Docker image
    timeout=10,  # Timeout for each code execution in seconds
    work_dir=work_dir  # Use the persistent directory to store the code files
) as code_executor:
    print("DockerCommandLineCodeExecutor has been set up")
    user_proxy = UserProxyAgent(
        name="user_proxy",
        code_execution_config={"executor": code_executor},
    )
    print("UserProxyAgent has been created and configured")

# End of script
print("docker_setup.py script execution completed")
# Now you can use `user_proxy` for code execution tasks

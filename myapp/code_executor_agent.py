# A rabbit hole with gpt 4. Where we tried to Run code. With Docker inside of Docker. Instead of just running Autogen with a Docker executor in a conda environment. Gpt 4 wanted to use user proxy Instead of converseable agent Because user proxy is a common base template where not much configuration is needed 
from pathlib import Path
from autogen import UserProxyAgent
from autogen.coding import DockerCommandLineCodeExecutor

# Create a directory for code execution
work_dir = Path("coding")
work_dir.mkdir(exist_ok=True)
print("Directory for code execution created at:", work_dir)

# Set up the Docker command line code executor with your existing Docker image
executor = DockerCommandLineCodeExecutor(
    image="autogen_custom_img",  # Use your existing Docker image
    timeout=10,  # Timeout for each code execution in seconds
    work_dir=work_dir  # Use the persistent directory to store the code files
)
print("DockerCommandLineCodeExecutor has been set up")

# Create the code executor agent
code_executor_agent = UserProxyAgent(
    name="code_executor_agent",
    code_execution_config={"executor": executor},
)
print("Code executor agent has been created and configured")

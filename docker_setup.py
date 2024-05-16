from pathlib import Path
from autogen import UserProxyAgent
from autogen.coding import DockerCommandLineCodeExecutor

# Create a directory for code execution
work_dir = Path("coding")
work_dir.mkdir(exist_ok=True)

# Set up the Docker command line code executor
with DockerCommandLineCodeExecutor(work_dir=work_dir) as code_executor:
    user_proxy = UserProxyAgent(
        name="user_proxy",
        code_execution_config={"executor": code_executor},
    )

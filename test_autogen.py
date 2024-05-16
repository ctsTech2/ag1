from pathlib import Path
from autogen import UserProxyAgent
from autogen.coding import DockerCommandLineCodeExecutor

# Create a directory for code execution if it doesn't exist
work_dir = Path("coding")
work_dir.mkdir(exist_ok=True)

# Set up the Docker command line code executor
with DockerCommandLineCodeExecutor(work_dir=work_dir) as code_executor:
    user_proxy = UserProxyAgent(
        name="user_proxy",
        code_execution_config={"executor": code_executor},
    )

    # Define a simple Python script to run inside Docker
    script = """
    print('Hello from AutoGen inside Docker!')
    """

    # Write the script to a file
    script_path = work_dir / "script.py"
    with open(script_path, "w") as file:
        file.write(script)

    # Execute the script using the Docker executor
    result = code_executor.run(f"python {script_path}")
    print(result.output)



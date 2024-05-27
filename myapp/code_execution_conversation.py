# A rabbit hole with gpt 4. Where we tried to Run code. With Docker inside of Docker. Instead of just running Autogen with a Docker executor in a conda environment. Gpt 4 wanted to use user proxy Instead of converseable agent Because user proxy is a common base template where not much configuration is needed import os
from pathlib import Path
from autogen import ConversableAgent, UserProxyAgent
from autogen.coding import DockerCommandLineCodeExecutor

# Create a directory for code execution if it doesn't exist
work_dir = Path("coding")
work_dir.mkdir(exist_ok=True)
print(f"Directory for code execution created at: {work_dir}")

# Set up the Docker command line code executor with your existing Docker image
executor = DockerCommandLineCodeExecutor(
    image="autogen_custom_img",  # Use your existing Docker image
    timeout=10,  # Timeout for each code execution in seconds
    work_dir=work_dir  # Use the persistent directory to store the code files
)
print("DockerCommandLineCodeExecutor has been set up")

# Define the code writer agent
code_writer_system_message = """You are a helpful AI assistant.
Solve tasks using your coding and language skills.
In the following cases, suggest python code (in a python coding block) or shell script (in a sh coding block) for the user to execute.
1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to be solved based on your language skill, you can solve the task by yourself.
2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly.
Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill.
When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user.
If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the user.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.
Reply 'TERMINATE' in the end when everything is done.
"""

code_writer_agent = ConversableAgent(
    "code_writer_agent",
    system_message=code_writer_system_message,
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
    code_execution_config=False,  # Turn off code execution for this agent.
)
print("Code writer agent has been created.")

# Define the code executor agent
code_executor_agent = UserProxyAgent(
    name="code_executor_agent",
    code_execution_config={"executor": executor},
)
print("Code executor agent has been created and configured")

# Log the work directory content before execution
print(f"Contents of work directory before execution: {list(work_dir.iterdir())}")

# Initiate a conversation between the code writer agent and the code executor agent
chat_result = code_executor_agent.initiate_chat(
    code_writer_agent,
    message="Write Python code to calculate the 14th Fibonacci number.",
)

# Print the chat result
print(chat_result)

# Log the work directory content after execution
print(f"Contents of work directory after execution: {list(work_dir.iterdir())}")

# Check the contents of the temporary code file if it exists
tmp_files = list(work_dir.glob("*.py"))
if tmp_files:
    for tmp_file in tmp_files:
        with open(tmp_file, 'r') as file:
            print(f"Contents of {tmp_file.name}:")
            print(file.read())
else:
    print("No temporary code files found in the work directory.")

# End of script
print("code_execution_conversation.py script execution completed")

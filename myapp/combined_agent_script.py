import os
from pathlib import Path
from dotenv import load_dotenv
from autogen import ConversableAgent
from autogen.coding import DockerCommandLineCodeExecutor

# Load environment variables from the .env file
load_dotenv()

# Ensure the OpenAI API key is loaded
if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("OPENAI_API_KEY environment variable not set")

# Create a directory for code execution if it doesn't exist
work_dir = Path("coding")
work_dir.mkdir(exist_ok=True)
print(f"Directory for code execution created at: {work_dir}")

# Set up the Docker command line code executor
executor = DockerCommandLineCodeExecutor(
    image="autogen_custom_img",  # Use your existing Docker image
    timeout=10,  # Timeout for each code execution in seconds
    work_dir=work_dir  # Use the persistent directory to store the code files
)
print("DockerCommandLineCodeExecutor has been set up")

# Define the code writer agent's system message to instruct the LLM on how to use the code executor in the code executor agent.
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

# Create the code writer agent
code_writer_agent = ConversableAgent(
    "code_writer_agent",
    system_message=code_writer_system_message,
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": os.environ["OPENAI_API_KEY"]}]},
    code_execution_config=False,  # Turn off code execution for this agent.
)
print("Code writer agent has been created.")

# Create the code executor agent
code_executor_agent = ConversableAgent(
    "code_executor_agent",
    llm_config=False,  # Turn off LLM for this agent.
    code_execution_config={"executor": executor},  # Use the Docker command line code executor.
    human_input_mode="ALWAYS",  # Always take human input for this agent for safety.
)
print("Code executor agent has been created and configured")

# Initiate a conversation between the code writer agent and the code executor agent
terminate = False
while not terminate:
    chat_result = code_executor_agent.initiate_chat(
        code_writer_agent,
        message="Write Python code to calculate the 14th Fibonacci number.",
    )

    # Print the chat result
    print(chat_result)

    # Check if the conversation should terminate
    for message in chat_result.chat_history:
        if "TERMINATE" in message['content']:
            terminate = True
            break

# Stop the Docker command line code executor to release the resources
executor.stop()
print("DockerCommandLineCodeExecutor has been stopped")

# End of script
print("Script execution completed")

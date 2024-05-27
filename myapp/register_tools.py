import os
from dotenv import load_dotenv
from autogen import ConversableAgent, register_function
from calculator_tool import calculator

load_dotenv()  # Load environment variables from .env file

# Define the assistant agent
assistant = ConversableAgent(
    name="Assistant",
    system_message="You are a helpful AI assistant. You can help with simple calculations. Return 'TERMINATE' when the task is done.",
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": os.environ["OPENAI_API_KEY"]}]},
)

# Define the user proxy agent
user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

# Register the updated calculator function with both agents
register_function(
    calculator,
    caller=assistant,  # The assistant agent can suggest calls to the calculator.
    executor=user_proxy,  # The user proxy agent can execute the calculator calls.
    name="calculator",  # By default, the function name is used as the tool name.
    description="A calculator tool that accepts nested expression as input",  # A description of the tool.
)

if __name__ == "__main__":
    # Initiate a chat to test the tool
    chat_result = user_proxy.initiate_chat(assistant, message="What is (1423 - 123) / 3 + (32 + 23) * 5?")
    # print(chat_result)

import os
from dotenv import load_dotenv
from autogen import ConversableAgent, GroupChat, GroupChatManager

# Load environment variables from the .env file
load_dotenv()

# Ensure the OpenAI API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

# Create the agents with descriptions
number_agent = ConversableAgent(
    name="Number_Agent",
    system_message="You return me the numbers I give you, one number each line.",
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": api_key}]},
    human_input_mode="NEVER",
    description="Return the numbers given."
)

adder_agent = ConversableAgent(
    name="Adder_Agent",
    system_message="You add 1 to each number I give you and return me the new numbers, one number each line.",
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": api_key}]},
    human_input_mode="NEVER",
    description="Add 1 to each input number."
)

multiplier_agent = ConversableAgent(
    name="Multiplier_Agent",
    system_message="You multiply each number I give you by 2 and return me the new numbers, one number each line.",
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": api_key}]},
    human_input_mode="NEVER",
    description="Multiply each input number by 2."
)

subtracter_agent = ConversableAgent(
    name="Subtracter_Agent",
    system_message="You subtract 1 from each number I give you and return me the new numbers, one number each line.",
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": api_key}]},
    human_input_mode="NEVER",
    description="Subtract 1 from each input number."
)

divider_agent = ConversableAgent(
    name="Divider_Agent",
    system_message="You divide each number I give you by 2 and return me the new numbers, one number each line.",
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": api_key}]},
    human_input_mode="NEVER",
    description="Divide each input number by 2."
)

# Create a GroupChat object
group_chat = GroupChat(
    agents=[adder_agent, multiplier_agent, subtracter_agent, divider_agent, number_agent],
    messages=[],
    max_round=6,
    send_introductions=True,
)

# Create a GroupChatManager object
group_chat_manager = GroupChatManager(
    groupchat=group_chat,
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": api_key}]},
)

# Start the group chat
chat_result = number_agent.initiate_chat(
    group_chat_manager,
    message="My number is 3, I want to turn it into 13.",
    summary_method="reflection_with_llm",
)

# Print the chat summary
print("Chat Summary:")
print(chat_result.summary)

# Print the chat history
print("\nChat History:")
import pprint
pprint.pprint(chat_result.chat_history)

# Print the cost of the chat
print("\nChat Cost:")
pprint.pprint(chat_result.cost)

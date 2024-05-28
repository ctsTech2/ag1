import os
from dotenv import load_dotenv
from autogen import ConversableAgent, GroupChat, GroupChatManager
import pprint  # Import pprint for pretty-printing

# Load environment variables from the .env file
load_dotenv()

# Ensure the OpenAI API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

# Create the agents with system messages and descriptions
number_agent = ConversableAgent(
    name="Number_Agent",
    system_message="You return me the numbers I give you, one number each line.",
    description="Return the numbers given.",
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": api_key}]},
    human_input_mode="NEVER"
)

adder_agent = ConversableAgent(
    name="Adder_Agent",
    system_message="You add 1 to each number I give you and return me the new numbers, one number each line.",
    description="Add 1 to each input number.",
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": api_key}]},
    human_input_mode="NEVER"
)

multiplier_agent = ConversableAgent(
    name="Multiplier_Agent",
    system_message="You multiply each number I give you by 2 and return me the new numbers, one number each line.",
    description="Multiply each input number by 2.",
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": api_key}]},
    human_input_mode="NEVER"
)

subtracter_agent = ConversableAgent(
    name="Subtracter_Agent",
    system_message="You subtract 1 from each number I give you and return me the new numbers, one number each line.",
    description="Subtract 1 from each input number.",
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": api_key}]},
    human_input_mode="NEVER"
)

divider_agent = ConversableAgent(
    name="Divider_Agent",
    system_message="You divide each number I give you by 2 and return me the new numbers, one number each line.",
    description="Divide each input number by 2.",
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": api_key}]},
    human_input_mode="NEVER"
)

# Define the allowed transitions for each agent using agent objects
allowed_transitions = {
    number_agent: [adder_agent, number_agent],
    adder_agent: [multiplier_agent, number_agent],
    subtracter_agent: [divider_agent, number_agent],
    multiplier_agent: [subtracter_agent, number_agent],
    divider_agent: [adder_agent, number_agent],
}

# Create a GroupChat object with allowed transitions
constrained_graph_chat = GroupChat(
    agents=[adder_agent, multiplier_agent, subtracter_agent, divider_agent, number_agent],
    allowed_or_disallowed_speaker_transitions=allowed_transitions,
    speaker_transitions_type="allowed",
    messages=[],
    max_round=12,
    send_introductions=True,
)

# Create a GroupChatManager object
constrained_group_chat_manager = GroupChatManager(
    groupchat=constrained_graph_chat,
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": api_key}]},
)

# Initiate the chat
chat_result = number_agent.initiate_chat(
    constrained_group_chat_manager,
    message="My number is 3, I want to turn it into 10. Once I get to 10, keep it there.",
    summary_method="reflection_with_llm",
)

# # Print the chat summary and history
# print("Chat Summary:")
# print(chat_result.summary)

# print("\nChat History:")
# pprint.pprint(chat_result.chat_history)

# print("\nChat Cost:")
# pprint.pprint(chat_result.cost)

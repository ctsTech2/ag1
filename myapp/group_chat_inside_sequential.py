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

# Create a GroupChat object with introductions
group_chat_with_introductions = GroupChat(
    agents=[adder_agent, multiplier_agent, subtracter_agent, divider_agent, number_agent],
    messages=[],
    max_round=6,
    send_introductions=True,
)

# Create a GroupChatManager object with introductions
group_chat_manager_with_intros = GroupChatManager(
    groupchat=group_chat_with_introductions,
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": api_key}]},
)

# Start a sequence of two-agent chats between the number agent and the group chat manager
chat_results = number_agent.initiate_chats(
    [
        {
            "recipient": group_chat_manager_with_intros,
            "message": "My number is 3, I want to turn it into 13. Use each other's outputs to reach the goal.",
            "clear_history": False,  # Retain history for subsequent chats
        },
        {
            "recipient": group_chat_manager_with_intros,
            "message": "Turn this number to 32.",
            "clear_history": False,  # Retain history for subsequent chats
        },
    ]
)

# # Print the summaries of each chat
# for i, result in enumerate(chat_results, start=1):
#     print(f"Chat {i} Summary:")
#     print(result.summary)
#     print("\nChat History:")
#     pprint.pprint(result.chat_history)
#     print("\nChat Cost:")
#     pprint.pprint(result.cost)
#     print("\n" + "="*80 + "\n")

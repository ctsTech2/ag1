import os
from autogen import ConversableAgent

# Create the agent Cathy
cathy = ConversableAgent(
    "cathy",
    system_message="Your name is Cathy and you are a part of a duo of comedians.",
    llm_config={"config_list": [{"model": "gpt-4o", "temperature": 0.9, "api_key": os.environ.get("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",  # Never ask for human input.
)

# Create the agent Joe
joe = ConversableAgent(
    "joe",
    system_message="Your name is Joe and you are a part of a duo of comedians.",
    llm_config={"config_list": [{"model": "gpt-4o", "temperature": 0.7, "api_key": os.environ.get("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",  # Never ask for human input.
    max_consecutive_auto_reply=1,  # Limit the number of consecutive auto-replies.
)

# Initiate a short chat between Joe and Cathy
result = joe.initiate_chat(cathy, message="Cathy, tell me a joke.", max_turns=2)

# Print the result of the conversation
# print(result)

#Example of a ChatResult object
# ChatResult(chat_id=None, chat_history=
#            [
#                {'content': 'Cathy, tell me a joke.', 'role': 'assistant'}, 
#                {'content': "Why don't scientists trust atoms?\n\nBecause they make up everything!", 'role': 'user'}, 
#                {'content': "Haha, good one Cathy! Okay, my turn. \n\nWhy don't we ever tell secrets on a farm?\n\nBecause the potatoes have eyes, the corn has ears, and the beans stalk.", 'role': 'assistant'}, 
#                {'content': "Haha, that's absolutely hilarious! You've got the farm gossips all figured out! Your turn, Cathy.\n\nWhy was the math book sad?\n\nBecause it had too many problems!", 'role': 'user'}], 
#            summary="Haha, that's absolutely hilarious! You've got the farm gossips all figured out! Your turn, Cathy.\n\nWhy was the math book sad?\n\nBecause it had too many problems!", 
#            cost={'usage_including_cached_inference': 
#                {'total_cost': 0.011009999999999999, 'gpt-4-0613': {'cost': 0.011009999999999999, 'prompt_tokens': 183, 'completion_tokens': 92, 'total_tokens': 275}}, 
#                'usage_excluding_cached_inference': {'total_cost': 0.011009999999999999, 'gpt-4-0613': {'cost': 0.011009999999999999, 'prompt_tokens': 183, 'completion_tokens': 92, 'total_tokens': 275}}}, 
#            human_input=[]
#            )

# Print the result of the conversation, pulling out the chat history
# for msg in result.chat_history:
#     print(f"{msg['role']}: {msg['content']}")
import os
from dotenv import load_dotenv
from autogen import ConversableAgent

# Load environment variables from the .env file
load_dotenv()

# Ensure the OpenAI API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

# Create the student agent
student_agent = ConversableAgent(
    name="Student_Agent",
    system_message="You are a student willing to learn.",
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": api_key}]},
)

# Create the teacher agent
teacher_agent = ConversableAgent(
    name="Teacher_Agent",
    system_message="You are a math teacher.",
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": api_key}]},
)

# Initiate a chat between the student agent and the teacher agent
chat_result = student_agent.initiate_chat(
    teacher_agent,
    message="What is triangle inequality?",
    summary_method="reflection_with_llm",
    max_turns=2,
)

# Print the chat summary
print("Chat Summary:")
print(chat_result.summary)

# Print the chat history
# print("\nChat History:")
# import pprint
# pprint.pprint(chat_result.chat_history)

# Print the cost of the chat
# print("\nChat Cost:")
# pprint.pprint(chat_result.cost)

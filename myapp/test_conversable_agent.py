import os
from autogen import ConversableAgent

# Create the ConversableAgent with GPT-4 LLM
agent = ConversableAgent(
    "chatbot",
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": os.environ.get("OPENAI_API_KEY")}]},
    code_execution_config=False,  # Turn off code execution
    function_map=None,  # No registered functions
    human_input_mode="NEVER",  # Never ask for human input
)

# Test the agent by asking it to generate a reply to a question
reply = agent.generate_reply(messages=[{"content": "Tell me a joke.", "role": "user"}])
print(reply)


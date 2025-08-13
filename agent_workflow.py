# A Simple Multi-Step Agent
"""
This script will define an agent that:

    Receives a natural language question.

    Decides if it needs to use a tool (like Wikipedia search) to answer the question.

    If a tool is used, it processes the tool's output.

    Formulates a final answer using the LLM.

    All these steps will be automatically traced by Langfuse thanks to the CallbackHandler.
"""

import os
from dotenv import load_dotenv

# from langchain_openai import ChatOpenAI # For future version
from langchain_community.chat_models import ChatOllama # Import ChatOllama
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain import hub
from langfuse.langchain import CallbackHandler

# --- 0. Load Environment Variables (if using .env file) ---
# Make sure the .env file is in the root of your project
# and contains OLLAMA_BASE_URL, (OPENAI_API_KEY), LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST
load_dotenv()

# --- 1. Initialize Langfuse Callback Handler ---
langfuse_handler = CallbackHandler(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

# --- 2. Define the LLM (using Ollama) ---
# Ensure Ollama is running and it has pulled the model (e.g., ollama pull llama3)
llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "llama3"), # Default to 'llama3' if not set in .env
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"), # Default Ollama URL
    temperature=0
)

# --- 3. Define the Tools the Agent Can Use ---
# I'll use the Wikipedia tool for demonstration.
# This tool allows the agent to search Wikipedia for information.
wikipedia_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
wikipedia_tool = WikipediaQueryRun(api_wrapper=wikipedia_wrapper)

# Put all available tools into a list
tools = [wikipedia_tool]

# --- 4. Pull the Agent Prompt from LangChain Hub ---
# The ReAct agent prompt defines how the LLM reasons and uses tools.
# This prompt typically includes placeholders for `tools`, `tool_names`, and `agent_scratchpad`.
prompt = hub.pull("hwchase17/react")

# --- 5. Create the ReAct Agent ---
# The create_react_agent function creates a runnable agent.
# It takes the LLM, tools, and the ReAct prompt.
agent = create_react_agent(llm, tools, prompt)

# --- 6. Create the Agent Executor ---
# The AgentExecutor is responsible for executing the agent's plan,
# calling tools, and managing the iterative process.
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True, # Set to True to see the agent's thought process in the console
    handle_parsing_errors=True # Good practice for robust agents
)

# --- 7. Define a Function to Run the Agent with Observability ---
def run_agent_workflow(query: str):
    print(f"\n--- Running Agent for Query: '{query}' ---")
    try:
        # Invoke the agent executor, passing the Langfuse callback handler
        result = agent_executor.invoke(
            {"input": query},
            config={"callbacks": [langfuse_handler]}
        )
        print("\n--- Agent Finished ---")
        print("Final Answer:", result["output"])
    except Exception as e:
        print(f"\n--- Agent Error: {e} ---")
        # Langfuse should still capture the error in the trace

# --- 8. Run Some Example Queries ---
if __name__ == "__main__":
    # Example 1: A question that requires using the Wikipedia tool
    run_agent_workflow("Who is the current CEO of Google?")

    # Example 2: A question that might not require a tool, or is general knowledge
    run_agent_workflow("What is the capital of France?")

    # Example 3: A question that might lead to an error or an interesting trace
    run_agent_workflow("Tell me about the history of the internet in 3 sentences and then find me the capital of Bhutan.")

    print("\nCheck your Langfuse dashboard for traces of these runs!")
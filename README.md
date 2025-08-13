# Agent Trace: AI Observability Agent

**Agent Trace** is a proof-of-concept application that provides observability and monitoring for LLM-powered agents and workflows. This project addresses the critical need for debugging, performance monitoring, and cost tracking of complex AI systems deployed in a production environment.

The core idea is to transform the "black box" of LLM agent behavior into a transparent, actionable dashboard. The objective of this MVP is to demonstrate the foundational components required to capture and analyze every step of an agent's reasoning process.

## Features (MVP)

-   **Agent Workflow Tracing:** Captures a detailed, step-by-step trace of a LangChain agent's execution, including LLM calls, tool usage, and intermediate thoughts.
-   **Metrics Collection:** Automatically logs key metrics such as latency, token usage, and estimated costs for each LLM invocation.
-   **Error and Failure Detection:** Identifies and logs errors that occur during the agent's execution or within its tool calls.
-   **Open-Source Integration:** Built to work with locally hosted, open-source LLMs (via Ollama) to minimize development costs.
-   **Observability Backend:** Utilizes Langfuse to store and visualize the trace data, providing a robust foundation for an observability dashboard.

## System Architecture

The project follows a simple but powerful architecture:

1.  A **LangChain Agent** (`agent_workflow.py`) performs a multi-step task.
2.  The **Langfuse Callback Handler** instruments the agent, automatically sending trace data to the Langfuse backend.
3.  The (future) **Streamlit Dashboard** will consume the data from the Langfuse API to provide a user-friendly visualization of the agent's behavior.

## Getting Started

This guide helps to set up and run the `agent_workflow.py` script, which generates the observable data for the project.

### Prerequisites

-   [Python 3.9+](https://www.python.org/)
-   [Ollama](https://ollama.com/) (to run open-source models locally)
-   [An active virtual environment](https://docs.python.org/3/library/venv.html)
-   A free [Langfuse](https://cloud.langfuse.com/) account (the "Hobby" plan is perfect for this project)

### 1. Installation

1.  Clone this repository and navigate to the project directory:
    ```bash
    git clone [https://github.com/your-username/ai-observability-agent.git](https://github.com/your-username/ai-observability-agent.git)
    cd ai-observability-agent
    ```
2.  Set up and activate the Python virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Install the necessary Python packages:
    ```bash
    pip install python-dotenv langchain langchain-community langchain-ollama wikipedia
    ```

### 2. Configuration

1.  **Ollama:** Make sure the Ollama server is running and a model is pulled (e.g., `llama3`).
    ```bash
    ollama serve
    ollama pull llama3
    ```
2.  **Environment Variables:** Create a file named `.env` in the root of the project and add your API keys.

    ```dotenv
    # Langfuse Configuration
    LANGFUSE_PUBLIC_KEY=pk-lf-...
    LANGFUSE_SECRET_KEY=sk-lf-...
    LANGFUSE_HOST=[https://cloud.langfuse.com](https://cloud.langfuse.com)

    # Ollama Configuration
    OLLAMA_BASE_URL=http://localhost:11434
    OLLAMA_MODEL=llama3
    ```

### 3. Run the Agent

Execute the agent script. This will perform several multi-step tasks and send the traces to the Langfuse account.

```bash
python agent_workflow.py
```
After running the script, log in to the Langfuse dashboard to view the generated traces, metrics, and logs.
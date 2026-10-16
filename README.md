# AI Customer Support Agent

An agentic AI customer-support application built with Python and the OpenAI Responses API. The agent selects and executes tools to answer customer questions, handle missing order information, and prepare a simulated support handoff.

## Features

- **Agentic tool calling:** The model chooses the appropriate tool for a customer request.
- **Order lookup:** Retrieves status and estimated delivery information from a fictional order database.
- **Policy lookup:** Answers supported delivery, refund, return, and cancellation questions.
- **Multi-step execution:** Combines results from multiple tools in one response.
- **Safe handling:** Avoids inventing order information and prepares a demo handoff when an order cannot be found.
- **Execution safeguards:** Configurable limits for tool-use rounds and total tool calls.
- **Automated tests:** Uses pytest to validate tools and agent-controller behavior.

## Architecture

1. Customer submits a request.
2. The OpenAI Responses API determines whether a tool is needed.
3. Python executes the requested tool.
4. Tool results are returned to the model.
5. The agent continues until it produces a final response or reaches an execution limit.

## Tech Stack

- Python
- OpenAI Responses API
- OpenAI function calling
- pytest
- python-dotenv

## Project Structure

```text
project-4-ai-customer-support-agent/
├── config.py
├── requirements.txt
├── .gitignore
├── README.md
├── src/
│   ├── __init__.py
│   ├── agent.py
│   └── agent_tools.py
├── tests/
│   ├── __init__.py
│   └── test_agent_tools.py
└── data/
    └── support_faq.txt
```

## Setup

1. Create and activate a Python virtual environment.
2. Install the dependencies listed in `requirements.txt`.
3. Create a `.env` file in the project root and set `OPENAI_API_KEY` to your own OpenAI API key.
4. Run the agent or the tests using the commands below.

## Run the Tests

```bash
python -m pytest -v
```

## Example Request

```text
Check order ORD-1001 and tell me the delivery estimate.
Also, what is the standard delivery policy?
```

The agent can use the order-status and policy-lookup tools, then combine the results into one response.

## Safety and Scope

This is an educational demonstration using fictional order data and sample policies. The support handoff is simulated; no real support ticket is created, and no real orders or refunds are changed. API usage may incur charges.

## Future Improvements

- Structured execution traces and error monitoring
- More comprehensive agent-controller tests
- Human approval for sensitive actions
- Integration with a real order-management system

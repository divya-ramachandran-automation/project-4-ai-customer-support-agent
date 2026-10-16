
import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from config import MODEL, MAX_TOOL_CALLS, MAX_TOOL_ROUNDS

from src.agent_tools import (
    get_order_status,
    lookup_policy,
    escalate_to_support,
)

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TOOLS = [
    {
        "type": "function",
        "name": "get_order_status",
        "description": "Look up the status and estimated delivery of a ShopEase order.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"}
            },
            "required": ["order_id"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "lookup_policy",
        "description": "Look up ShopEase delivery, refund, return, or cancellation policies.",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "enum": [
                        "delivery",
                        "refund",
                        "return",
                        "cancellation",
                    ],
                }
            },
            "required": ["topic"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "escalate_to_support",
        "description": "Prepare a demo support handoff when information is unavailable or human assistance is needed.",
        "parameters": {
            "type": "object",
            "properties": {
                "reason": {"type": "string"}
            },
            "required": ["reason"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]

TOOL_FUNCTIONS = {
    "get_order_status": get_order_status,
    "lookup_policy": lookup_policy,
    "escalate_to_support": escalate_to_support,
}


def run_agent(question: str) -> str:
    """Run the agent and execute requested tools until it produces an answer."""
    response = client.responses.create(
        model=MODEL,
        instructions=(
            "You are the ShopEase customer support agent. "
            "Use tools to answer customer questions whenever appropriate. "
            "You may call multiple tools when necessary. "
            "Never invent order details or company policies. "
            "When get_order_status reports that an order was not found, "
            "call escalate_to_support to prepare a demo handoff, then explain "
            "that the order could not be found and support handoff was prepared. "
            "When policy information is unavailable or human assistance is needed, "
            "use the support handoff tool. "
            "The handoff is a demo only; never claim a real ticket was created. "
            "Answer customers clearly and politely."
        ),
        input=question,
        tools=TOOLS,
    )

    # Allow several tool-use rounds, but prevent an endless loop.
    total_tool_calls = 0
    for _ in range(MAX_TOOL_ROUNDS):
        function_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        if not function_calls:
            print(f"[Agent] Total tool calls: {total_tool_calls}")
            return response.output_text

        tool_outputs = []

        for call in function_calls:
            if total_tool_calls >= MAX_TOOL_CALLS:
                return "I reached the tool-use limit. Please contact ShopEase support."
            total_tool_calls += 1
            
            try:
                arguments = json.loads(call.arguments)
                print(f"[Agent] Calling tool: {call.name}")
                tool_result = TOOL_FUNCTIONS[call.name](**arguments)
                print(f"[Agent] Tool completed: {call.name}")

                # Automatically prepare a handoff if an order is not found.
                if (
                    call.name == "get_order_status"
                    and tool_result.get("found") is False
                ):
                    handoff = escalate_to_support(
                        "Order cannot be found in the demo database"
                    )
                    tool_result["support_handoff"] = handoff
            except (KeyError, TypeError, ValueError) as error:
                tool_result = {
                    "error": f"Tool execution failed: {error}"
                }
            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": json.dumps(tool_result),
                }
            )

        response = client.responses.create(
            model=MODEL,
            previous_response_id=response.id,
            input=tool_outputs,
            tools=TOOLS,
        )

    return (
        "I couldn't complete the request within the allowed tool-use steps. "
        "Please contact ShopEase support."
    )

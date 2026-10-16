
from src.agent_tools import (
    get_order_status,
    lookup_policy,
    escalate_to_support,
)


def test_get_order_status_for_existing_order():
    result = get_order_status("ORD-1001")

    assert result["found"] is True
    assert result["status"] == "Shipped"


def test_get_order_status_for_unknown_order():
    result = get_order_status("ORD-9999")

    assert result["found"] is False


def test_lookup_refund_policy():
    result = lookup_policy("refund")

    assert result["found"] is True
    assert "5–7 business days" in result["policy"]


def test_unknown_policy():
    result = lookup_policy("exchange")

    assert result["found"] is False


def test_escalation_is_demo_only():
    result = escalate_to_support("Unknown order")

    assert result["escalated"] is True
    assert "No real support ticket has been created." in result["message"]


from unittest.mock import patch

from src.agent import run_agent


def test_unknown_order_prepares_support_handoff():
    with patch("src.agent.client.responses.create") as mock_create:
        mock_create.return_value.output = [
            type(
                "FunctionCall",
                (),
                {
                    "type": "function_call",
                    "name": "get_order_status",
                    "arguments": '{"order_id": "ORD-9999"}',
                    "call_id": "call_test_123",
                },
            )()
        ]
        mock_create.return_value.id = "response_test_1"

        # The second response ends the tool loop.
        final_response = type(
            "FinalResponse",
            (),
            {
                "output": [],
                "output_text": (
                    "The order was not found. A demo support handoff "
                    "has been prepared."
                ),
            },
        )()
        mock_create.side_effect = [
            mock_create.return_value,
            final_response,
        ]

        result = run_agent(
            "Please track order ORD-9999."
        )

        assert "order was not found" in result.lower()
        assert "support handoff" in result.lower()


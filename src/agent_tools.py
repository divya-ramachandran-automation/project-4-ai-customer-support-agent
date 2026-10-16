
"""Tools available to the ShopEase customer support agent."""

ORDERS = {
    "ORD-1001": {
        "status": "Shipped",
        "estimated_delivery": "Within 2 business days",
    },
    "ORD-1002": {
        "status": "Processing",
        "estimated_delivery": "Not yet available",
    },
    "ORD-1003": {
        "status": "Delivered",
        "estimated_delivery": "Already delivered",
    },
}


def get_order_status(order_id: str) -> dict:
    """Look up a fictional order in the demo order database."""
    order = ORDERS.get(order_id.strip().upper())

    if order is None:
        return {
            "found": False,
            "message": "Order not found. Check the order ID or contact support.",
        }

    return {
        "found": True,
        "order_id": order_id.strip().upper(),
        **order,
    }


def lookup_policy(topic: str) -> dict:
    """Look up a customer support policy."""
    policies = {
        "delivery": (
            "Standard delivery usually takes 3–5 business days after shipment."
        ),
        "refund": (
            "After an approved return is received and inspected, "
            "refunds are generally processed within 5–7 business days."
        ),
        "return": (
            "Eligible unused products can be returned within 30 days "
            "of delivery, subject to applicable restrictions."
        ),
        "cancellation": (
            "Orders can generally be cancelled before shipment. "
            "Cancellation may no longer be possible after shipment."
        ),
    }

    normalized_topic = topic.strip().lower()

    if normalized_topic not in policies:
        return {
            "found": False,
            "message": "No matching policy was found. Contact support.",
        }

    return {
        "found": True,
        "topic": normalized_topic,
        "policy": policies[normalized_topic],
    }


def escalate_to_support(reason: str) -> dict:
    """Prepare a demo support handoff; does not contact a real team."""
    return {
        "escalated": True,
        "reason": reason,
        "message": (
            "A support handoff has been prepared in this demo. "
            "No real support ticket has been created."
        ),
    }

"""The API's answers the specs are given, each as the document gives it."""

import json


def json_of(value: object) -> str:
    """The value as JSON, each object's members in the order of their names."""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def document(id: str, name: str) -> dict[str, object]:
    """A document of the draft, ready, by its id and its name."""
    return {
        "id": id,
        "name": name,
        "size_bytes": 20480,
        "page_count": 2,
        "status": "ready",
        "url": f"https://example.com/{id}.pdf",
    }


def fax(**changes: object) -> dict[str, object]:
    """fax_1, a fax you sent that was delivered, with each member changes names in place of its
    own."""
    return {
        "id": "fax_1",
        "direction": "sent",
        "status": "delivered",
        "step": None,
        "office_id": None,
        "to_number": "+12025550143",
        "from_number": "+12025550100",
        "pages": 2,
        "price": None,
        "sent_at": "2026-11-07T02:00:00Z",
        "finished_at": "2026-11-07T02:03:00Z",
        "retry_at": None,
        "failure": None,
        "time_zone": "America/New_York",
        "sender_name": None,
        "cover_confidential": False,
        **changes,
    }


def page(*items: object) -> dict[str, object]:
    """A page of a list holding the items, with no page after it."""
    return {"data": list(items), "has_more": False, "next_cursor": None}


def refusal(code: str, message: str) -> dict[str, object]:
    """The API's refusal, by its code and its sentence."""
    error: dict[str, object] = {
        "code": code,
        "message": message,
        "details": [],
        "request_id": "req_1",
        "doc_url": None,
    }
    return {"error": error}


# GET /quote's answer for a fax of one page.
QUOTE: dict[str, object] = {
    "pages": 1,
    "price": {"amount_minor": 100, "currency": "USD"},
    "price_shown": "$1.00",
    "terms": "The stand-in’s terms.",
    "price_list": "stand-in",
}

# An office of GET /offices, which takes Form 2848 from Ohio.
OFFICE: dict[str, object] = {
    "id": "stand-in-office",
    "name": "A stand-in office",
    "fax_number": "+12025550143",
    "fax_number_from_abroad": None,
    "applies_to": ["Ohio"],
    "takes": ["Form 2848"],
    "signed_in_ink": False,
    "confidential_cover": False,
    "sources": [{"title": "A stand-in page", "url": "https://example.com/office"}],
    "checked_on": "2026-11-01",
}

# GET /plan's answer for a client with no plan.
NO_PLAN: dict[str, object] = {"plan": None}

# What the stand-in answers each operation's success with, by its operation id: no body for the two
# that answer 204.
SUCCESS: dict[str, str] = {
    "getQuote": json_of(QUOTE),
    "getDraft": json_of({"id": "fax_1", "documents": []}),
    "addDocument": json_of({"document": document("doc_1", "letter.pdf"), "upload": None}),
    "completeDocument": json_of(document("doc_1", "letter.pdf")),
    "removeDocument": "",
    "sendDraft": json_of(
        {
            "fax": fax(status="sending", step="queued", finished_at=None),
            "paid_by": "plan",
            "confirm_url": None,
        }
    ),
    "listFaxes": json_of(page(fax())),
    "getFax": json_of(fax()),
    "getConfirmation": json_of({"url": "https://example.com/confirmation.pdf"}),
    "getPlan": json_of(NO_PLAN),
    "listOffices": json_of(page(OFFICE)),
    "registerWebhookEndpoint": json_of(
        {
            "id": "endpoint_1",
            "url": "https://example.com/xipfax/events",
            "created_at": "2026-11-07T02:00:00Z",
            "secret": "whsec_c3RhbmQtaW4=",
        }
    ),
    "removeWebhookEndpoint": "",
}

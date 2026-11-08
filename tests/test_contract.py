"""Each of the SDK's calls sends the request the API's document asks for: its method and path on
the document's server, the key as a bearer token, the version, and every parameter and body as the
document's schemas take them. The calls are typed by the SDK, so mypy passes them only as the
generated code allows, and each request they send is read against the document itself, as each
answer the stand-in gives is. Each event the document posts is typed by the SDK as FaxEvent, which
the document takes as the SDK writes it."""

import json
from collections.abc import Callable

import pytest

from tests import answers
from tests.contract import Operation, load
from tests.standin import StandIn, same
from xipfax_sdk import API_VERSION, XipFax
from xipfax_sdk.api.draft import (
    add_document,
    complete_document,
    get_draft,
    remove_document,
    send_draft,
)
from xipfax_sdk.api.faxes import get_confirmation, get_fax, list_faxes
from xipfax_sdk.api.offices import list_offices
from xipfax_sdk.api.plan import get_plan
from xipfax_sdk.api.quote import get_quote
from xipfax_sdk.api.webhook_endpoints import register_webhook_endpoint, remove_webhook_endpoint
from xipfax_sdk.models import APIError, Fax, FaxEvent, NewDocument, NewWebhookEndpoint, SendDraft

API_KEY = "xipfax_key_live_example"

# One call of each operation, by its operation id, with arguments the document takes: each answers
# what its call answered.
CALLS: dict[str, Callable[[XipFax], object]] = {
    "getQuote": lambda xipfax: get_quote.sync(client=xipfax, pages=3),
    "getDraft": lambda xipfax: get_draft.sync(client=xipfax),
    "addDocument": lambda xipfax: add_document.sync(
        client=xipfax,
        body=NewDocument(name="letter.pdf", url="https://example.com/letter.pdf"),
        idempotency_key="add-letter-1",
    ),
    "completeDocument": lambda xipfax: complete_document.sync(
        "doc_1", client=xipfax, idempotency_key="complete-letter-1"
    ),
    "removeDocument": lambda xipfax: remove_document.sync("doc_1", client=xipfax),
    "sendDraft": lambda xipfax: send_draft.sync(
        client=xipfax,
        body=SendDraft(fax_number="+1 202 555 0143", document_ids=["doc_1"]),
        idempotency_key="send-letter-1",
    ),
    "listFaxes": lambda xipfax: list_faxes.sync(
        client=xipfax, limit=20, starting_after="fax_0", direction="sent"
    ),
    "getFax": lambda xipfax: get_fax.sync("fax_1", client=xipfax),
    "getConfirmation": lambda xipfax: get_confirmation.sync("fax_1", client=xipfax),
    "getPlan": lambda xipfax: get_plan.sync(client=xipfax),
    "listOffices": lambda xipfax: list_offices.sync(
        client=xipfax, search="Form 2848", place="OH", limit=5, starting_after="office_0"
    ),
    "registerWebhookEndpoint": lambda xipfax: register_webhook_endpoint.sync(
        client=xipfax,
        body=NewWebhookEndpoint(url="https://example.com/xipfax/events"),
        idempotency_key="register-endpoint-1",
    ),
    "removeWebhookEndpoint": lambda xipfax: remove_webhook_endpoint.sync(
        "endpoint_1", client=xipfax
    ),
}


def test_the_sdk_has_a_call_for_every_operation_the_document_names_and_no_other() -> None:
    assert sorted(CALLS) == sorted(operation.id for operation in load().operations)


def test_the_sdk_names_the_version_the_document_is_the_one_xip_version_takes() -> None:
    document = load()

    assert API_VERSION == document.version
    for operation in document.operations:
        assert document.version_refused(operation, API_VERSION) == [], operation.id


@pytest.mark.parametrize("operation", load().operations, ids=lambda operation: operation.id)
def test_each_call_sends_its_request_as_the_document_asks(operation: Operation) -> None:
    answer = answers.SUCCESS[operation.id]
    stand_in = StandIn(same(operation.success, answer))
    xipfax = XipFax(API_KEY, httpx_args={"transport": stand_in.transport})

    answered = CALLS[operation.id](xipfax)

    assert not isinstance(answered, APIError), answered
    assert len(stand_in.requests) == 1, stand_in.requests
    request = stand_in.requests[0]
    assert request.headers.get_list("Authorization") == [f"Bearer {API_KEY}"]
    assert load().read_request(request, API_VERSION) == (operation.id, [])
    assert load().read_answer(request, operation.success, answer) == []


def test_each_event_the_document_posts_is_a_fax_event_it_takes() -> None:
    document = load()
    # The fax each event tells of, by the event's type: one for each type the document posts.
    faxes = {
        "fax.delivered": answers.fax(price={"amount_minor": 100, "currency": "USD"}),
        "fax.failed": answers.fax(status="failed", failure="busy"),
        "fax.received": answers.fax(
            id="fax_2",
            direction="received",
            status="received",
            from_number="+12025550111",
            to_number="+12025550100",
            pages=3,
            finished_at=None,
            time_zone=None,
        ),
    }
    assert sorted(document.webhooks) == sorted(faxes)

    for name, fax in faxes.items():
        event = FaxEvent(
            id="event_1",
            type_=name,
            api_version=API_VERSION,
            created_at="2026-11-07T02:03:00Z",
            data=Fax.from_dict(fax),
        )
        written = json.loads(json.dumps(event.to_dict()))

        assert document.check(document.webhooks[name], written, name) == [], name
        assert FaxEvent.from_dict(written).data.id == fax["id"], name

"""XipFax, the client each call takes: it starts only with a key, sends to the API's own address
unless given another, keeps its key to itself, names the version the SDK is generated from on every
request, keeps both through a copy, answers a refusal as the API's own error and raises on a status
the document doesn't give, and reads an answer that gains a member."""

from typing import Any

import pytest

from tests import answers
from tests.standin import StandIn, same
from xipfax_sdk import API_VERSION, XipFax, errors
from xipfax_sdk.api.faxes import get_fax
from xipfax_sdk.api.plan import get_plan
from xipfax_sdk.models import APIError, Fax

NO_PLAN = answers.json_of(answers.NO_PLAN)


def client_of(key: str, stand_in: StandIn, **options: Any) -> XipFax:
    """A client of key whose every request goes to the stand-in, with the options given."""
    return XipFax(key, httpx_args={"transport": stand_in.transport}, **options)


def keys_of(stand_in: StandIn) -> list[list[str]]:
    """The Authorization each request to the stand-in sent, in their order."""
    return [request.headers.get_list("Authorization") for request in stand_in.requests]


@pytest.mark.parametrize("key", [None, "", "   "])
def test_xipfax_refuses_to_start_without_a_key(key: str | None) -> None:
    with pytest.raises(TypeError, match="XipFax needs your API key"):
        XipFax(key)


def test_xipfax_sends_to_the_apis_own_address_unless_given_another() -> None:
    own = StandIn(same(200, NO_PLAN))
    other = StandIn(same(200, NO_PLAN))

    get_plan.sync(client=client_of("key-a", own))
    get_plan.sync(client=client_of("key-a", other, base_url="https://api.example.com/"))

    assert [str(request.url) for request in own.requests] == ["https://api.xipfax.com/plan"]
    assert [str(request.url) for request in other.requests] == ["https://api.example.com/plan"]


def test_each_client_keeps_its_key_to_itself() -> None:
    a = StandIn(same(200, NO_PLAN))
    b = StandIn(same(200, NO_PLAN))

    get_plan.sync(client=client_of("key-a", a))
    get_plan.sync(client=client_of("key-b", b))

    assert keys_of(a) == [["Bearer key-a"]]
    assert keys_of(b) == [["Bearer key-b"]]


def test_each_request_names_the_version_the_sdk_is_generated_from() -> None:
    stand_in = StandIn(same(200, NO_PLAN))

    get_plan.sync(client=client_of("key-a", stand_in))

    assert stand_in.requests[0].headers.get_list("Xip-Version") == [API_VERSION]


def test_a_copy_with_more_headers_keeps_the_key_and_the_version() -> None:
    stand_in = StandIn(same(200, NO_PLAN))
    copied = client_of("key-a", stand_in).with_headers({"X-Trace": "trace-1"})

    get_plan.sync(client=copied)

    request = stand_in.requests[0]
    assert request.headers.get_list("Authorization") == ["Bearer key-a"]
    assert request.headers.get_list("Xip-Version") == [API_VERSION]
    assert request.headers.get_list("X-Trace") == ["trace-1"]


def test_xipfax_shows_no_key_when_printed() -> None:
    xipfax = XipFax("xipfax_key_live_example")

    assert repr(xipfax) == "XipFax(base_url='https://api.xipfax.com')"


def test_a_refusal_is_the_apis_own_error() -> None:
    refusal = answers.refusal("authentication_failed", "That key isn’t one of XipFax’s.")
    stand_in = StandIn(same(401, answers.json_of(refusal)))

    answer = get_plan.sync_detailed(client=client_of("key-a", stand_in))

    assert answer.status_code == 401
    assert isinstance(answer.parsed, APIError)
    assert answer.parsed.error.code == "authentication_failed"
    assert answer.parsed.error.request_id == "req_1"


def test_a_status_the_document_doesnt_give_raises_unexpected_status() -> None:
    stand_in = StandIn(same(418, ""))

    with pytest.raises(errors.UnexpectedStatus):
        get_plan.sync(client=client_of("key-a", stand_in))


def test_an_answer_that_gains_a_member_is_read_and_carries_it_through() -> None:
    # The document's Additions rule: within a version, an answer may gain a member, and an open set
    # a new value. Here the fax gains tracking, and its status is one the SDK has never seen.
    gained = answers.fax(status="archived", tracking={"carrier": "stand-in"})
    stand_in = StandIn(same(200, answers.json_of(gained)))

    fax = get_fax.sync("fax_1", client=client_of("key-a", stand_in))

    assert isinstance(fax, Fax)
    assert fax.status == "archived"
    assert fax.to_dict()["tracking"] == {"carrier": "stand-in"}

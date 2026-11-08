"""The quickstart, walked against a stand-in of the API that answers as the document says: its free
steps first, its charged step said before it and taken only on send, and each request it sends read
against the document, as each answer the stand-in gives is."""

import json
from dataclasses import dataclass

import httpx
import pytest

from examples.quickstart import READ_EVERY, REAL_AND_CHARGED, Given, Refused, name_of, quickstart
from tests import answers
from tests.contract import load
from tests.standin import StandIn
from xipfax_sdk import API_VERSION, XipFax

API_KEY = "xipfax_key_live_example"
FAX_NUMBER = "+1 202 555 0143"
PDF_LINK = "https://example.com/letter.pdf"

# The API's refusal of a send whose documents aren't the draft's.
CHANGED = "Your fax changed since this page showed it. Look it over, then send it again."


class API:
    """The API as the quickstart finds it: its draft holding documents to begin with, and
    added_on_xipfax too once the quickstart adds its own, as documents the client adds on xipfax.com
    meanwhile, each by its id."""

    def __init__(self, documents: list[str], added_on_xipfax: list[str]) -> None:
        self.documents = list(documents)
        self.added_on_xipfax = added_on_xipfax
        self.reads = 0
        # Each request, line and question of the walk, in its order.
        self.events: list[str] = []
        # What the document refuses in each answer the stand-in gave.
        self.refused: list[str] = []

    def answer(self, request: httpx.Request) -> tuple[int, str]:
        """Answers a request as the API would, and reads the answer against the document."""
        route = f"{request.method} {request.url.path}"
        self.events.append(route)
        status, body = self.route(route, request.content)
        self.refused += load().read_answer(request, status, body)
        return status, body

    def route(self, route: str, body: bytes) -> tuple[int, str]:
        """The status and the body the API answers a route with."""
        match route:
            case "GET /quote":
                return 200, answers.SUCCESS["getQuote"]
            case "GET /offices":
                return 200, answers.SUCCESS["listOffices"]
            case "GET /draft":
                documents = [answers.document(id, "letter.pdf") for id in self.documents]
                return 200, answers.json_of({"id": "fax_1", "documents": documents})
            case "POST /draft/documents":
                self.documents += ["doc_1", *self.added_on_xipfax]
                return 201, answers.SUCCESS["addDocument"]
            case "DELETE /draft/documents/doc_1":
                self.documents.remove("doc_1")
                return 204, ""
            case "POST /draft/send":
                # As the API does, it sends a draft only where the send names its documents, in
                # their order.
                if json.loads(body).get("document_ids") != self.documents:
                    return 409, answers.json_of(answers.refusal("draft_changed", CHANGED))
                return 200, answers.SUCCESS["sendDraft"]
            case "GET /faxes/fax_1":
                self.reads += 1
                if self.reads < 2:
                    sending = answers.fax(status="sending", step="sending", finished_at=None)
                    return 200, answers.json_of(sending)
                return 200, answers.SUCCESS["getFax"]
            case "GET /faxes/fax_1/confirmation":
                return 200, answers.SUCCESS["getConfirmation"]
        return 404, ""


@dataclass
class Walk:
    """What a walk saw: each request, line and question in its order, the requests themselves, the
    refusal that stopped the quickstart, if one did, and each pause between reads of the fax."""

    events: list[str]
    requests: list[httpx.Request]
    refused: Refused | None
    pauses: list[float]

    def routes(self) -> list[str]:
        """The walk's requests alone, by their routes."""
        return [event for event in self.events if not event.startswith(("say: ", "ask: "))]

    def sent(self) -> object:
        """The body of the walk's POST /draft/send."""
        for request in self.requests:
            if request.method == "POST" and request.url.path == "/draft/send":
                return json.loads(request.content)
        raise AssertionError("the walk sent no POST /draft/send")


def walk_of(
    draft: list[str], added_on_xipfax: list[str], typed: str, to: str, pdf_url: str
) -> Walk:
    """Walks the quickstart against the API, its draft holding draft and gaining added_on_xipfax,
    typed being what you type when it asks, and holds each request it sent, and each answer it was
    given, to the document."""
    api = API(draft, added_on_xipfax)
    stand_in = StandIn(api.answer)
    xipfax = XipFax(API_KEY, httpx_args={"transport": stand_in.transport})

    def say(line: str) -> None:
        api.events.append(f"say: {line}")

    def ask(question: str) -> str:
        api.events.append(f"ask: {question}")
        return typed

    pauses: list[float] = []

    def pause(seconds: float) -> None:
        pauses.append(seconds)

    refused: Refused | None = None
    try:
        quickstart(xipfax, Given(to=to, pdf_url=pdf_url, say=say, ask=ask, pause=pause))
    except Refused as refusal:
        refused = refusal

    for request in stand_in.requests:
        operation, wrong = load().read_request(request, API_VERSION)
        assert wrong == [], f"{request.method} {request.url}, {operation}"
    assert api.refused == [], "the stand-in's answers are the document's"
    return Walk(api.events, stand_in.requests, refused, pauses)


def test_the_quickstart_takes_the_free_steps_alone_where_it_has_no_number_or_pdf() -> None:
    walk = walk_of([], [], "send", "", "")

    assert walk.refused is None
    assert walk.routes() == ["GET /quote", "GET /offices"]
    assert not any(event.startswith("ask: ") for event in walk.events)


def test_the_quickstart_says_the_fax_is_real_and_charged_sends_it_on_send_and_follows_it() -> None:
    walk = walk_of([], [], "send", FAX_NUMBER, PDF_LINK)

    assert walk.refused is None
    assert walk.routes() == [
        "GET /quote",
        "GET /offices",
        "GET /draft",
        "POST /draft/documents",
        "POST /draft/send",
        "GET /faxes/fax_1",
        "GET /faxes/fax_1",
        "GET /faxes/fax_1/confirmation",
    ]
    added = walk.events.index("POST /draft/documents")
    warned = walk.events.index(f"say: {REAL_AND_CHARGED}")
    asked = next(index for index, event in enumerate(walk.events) if event.startswith("ask: "))
    sent = walk.events.index("POST /draft/send")
    assert added < warned < asked < sent, walk.events
    assert "say: Added letter.pdf, 2 pages." in walk.events
    assert walk.pauses == [READ_EVERY, READ_EVERY]
    assert walk.sent() == {"fax_number": FAX_NUMBER, "document_ids": ["doc_1"]}
    posts = [request for request in walk.requests if request.method == "POST"]
    keys = {request.headers["Idempotency-Key"] for request in posts}
    assert len(keys) == len(posts), keys


def test_the_quickstart_sends_nothing_on_any_other_answer_and_takes_its_document_out() -> None:
    walk = walk_of([], [], "no", FAX_NUMBER, PDF_LINK)

    assert walk.refused is None
    assert walk.routes() == [
        "GET /quote",
        "GET /offices",
        "GET /draft",
        "POST /draft/documents",
        "DELETE /draft/documents/doc_1",
    ]


def test_the_quickstart_names_only_its_own_document_so_a_draft_that_gained_one_is_refused() -> None:
    walk = walk_of([], ["doc_2"], "send", FAX_NUMBER, PDF_LINK)

    assert walk.refused is not None
    assert walk.refused.refusal.error.code == "draft_changed"
    assert walk.routes() == [
        "GET /quote",
        "GET /offices",
        "GET /draft",
        "POST /draft/documents",
        "POST /draft/send",
    ]
    assert walk.sent() == {"fax_number": FAX_NUMBER, "document_ids": ["doc_1"]}


def test_the_quickstart_adds_nothing_to_a_draft_that_already_holds_documents() -> None:
    walk = walk_of(["doc_0"], [], "send", FAX_NUMBER, PDF_LINK)

    assert walk.refused is None
    assert walk.routes() == ["GET /quote", "GET /offices", "GET /draft"]


@pytest.mark.parametrize(
    ("link", "name"),
    [
        ("https://example.com/letter.pdf", "letter.pdf"),
        ("https://example.com/forms/Form%202848.pdf", "Form 2848.pdf"),
        ("https://example.com/forms/", "forms"),
        ("https://example.com", "document.pdf"),
        ("https://example.com/%FF.pdf", "%FF.pdf"),
        ("https://example.com/" + "é" * 300, "é" * 255),
    ],
)
def test_the_document_is_named_as_its_link_ends(link: str, name: str) -> None:
    assert name_of(link) == name

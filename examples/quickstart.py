r"""XipFax's quickstart through the SDK, the steps of
https://developer.xipfax.com/docs/guides/quickstart/ in their order. The free steps come first: a
quote, and the offices that take a form. Then, only where you name a fax number of yours and a PDF,
a real fax, charged, which it says before it sends, and sends only once you type send.

Run it from a clone of this repository, with uv::

    uv sync
    XIPFAX_API_KEY=xipfax_key_live_… uv run python examples/quickstart.py

That takes the free steps alone. To send a fax too, real and charged, name a fax number of yours
and a public link to a PDF::

    XIPFAX_TO='+1 202 555 0143' XIPFAX_PDF_URL=https://example.com/letter.pdf \
      XIPFAX_API_KEY=xipfax_key_live_… uv run python examples/quickstart.py
"""

import contextlib
import os
import sys
import time
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar
from urllib.parse import unquote_to_bytes, urlsplit

from xipfax_sdk import XipFax
from xipfax_sdk.api.draft import add_document, get_draft, remove_document, send_draft
from xipfax_sdk.api.faxes import get_confirmation, get_fax
from xipfax_sdk.api.offices import list_offices
from xipfax_sdk.api.quote import get_quote
from xipfax_sdk.models import APIError, DraftDocument, NewDocument, SendDraft

# How long the quickstart waits between reads of the fax, in seconds, and how many it makes.
READ_EVERY = 10
READS = 30

# What the step that sends says first, as the docs' quickstart says it.
REAL_AND_CHARGED = (
    "This step sends a real fax, and it’s charged. It goes to the number you name, so name one "
    "of your own. Its pages count on your plan, or where you have no plan its price is held on "
    "the card you saved, and taken once it’s delivered. A fax that fails costs nothing."
)

T = TypeVar("T")


@dataclass
class Given:
    """What the quickstart is given, and how it talks to you."""

    # A fax number of yours, where the fax goes. Without it, only the free steps run.
    to: str
    # A public https link to a PDF, the fax's pages. Without it, only the free steps run.
    pdf_url: str
    # Tells you a line.
    say: Callable[[str], None]
    # Asks you a question, answering what you typed.
    ask: Callable[[str], str]
    # Waits so many seconds between reads of the fax.
    pause: Callable[[float], None]


class Refused(Exception):
    """The API's refusal, which stops the quickstart: refusal is the APIError it answered."""

    def __init__(self, refusal: APIError) -> None:
        super().__init__(f"XipFax refused it, {refusal.error.code}: {refusal.error.message}")
        self.refusal = refusal


def quickstart(xipfax: XipFax, given: Given) -> None:
    """Takes the quickstart's steps. The API's refusal stops it, raised as Refused, which main
    prints."""
    # 1. What a fax costs. This costs nothing, and it shows your key works.
    quote = answered(get_quote.sync(client=xipfax, pages=1))
    given.say(f"A one-page fax costs {quote.price_shown} without a plan: {quote.terms}")

    # 2. Where a form goes: the offices that take Form 2848 from Ohio, and their numbers. Also free.
    offices = answered(list_offices.sync(client=xipfax, search="Form 2848", place="OH", limit=3))
    for office in offices.data:
        given.say(f"{office.name} takes Form 2848 at {office.fax_number}.")

    if not given.to or not given.pdf_url:
        return

    # 3. Your draft, the fax you prepare. This sends only its own document, so it starts empty.
    draft = answered(get_draft.sync(client=xipfax))
    if draft.documents:
        given.say(
            "Your draft already holds documents. Send or remove them on xipfax.com first, so that "
            "this sends only its own."
        )
        return

    # 4. Add the PDF by its link. Each POST names a key of its own, so a retry can't add it twice.
    document = NewDocument(name=name_of(given.pdf_url), url=given.pdf_url)
    added = answered(add_document.sync(client=xipfax, body=document, idempotency_key=new_key()))
    given.say(f"Added {added.document.name}{pages_of(added.document)}.")

    # 5. Send it, a real fax, charged: said first, and sent only once you type send.
    given.say(REAL_AND_CHARGED)
    typed = given.ask(f"Type send to fax it to {given.to}, or anything else to stop: ")
    if typed.strip().lower() != "send":
        removed = remove_document.sync(added.document.id, client=xipfax)
        if isinstance(removed, APIError):
            raise Refused(removed)
        given.say("Nothing was sent, and the document is out of your draft again.")
        return
    # The send names the documents to send: the one this added, alone. A draft whose documents
    # aren't these is refused, so that nothing you didn't name is sent.
    send = SendDraft(fax_number=given.to, document_ids=[added.document.id])
    sent = answered(send_draft.sync(client=xipfax, body=send, idempotency_key=new_key()))
    if sent.confirm_url:
        given.say(
            f"Nothing was sent or held: the fax waits for you on xipfax.com, {sent.confirm_url}"
        )
        return
    given.say(f"Sent, paid by {sent.paid_by}: fax {sent.fax.id}.")

    # 6. Follow the fax until it's delivered or fails, then read its confirmation.
    fax, shown = sent.fax, ""
    for _ in range(READS):
        if fax.status in ("delivered", "failed"):
            break
        given.pause(READ_EVERY)
        fax = answered(get_fax.sync(fax.id, client=xipfax))
        stands = f"{fax.status}: {fax.step}" if fax.step else fax.status
        if stands != shown:
            given.say(stands)
        shown = stands
    if fax.status == "delivered":
        confirmation = answered(get_confirmation.sync(fax.id, client=xipfax))
        given.say(f"Its confirmation, readable for a few minutes: {confirmation.url}")
    elif fax.status == "failed":
        given.say(f"It failed, {fax.failure}, so it costs nothing.")
    else:
        given.say(
            f"It's still {fax.status}. Read it later: get_fax.sync({fax.id!r}, client=xipfax)."
        )


def answered(answer: T | APIError | None) -> T:
    """The API's answer, or its refusal raised as Refused."""
    if isinstance(answer, APIError):
        raise Refused(answer)
    if answer is None:
        # XipFax raises errors.UnexpectedStatus for a status the document doesn't give, so only a
        # client made to answer None for one gives None here.
        raise RuntimeError("XipFax answered with a status its document doesn't give")
    return answer


def new_key() -> str:
    """A key of a request's own for its Idempotency-Key, a random UUID."""
    return str(uuid.uuid4())


def name_of(link: str) -> str:
    """The PDF's name, as its link ends: letter.pdf."""
    try:
        path = urlsplit(link).path
    except ValueError:
        path = ""
    segments = [segment for segment in path.split("/") if segment]
    name = segments[-1] if segments else "document.pdf"
    # A link whose name isn't percent-encoded text keeps it as it is.
    with contextlib.suppress(UnicodeDecodeError):
        name = unquote_to_bytes(name).decode()
    return name[:255]


def pages_of(document: DraftDocument) -> str:
    """The document's pages, once XipFax has counted them."""
    if document.page_count is None:
        return ""
    return ", 1 page" if document.page_count == 1 else f", {document.page_count} pages"


def ask(question: str) -> str:
    """Asks in the terminal, answering the line typed. A terminal that closes answers what was typed
    before it did, which sends only if that was send."""
    try:
        return input(question)
    except EOFError:
        return ""


def main() -> None:
    """Runs the quickstart in your terminal, as this module's docstring shows."""
    key = os.environ.get("XIPFAX_API_KEY", "")
    if not key.strip():
        sys.exit(
            "Set XIPFAX_API_KEY to a key you made in the developer console: "
            "https://developer.xipfax.com/console/"
        )
    to, pdf_url = os.environ.get("XIPFAX_TO", ""), os.environ.get("XIPFAX_PDF_URL", "")
    given = Given(to=to, pdf_url=pdf_url, say=print, ask=ask, pause=time.sleep)
    try:
        quickstart(XipFax(key), given)
    except Refused as refused:
        sys.exit(str(refused))
    if not to or not pdf_url:
        print(
            "Those steps cost nothing. To send a fax too, run it again with XIPFAX_TO, a fax "
            "number of yours, and XIPFAX_PDF_URL, a public link to a PDF."
        )


if __name__ == "__main__":
    main()

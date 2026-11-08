"""The reader is held to failing too: each thing the document refuses in a request or an answer is
refused, by name, so that a spec reading the SDK's requests as fitting can fail."""

import httpx

from tests import answers
from tests.contract import load

# The version the document is, which each request's Xip-Version names.
VERSION = load().version

ADD_DOCUMENT = "https://api.xipfax.com/draft/documents"
REMOVE_DOCUMENT = "https://api.xipfax.com/draft/documents/doc_1"


def request_of(
    method: str, address: str, headers: list[tuple[str, str]], body: str = ""
) -> httpx.Request:
    """A request of method to address, with the headers and the body given."""
    return httpx.Request(method, address, headers=headers, content=body.encode())


def signed(*more: tuple[str, str]) -> list[tuple[str, str]]:
    """The key and the version as the SDK sends them, then each header more gives."""
    key = ("Authorization", "Bearer xipfax_key_live_example")
    return [key, ("Xip-Version", VERSION), *more]


def as_json(idempotency_key: str) -> list[tuple[str, str]]:
    """The headers of a request with a JSON body, signed and with its idempotency key."""
    return signed(("Content-Type", "application/json"), ("Idempotency-Key", idempotency_key))


def test_the_reader_takes_a_request_that_fits() -> None:
    request = request_of("GET", "https://api.xipfax.com/quote?pages=3", signed())

    operation, refused = load().read_request(request, VERSION)

    assert operation == "getQuote"
    assert refused == []


def test_the_reader_refuses_no_key_two_versions_too_many_pages_and_an_unknown_parameter() -> None:
    twice = [("Xip-Version", VERSION), ("Xip-Version", VERSION)]
    request = request_of("GET", "https://api.xipfax.com/quote?pages=251&color=red", twice)

    operation, refused = load().read_request(request, VERSION)

    assert operation == "getQuote"
    assert refused == [
        "Authorization is [], not one bearer key",
        f'Xip-Version is ["{VERSION}" "{VERSION}"], not {VERSION}',
        "header Xip-Version is sent 2 times",
        "query pages is 251, past its maximum of 250",
        "query color is no parameter of getQuote",
    ]


def test_the_reader_refuses_a_member_it_doesnt_take_a_size_under_the_least_and_no_name() -> None:
    body = '{"size_bytes":0,"colour":"red"}'
    request = request_of("POST", ADD_DOCUMENT, as_json("add-letter-1"), body)

    operation, refused = load().read_request(request, VERSION)

    assert operation == "addDocument"
    assert refused == [
        "body.colour is no member it takes",
        "body.size_bytes is 0, past its minimum of 1",
        "body.name is missing",
    ]


def test_the_reader_reads_a_patterns_end_as_the_end_of_the_text() -> None:
    # Python's $ also matches before a last line break, where the document's pattern doesn't: a name
    # that ends in one is refused.
    body = '{"name":"letter.pdf\\n"}'
    request = request_of("POST", ADD_DOCUMENT, as_json("add-letter-1"), body)

    operation, refused = load().read_request(request, VERSION)

    assert operation == "addDocument"
    assert refused == [
        r'body.name is "letter.pdf\n", not of the pattern ^[^\p{Cc}\p{Zl}\p{Zp}]+$',
    ]


def test_the_reader_refuses_a_body_where_the_operation_takes_none() -> None:
    request = request_of("DELETE", REMOVE_DOCUMENT, signed(), "{}")

    operation, refused = load().read_request(request, VERSION)

    assert operation == "removeDocument"
    assert refused == ["a body the operation takes none of"]


def test_the_reader_refuses_a_request_to_another_server() -> None:
    request = request_of("GET", "https://api.example.com/quote?pages=3", signed())

    operation, refused = load().read_request(request, VERSION)

    assert operation == ""
    assert refused == [
        "GET https://api.example.com/quote?pages=3 is no operation of the document",
    ]


def test_the_reader_refuses_a_fax_whose_pages_are_words_and_whose_status_it_doesnt_list() -> None:
    request = request_of("GET", "https://api.xipfax.com/faxes/fax_1", [])
    answer = answers.json_of(answers.fax(pages="two", status="archived"))

    assert load().read_answer(request, 200, answer) == [
        "answer.pages is string, not [integer null]",
        "answer.status is archived, none of [draft sending delivered failed received]",
    ]


def test_the_reader_refuses_a_status_the_operation_doesnt_give() -> None:
    request = request_of("GET", "https://api.xipfax.com/plan", [])

    assert load().read_answer(request, 418, "") == ["getPlan gives no 418"]


def test_the_reader_refuses_a_body_where_the_answer_carries_none() -> None:
    request = request_of("DELETE", REMOVE_DOCUMENT, [])

    assert load().read_answer(request, 204, "{}") == ["removeDocument's 204 carries no body"]


def test_the_reader_refuses_a_schema_keyword_it_doesnt_read() -> None:
    schema: dict[str, object] = {"oneOf": [{"type": "string"}]}

    assert load().check(schema, "text", "value") == [
        "value: the contract reads no oneOf, which its schema gives",
    ]


def test_the_reader_refuses_a_pattern_python_would_read_otherwise() -> None:
    # Python's . matches a carriage return and a line or paragraph separator, which ECMA-262's
    # doesn't, so a pattern with one outside a set is refused rather than read wrong.
    refused = load().check({"pattern": "^a.b$"}, "a-b", "value")

    assert refused == [
        "value: its pattern ^a.b$ doesn't compile: the specs read no . outside a set of characters",
    ]

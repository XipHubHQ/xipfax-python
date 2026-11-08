"""The stand-in, which answers the SDK's requests in place of the API in the specs: an httpx
transport that keeps each request it is given, its body read, and answers it as its answer says.
Nothing it does reaches a network."""

from collections.abc import Callable

import httpx

# What the stand-in answers a request with: a status, and a JSON body or "" for none.
Answer = Callable[[httpx.Request], tuple[int, str]]


class StandIn:
    """The stand-in, which a client takes as its transport: httpx_args={"transport": ...}."""

    def __init__(self, answer: Answer) -> None:
        # Each request the stand-in was given, in its order.
        self.requests: list[httpx.Request] = []
        self.answer = answer
        self.transport = httpx.MockTransport(self.handle)

    def handle(self, request: httpx.Request) -> httpx.Response:
        """Keeps the request, whose body the transport has read, and answers it."""
        self.requests.append(request)
        status, body = self.answer(request)
        headers = {"Content-Type": "application/json"} if body else {}
        return httpx.Response(status, headers=headers, content=body.encode())


def same(status: int, body: str) -> Answer:
    """An answer of one status and one body, whatever the request."""

    def answer(request: httpx.Request) -> tuple[int, str]:
        return status, body

    return answer

"""XipFax, the client each of the SDK's calls takes."""

from typing import Any

from .api_version import API_VERSION
from .client import AuthenticatedClient

BASE_URL = "https://api.xipfax.com"


class XipFax(AuthenticatedClient):
    """XipFax's API, as each call in ``xipfax_sdk.api`` takes it. Every request carries your key as
    a bearer token, and the version of the API this SDK was generated from, ``API_VERSION``, in its
    ``Xip-Version`` header::

        from xipfax_sdk import XipFax
        from xipfax_sdk.api.quote import get_quote

        xipfax = XipFax(os.environ["XIPFAX_API_KEY"])
        quote = get_quote.sync(client=xipfax, pages=3)

    Args:
        api_key: Your API key, ``xipfax_key_live_…``, made in the developer console. Keep it on
            your server.
        base_url: Where the API answers: ``https://api.xipfax.com`` unless you name another.
        **options: What the generated ``AuthenticatedClient`` takes beside them, such as
            ``timeout``, ``headers`` or ``httpx_args``. ``raise_on_unexpected_status`` is True
            unless you name it: a status the document doesn't give raises
            ``errors.UnexpectedStatus``, rather than the call answering None.
    """

    __slots__ = ()

    def __init__(
        self, api_key: str | None = None, *, base_url: str = BASE_URL, **options: Any
    ) -> None:
        # with_headers, with_cookies and with_timeout copy a client by attrs.evolve, which gives
        # each of the generated client's fields by its own name: the key comes as token.
        token = options.pop("token", None)
        key = api_key if api_key is not None else token
        if not isinstance(key, str) or not key.strip():
            raise TypeError(
                "XipFax needs your API key: XipFax(api_key). Make one in the developer console, "
                "https://developer.xipfax.com/console/."
            )
        options.setdefault("raise_on_unexpected_status", True)
        headers = {**options.pop("headers", {}), "Xip-Version": API_VERSION}
        super().__init__(base_url=base_url, token=key, headers=headers, **options)

    def __repr__(self) -> str:
        # The generated client's own would show the key, and the Authorization header it keeps.
        return f"XipFax(base_url={self._base_url!r})"

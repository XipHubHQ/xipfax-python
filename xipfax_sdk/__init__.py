"""XipFax's API for Python, generated from its OpenAPI document.

``XipFax`` is the client each call in ``xipfax_sdk.api`` takes: it holds your API key, and names
``API_VERSION``, the version of the API the SDK was generated from, on every request.
"""

from .api_version import API_VERSION
from .xipfax import XipFax

__all__ = (
    "API_VERSION",
    "XipFax",
)

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="NewWebhookEndpoint")


@_attrs_define
class NewWebhookEndpoint:
    """A webhook endpoint to register: the URL of your own server that takes the events.

    Attributes:
        url (str): Where XipFax posts each event: https on its usual port, at an address on the internet, 2,048
            characters at most.
    """

    url: str

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "url": url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        new_webhook_endpoint = cls(
            url=url,
        )

        return new_webhook_endpoint

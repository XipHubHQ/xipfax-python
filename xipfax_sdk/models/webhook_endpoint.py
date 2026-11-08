from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WebhookEndpoint")


@_attrs_define
class WebhookEndpoint:
    """A webhook endpoint of your account, just registered: every event goes to it, signed with its own secret.

    Attributes:
        id (str): The endpoint, as `DELETE /webhook-endpoints/{endpoint_id}` names it.
        url (str): Where XipFax posts each event.
        created_at (str): When it was registered.
        secret (None | str): Its signing secret, `whsec_` and the base64 of its key, which signs every event posted to
            it: keep it now, as no other answer shows it. Null in an answer given again for a repeated `Idempotency-Key`.
    """

    id: str
    url: str
    created_at: str
    secret: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        url = self.url

        created_at = self.created_at

        secret: None | str
        secret = self.secret

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "url": url,
                "created_at": created_at,
                "secret": secret,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        url = d.pop("url")

        created_at = d.pop("created_at")

        def _parse_secret(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        secret = _parse_secret(d.pop("secret"))

        webhook_endpoint = cls(
            id=id,
            url=url,
            created_at=created_at,
            secret=secret,
        )

        webhook_endpoint.additional_properties = d
        return webhook_endpoint

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

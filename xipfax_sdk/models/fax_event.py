from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.fax import Fax


T = TypeVar("T", bound="FaxEvent")


@_attrs_define
class FaxEvent:
    """What XipFax tells your endpoint of a fax: one delivered, failed for good, or received.

    Attributes:
        id (str): The event, the same on every delivery of it, as `webhook-id` names it: take each once.
        type_ (str): What happened: `fax.delivered` once a fax you sent is delivered, `fax.failed` once one fails for
            good, and `fax.received` once a fax sent to your number arrives. An open set: ignore a type you don’t handle.
        api_version (str): The version `data` is in.
        created_at (str): When it happened.
        data (Fax): A fax of your log: one you sent, or one sent to your number.
    """

    id: str
    type_: str
    api_version: str
    created_at: str
    data: Fax
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_ = self.type_

        api_version = self.api_version

        created_at = self.created_at

        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type_,
                "api_version": api_version,
                "created_at": created_at,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fax import Fax  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        type_ = d.pop("type")

        api_version = d.pop("api_version")

        created_at = d.pop("created_at")

        data = Fax.from_dict(d.pop("data"))

        fax_event = cls(
            id=id,
            type_=type_,
            api_version=api_version,
            created_at=created_at,
            data=data,
        )

        fax_event.additional_properties = d
        return fax_event

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

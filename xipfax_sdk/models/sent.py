from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.fax import Fax


T = TypeVar("T", bound="Sent")


@_attrs_define
class Sent:
    """The draft sent: `fax` is the fax on its way, `sending`; or, where it waits for you on xipfax.com, your draft,
    `draft`, under the id the fax keeps once you send it.

        Attributes:
            fax (Fax): A fax of your log: one you sent, or one sent to your number.
            paid_by (None | str): How the fax is paid, once it is sent: `plan`, its pages counted on your plan; or `card`,
                its price held on the card you saved until it ends, taken once it is delivered and let go if it fails. Null
                where it isn’t sent, nothing held: `confirm_url` says where it waits. An open set: read what you know.
            confirm_url (None | str): Where the fax waits for you, where it isn’t sent: your draft on xipfax.com, once you
                sign in, where you look it over and send it, paying for it there where you have no plan. Null once it is sent.
    """

    fax: Fax
    paid_by: None | str
    confirm_url: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        fax = self.fax.to_dict()

        paid_by: None | str
        paid_by = self.paid_by

        confirm_url: None | str
        confirm_url = self.confirm_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fax": fax,
                "paid_by": paid_by,
                "confirm_url": confirm_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fax import Fax  # noqa: PLC0415

        d = dict(src_dict)
        fax = Fax.from_dict(d.pop("fax"))

        def _parse_paid_by(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        paid_by = _parse_paid_by(d.pop("paid_by"))

        def _parse_confirm_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        confirm_url = _parse_confirm_url(d.pop("confirm_url"))

        sent = cls(
            fax=fax,
            paid_by=paid_by,
            confirm_url=confirm_url,
        )

        sent.additional_properties = d
        return sent

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

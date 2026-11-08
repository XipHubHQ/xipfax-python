from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="QuotePrice")


@_attrs_define
class QuotePrice:
    """What the fax costs without a plan. A fax sent on the plan counts its pages there instead.

    Attributes:
        amount_minor (int): In the currency’s smallest unit: cents.
        currency (Literal['USD']):
    """

    amount_minor: int
    currency: Literal["USD"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount_minor = self.amount_minor

        currency = self.currency

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount_minor": amount_minor,
                "currency": currency,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount_minor = d.pop("amount_minor")

        currency = cast(Literal["USD"], d.pop("currency"))
        if currency != "USD":
            raise ValueError(f"currency must match const 'USD', got '{currency}'")

        quote_price = cls(
            amount_minor=amount_minor,
            currency=currency,
        )

        quote_price.additional_properties = d
        return quote_price

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

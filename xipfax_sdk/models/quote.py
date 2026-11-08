from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.quote_price import QuotePrice


T = TypeVar("T", bound="Quote")


@_attrs_define
class Quote:
    """
    Attributes:
        pages (int): The pages quoted.
        price (QuotePrice): What the fax costs without a plan. A fax sent on the plan counts its pages there instead.
        price_shown (str): The price as XipFax prints it: $4.99.
        terms (str): How the price is made, as XipFax’s pages say it: the first pages, then each page.
        price_list (str): The version of XipFax’s price list the quote is from.
    """

    pages: int
    price: QuotePrice
    price_shown: str
    terms: str
    price_list: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pages = self.pages

        price = self.price.to_dict()

        price_shown = self.price_shown

        terms = self.terms

        price_list = self.price_list

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pages": pages,
                "price": price,
                "price_shown": price_shown,
                "terms": terms,
                "price_list": price_list,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.quote_price import QuotePrice  # noqa: PLC0415

        d = dict(src_dict)
        pages = d.pop("pages")

        price = QuotePrice.from_dict(d.pop("price"))

        price_shown = d.pop("price_shown")

        terms = d.pop("terms")

        price_list = d.pop("price_list")

        quote = cls(
            pages=pages,
            price=price,
            price_shown=price_shown,
            terms=terms,
            price_list=price_list,
        )

        quote.additional_properties = d
        return quote

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

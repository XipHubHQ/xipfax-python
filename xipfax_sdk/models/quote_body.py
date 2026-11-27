from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="QuoteBody")


@_attrs_define
class QuoteBody:
    """
    Attributes:
        pages (int): The pages to send, from 1 to 250.
        to_number (str): The fax number, with its country code, such as `+44 20 7946 0958`; a number in the US, its
            territories or Canada needs none.
    """

    pages: int
    to_number: str

    def to_dict(self) -> dict[str, Any]:
        pages = self.pages

        to_number = self.to_number

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "pages": pages,
                "to_number": to_number,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pages = d.pop("pages")

        to_number = d.pop("to_number")

        quote_body = cls(
            pages=pages,
            to_number=to_number,
        )

        return quote_body

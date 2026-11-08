from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="NewDocument")


@_attrs_define
class NewDocument:
    """
    Attributes:
        name (str): Its name, such as its file’s: 255 characters at most.
        size_bytes (int | Unset): Its size, to upload it: a PDF of 40 MB at most, sent by the link the answer gives.
        url (str | Unset): Where XipFax fetches it from: an https link to a public address that answers with the PDF
            itself, 40 MB at most, within 15 seconds. XipFax follows no redirect.
    """

    name: str
    size_bytes: int | Unset = UNSET
    url: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        size_bytes = self.size_bytes

        url = self.url

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
            }
        )
        if size_bytes is not UNSET:
            field_dict["size_bytes"] = size_bytes
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        size_bytes = d.pop("size_bytes", UNSET)

        url = d.pop("url", UNSET)

        new_document = cls(
            name=name,
            size_bytes=size_bytes,
            url=url,
        )

        return new_document

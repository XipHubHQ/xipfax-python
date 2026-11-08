from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DraftDocument")


@_attrs_define
class DraftDocument:
    """A document of the draft, in its place in the fax.

    Attributes:
        id (str): The document.
        name (str): Its name, as it was added.
        size_bytes (int): Its size.
        page_count (int | None): Its pages, once XipFax has read it; null while it uploads.
        status (str): `uploading` until XipFax has read it back, then `ready`. An open set: read what you know.
        url (None | str): A link that reads the document for a few minutes, once it is ready; null while it uploads, and
            in an answer given again for a repeated `Idempotency-Key`.
    """

    id: str
    name: str
    size_bytes: int
    page_count: int | None
    status: str
    url: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        size_bytes = self.size_bytes

        page_count: int | None
        page_count = self.page_count

        status = self.status

        url: None | str
        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "size_bytes": size_bytes,
                "page_count": page_count,
                "status": status,
                "url": url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        size_bytes = d.pop("size_bytes")

        def _parse_page_count(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        page_count = _parse_page_count(d.pop("page_count"))

        status = d.pop("status")

        def _parse_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        url = _parse_url(d.pop("url"))

        draft_document = cls(
            id=id,
            name=name,
            size_bytes=size_bytes,
            page_count=page_count,
            status=status,
            url=url,
        )

        draft_document.additional_properties = d
        return draft_document

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

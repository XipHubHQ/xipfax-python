from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.document_added_upload_type_0_headers import DocumentAddedUploadType0Headers


T = TypeVar("T", bound="DocumentAddedUploadType0")


@_attrs_define
class DocumentAddedUploadType0:
    """
    Attributes:
        url (str):
        headers (DocumentAddedUploadType0Headers):
    """

    url: str
    headers: DocumentAddedUploadType0Headers
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        headers = self.headers.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "headers": headers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.document_added_upload_type_0_headers import DocumentAddedUploadType0Headers  # noqa: PLC0415

        d = dict(src_dict)
        url = d.pop("url")

        headers = DocumentAddedUploadType0Headers.from_dict(d.pop("headers"))

        document_added_upload_type_0 = cls(
            url=url,
            headers=headers,
        )

        document_added_upload_type_0.additional_properties = d
        return document_added_upload_type_0

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

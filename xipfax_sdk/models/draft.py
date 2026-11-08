from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.draft_document import DraftDocument


T = TypeVar("T", bound="Draft")


@_attrs_define
class Draft:
    """The fax you prepare, one at a time: the one your account’s web app shows too.

    Attributes:
        id (str): The draft, which becomes the fax once it is sent.
        documents (list[DraftDocument]): Its documents, in the order the fax sends them: 250 at most.
    """

    id: str
    documents: list[DraftDocument]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        documents = []
        for documents_item_data in self.documents:
            documents_item = documents_item_data.to_dict()
            documents.append(documents_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "documents": documents,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.draft_document import DraftDocument  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        documents = []
        _documents = d.pop("documents")
        for documents_item_data in _documents:
            documents_item = DraftDocument.from_dict(documents_item_data)

            documents.append(documents_item)

        draft = cls(
            id=id,
            documents=documents,
        )

        draft.additional_properties = d
        return draft

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

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SendDraft")


@_attrs_define
class SendDraft:
    """
    Attributes:
        document_ids (list[str]): The draft’s documents, as `GET /draft` names them, in its order: a draft whose
            documents aren’t these, in this order, is refused `draft_changed`, so that nothing you didn’t name is sent.
        fax_number (str | Unset): The number to send it to, in the US, its territories or Canada, written as you like,
            such as `+1 202 555 0143`.
        office_id (str | Unset): Or the office to send it to, by its id on XipFax’s list (`GET /offices`), which gives
            its number.
    """

    document_ids: list[str]
    fax_number: str | Unset = UNSET
    office_id: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        document_ids = self.document_ids

        fax_number = self.fax_number

        office_id = self.office_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "document_ids": document_ids,
            }
        )
        if fax_number is not UNSET:
            field_dict["fax_number"] = fax_number
        if office_id is not UNSET:
            field_dict["office_id"] = office_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        document_ids = cast(list[str], d.pop("document_ids"))

        fax_number = d.pop("fax_number", UNSET)

        office_id = d.pop("office_id", UNSET)

        send_draft = cls(
            document_ids=document_ids,
            fax_number=fax_number,
            office_id=office_id,
        )

        return send_draft

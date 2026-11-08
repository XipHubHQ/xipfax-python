from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.api_error_detail import APIErrorDetail


T = TypeVar("T", bound="APIErrorObject")


@_attrs_define
class APIErrorObject:
    """
    Attributes:
        code (str): What refused the request, from an open set: branch on it.
        message (str): XipFax’s sentence, for a person; never branch on it.
        details (list[APIErrorDetail]): One entry for each problem with the request; none where it has no parts.
        request_id (str): The request, as its answer’s `X-Request-Id` names it.
        doc_url (None | str): The page that explains the code; null while none does.
        valid_versions (list[str] | Unset): The released versions, which `version_invalid` names.
    """

    code: str
    message: str
    details: list[APIErrorDetail]
    request_id: str
    doc_url: None | str
    valid_versions: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        details = []
        for details_item_data in self.details:
            details_item = details_item_data.to_dict()
            details.append(details_item)

        request_id = self.request_id

        doc_url: None | str
        doc_url = self.doc_url

        valid_versions: list[str] | Unset = UNSET
        if not isinstance(self.valid_versions, Unset):
            valid_versions = self.valid_versions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
                "details": details,
                "request_id": request_id,
                "doc_url": doc_url,
            }
        )
        if valid_versions is not UNSET:
            field_dict["valid_versions"] = valid_versions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.api_error_detail import APIErrorDetail  # noqa: PLC0415

        d = dict(src_dict)
        code = d.pop("code")

        message = d.pop("message")

        details = []
        _details = d.pop("details")
        for details_item_data in _details:
            details_item = APIErrorDetail.from_dict(details_item_data)

            details.append(details_item)

        request_id = d.pop("request_id")

        def _parse_doc_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        doc_url = _parse_doc_url(d.pop("doc_url"))

        valid_versions = cast(list[str], d.pop("valid_versions", UNSET))

        api_error_object = cls(
            code=code,
            message=message,
            details=details,
            request_id=request_id,
            doc_url=doc_url,
            valid_versions=valid_versions,
        )

        api_error_object.additional_properties = d
        return api_error_object

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

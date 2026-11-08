from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.document_added_upload_type_0 import DocumentAddedUploadType0
    from ..models.draft_document import DraftDocument


T = TypeVar("T", bound="DocumentAdded")


@_attrs_define
class DocumentAdded:
    """A document added to the draft, and where its bytes go.

    Attributes:
        document (DraftDocument): A document of the draft, in its place in the fax.
        upload (DocumentAddedUploadType0 | None): Where to send its bytes: a PUT to `url` with these `headers`, within a
            few minutes, as many bytes as `size_bytes` says; then complete it. Null where XipFax fetched it from its link.
            In an answer given again for a repeated `Idempotency-Key`, a fresh link while the document still uploads, and
            null once it is ready or removed.
    """

    document: DraftDocument
    upload: DocumentAddedUploadType0 | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.document_added_upload_type_0 import DocumentAddedUploadType0  # noqa: PLC0415

        document = self.document.to_dict()

        upload: dict[str, Any] | None
        if isinstance(self.upload, DocumentAddedUploadType0):
            upload = self.upload.to_dict()
        else:
            upload = self.upload

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "document": document,
                "upload": upload,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.document_added_upload_type_0 import DocumentAddedUploadType0  # noqa: PLC0415
        from ..models.draft_document import DraftDocument  # noqa: PLC0415

        d = dict(src_dict)
        document = DraftDocument.from_dict(d.pop("document"))

        def _parse_upload(data: object) -> DocumentAddedUploadType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                upload_type_0 = DocumentAddedUploadType0.from_dict(data)

                return upload_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DocumentAddedUploadType0 | None, data)

        upload = _parse_upload(d.pop("upload"))

        document_added = cls(
            document=document,
            upload=upload,
        )

        document_added.additional_properties = d
        return document_added

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

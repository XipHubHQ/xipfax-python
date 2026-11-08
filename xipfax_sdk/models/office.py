from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.office_source import OfficeSource


T = TypeVar("T", bound="Office")


@_attrs_define
class Office:
    """A government office whose fax number XipFax gives, from the agency’s own pages.

    Attributes:
        id (str): The office, as XipFax’s list names it: `irs-caf-ogden`. A fax of your log names the office it went to
            by it.
        name (str): The office by its agency and its name: `IRS Ogden CAF unit`.
        fax_number (str): The number a fax to it goes to, `+1` and ten digits.
        fax_number_from_abroad (None | str): The number the agency gives a sender outside the United States, in E.164;
            null where it gives none.
        applies_to (list[str]): Whom or what the agency gives this number for, where it gives others another: `Ohio`, or
            `businesses in Wisconsin`; with `place`, only what applies there, where any of it does. Empty where the office
            takes what it takes from anyone.
        takes (list[str]): The forms and notices it takes, as XipFax’s pages name them: `Form 2848`.
        signed_in_ink (bool): Whether it takes a form only signed by hand, in ink.
        confidential_cover (bool): Whether it asks for a cover page marked Confidential, which a fax to it from XipFax
            marks.
        sources (list[OfficeSource]): The agency’s own pages that print the number.
        checked_on (str): The day XipFax last found the number on each of its sources: `YYYY-MM-DD`.
    """

    id: str
    name: str
    fax_number: str
    fax_number_from_abroad: None | str
    applies_to: list[str]
    takes: list[str]
    signed_in_ink: bool
    confidential_cover: bool
    sources: list[OfficeSource]
    checked_on: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        fax_number = self.fax_number

        fax_number_from_abroad: None | str
        fax_number_from_abroad = self.fax_number_from_abroad

        applies_to = self.applies_to

        takes = self.takes

        signed_in_ink = self.signed_in_ink

        confidential_cover = self.confidential_cover

        sources = []
        for sources_item_data in self.sources:
            sources_item = sources_item_data.to_dict()
            sources.append(sources_item)

        checked_on = self.checked_on

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "fax_number": fax_number,
                "fax_number_from_abroad": fax_number_from_abroad,
                "applies_to": applies_to,
                "takes": takes,
                "signed_in_ink": signed_in_ink,
                "confidential_cover": confidential_cover,
                "sources": sources,
                "checked_on": checked_on,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.office_source import OfficeSource  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        fax_number = d.pop("fax_number")

        def _parse_fax_number_from_abroad(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        fax_number_from_abroad = _parse_fax_number_from_abroad(d.pop("fax_number_from_abroad"))

        applies_to = cast(list[str], d.pop("applies_to"))

        takes = cast(list[str], d.pop("takes"))

        signed_in_ink = d.pop("signed_in_ink")

        confidential_cover = d.pop("confidential_cover")

        sources = []
        _sources = d.pop("sources")
        for sources_item_data in _sources:
            sources_item = OfficeSource.from_dict(sources_item_data)

            sources.append(sources_item)

        checked_on = d.pop("checked_on")

        office = cls(
            id=id,
            name=name,
            fax_number=fax_number,
            fax_number_from_abroad=fax_number_from_abroad,
            applies_to=applies_to,
            takes=takes,
            signed_in_ink=signed_in_ink,
            confidential_cover=confidential_cover,
            sources=sources,
            checked_on=checked_on,
        )

        office.additional_properties = d
        return office

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

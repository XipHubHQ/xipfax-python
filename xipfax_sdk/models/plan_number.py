from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PlanNumber")


@_attrs_define
class PlanNumber:
    """The fax number that comes with the plan, yours while the plan lasts.

    Attributes:
        area_code (str): The US area code it is in.
        status (str): `ordering` while XipFax gets it, `active` once it is yours, `failed` where none could be had in
            its area code. An open set.
        fax_number (None | str): The number, `+1` and ten digits, once it is ordered; null before, and once one fails.
    """

    area_code: str
    status: str
    fax_number: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        area_code = self.area_code

        status = self.status

        fax_number: None | str
        fax_number = self.fax_number

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "area_code": area_code,
                "status": status,
                "fax_number": fax_number,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        area_code = d.pop("area_code")

        status = d.pop("status")

        def _parse_fax_number(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        fax_number = _parse_fax_number(d.pop("fax_number"))

        plan_number = cls(
            area_code=area_code,
            status=status,
            fax_number=fax_number,
        )

        plan_number.additional_properties = d
        return plan_number

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

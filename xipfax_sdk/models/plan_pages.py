from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PlanPages")


@_attrs_define
class PlanPages:
    """The month’s pages, sent and received together.

    Attributes:
        used (int): The pages sent and received this month.
        included (int): The pages the plan includes each month.
        resets_at (str): When the month’s pages start again.
    """

    used: int
    included: int
    resets_at: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        used = self.used

        included = self.included

        resets_at = self.resets_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "used": used,
                "included": included,
                "resets_at": resets_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        used = d.pop("used")

        included = d.pop("included")

        resets_at = d.pop("resets_at")

        plan_pages = cls(
            used=used,
            included=included,
            resets_at=resets_at,
        )

        plan_pages.additional_properties = d
        return plan_pages

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

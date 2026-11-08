from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.plan import Plan


T = TypeVar("T", bound="PlanAnswer")


@_attrs_define
class PlanAnswer:
    """Your plan, or none.

    Attributes:
        plan (None | Plan): Your plan; null where you have none.
    """

    plan: None | Plan
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.plan import Plan  # noqa: PLC0415

        plan: dict[str, Any] | None
        if isinstance(self.plan, Plan):
            plan = self.plan.to_dict()
        else:
            plan = self.plan

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "plan": plan,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.plan import Plan  # noqa: PLC0415

        d = dict(src_dict)

        def _parse_plan(data: object) -> None | Plan:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                plan_type_0 = Plan.from_dict(data)

                return plan_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Plan, data)

        plan = _parse_plan(d.pop("plan"))

        plan_answer = cls(
            plan=plan,
        )

        plan_answer.additional_properties = d
        return plan_answer

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

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.money import Money
    from ..models.plan_number import PlanNumber
    from ..models.plan_pages import PlanPages


T = TypeVar("T", bound="Plan")


@_attrs_define
class Plan:
    """Your plan: your own fax number, and pages each month.

    Attributes:
        interval (str): How often it is paid for: each `month`, or each `year`.
        price (Money): An amount of money.
        period_ends_at (str): The end of the period paid for: the plan renews then, or ends then where it is cancelled.
        is_ending (bool): Whether it is cancelled, to end at `period_ends_at` rather than renew.
        refused_renewal (Money | None): What the renewal the card refused charges, until it is paid; null where none is
            owed.
        number (PlanNumber): The fax number that comes with the plan, yours while the plan lasts.
        pages (PlanPages): The month’s pages, sent and received together.
    """

    interval: str
    price: Money
    period_ends_at: str
    is_ending: bool
    refused_renewal: Money | None
    number: PlanNumber
    pages: PlanPages
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.money import Money  # noqa: PLC0415

        interval = self.interval

        price = self.price.to_dict()

        period_ends_at = self.period_ends_at

        is_ending = self.is_ending

        refused_renewal: dict[str, Any] | None
        if isinstance(self.refused_renewal, Money):
            refused_renewal = self.refused_renewal.to_dict()
        else:
            refused_renewal = self.refused_renewal

        number = self.number.to_dict()

        pages = self.pages.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "interval": interval,
                "price": price,
                "period_ends_at": period_ends_at,
                "is_ending": is_ending,
                "refused_renewal": refused_renewal,
                "number": number,
                "pages": pages,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.money import Money  # noqa: PLC0415
        from ..models.plan_number import PlanNumber  # noqa: PLC0415
        from ..models.plan_pages import PlanPages  # noqa: PLC0415

        d = dict(src_dict)
        interval = d.pop("interval")

        price = Money.from_dict(d.pop("price"))

        period_ends_at = d.pop("period_ends_at")

        is_ending = d.pop("is_ending")

        def _parse_refused_renewal(data: object) -> Money | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                refused_renewal_type_0 = Money.from_dict(data)

                return refused_renewal_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Money | None, data)

        refused_renewal = _parse_refused_renewal(d.pop("refused_renewal"))

        number = PlanNumber.from_dict(d.pop("number"))

        pages = PlanPages.from_dict(d.pop("pages"))

        plan = cls(
            interval=interval,
            price=price,
            period_ends_at=period_ends_at,
            is_ending=is_ending,
            refused_renewal=refused_renewal,
            number=number,
            pages=pages,
        )

        plan.additional_properties = d
        return plan

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

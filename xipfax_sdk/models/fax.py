from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.money import Money


T = TypeVar("T", bound="Fax")


@_attrs_define
class Fax:
    """A fax of your log: one you sent, or one sent to your number.

    Attributes:
        id (str): The fax.
        direction (str): `sent` for a fax you sent, `received` for one sent to your number.
        status (str): Where it stands: `draft` for your draft, read by its id until it is sent; `sending` until it is
            delivered or fails for good, then `delivered` or `failed`; `received` for a fax sent to your number. An open
            set: read what you know.
        step (None | str): Where a fax being sent has got to: `queued`, `preparing` its pages, then `sending`; null for
            a draft, once it has ended, and for a fax received. An open set.
        office_id (None | str): The office it went to, by its id on XipFax’s list (`GET /offices`); null for a number
            typed, and for a fax received.
        to_number (None | str): The number it went to, `+1` and ten digits; for a fax received, your number it came to.
        from_number (None | str): For a fax you sent, the number it went from: your XipFax number, or XipFax’s where you
            have none; for your draft, null; for a fax received, the caller’s number in E.164, null where the caller’s line
            gave none.
        pages (int | None): Its pages, the cover page among them.
        price (Money | None): What it costs: what its payment holds while it sends, and what was taken once it was
            delivered. Null for a fax sent on the plan or with a promo code, for one that failed, which costs nothing, and
            for a fax received.
        sent_at (None | str): When you sent it; for a fax received, when it came.
        finished_at (None | str): When it was delivered or failed for good; null until then.
        retry_at (None | str): When it is tried again, while a failed try waits for the next; null otherwise.
        failure (None | str): Why its last try failed: `no_answer`, `busy`, `call_dropped`, `declined`,
            `not_a_fax_number`, or `ours` for a failure on XipFax’s side. Null where none failed. An open set.
        time_zone (None | str): The time zone its confirmation tells its times in, as the IANA database names it; null
            for a fax received.
        sender_name (None | str): For a fax you sent, the sender’s name its header line gave.
        cover_confidential (bool): Whether its cover page was marked Confidential; false for a fax received.
    """

    id: str
    direction: str
    status: str
    step: None | str
    office_id: None | str
    to_number: None | str
    from_number: None | str
    pages: int | None
    price: Money | None
    sent_at: None | str
    finished_at: None | str
    retry_at: None | str
    failure: None | str
    time_zone: None | str
    sender_name: None | str
    cover_confidential: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.money import Money  # noqa: PLC0415

        id = self.id

        direction = self.direction

        status = self.status

        step: None | str
        step = self.step

        office_id: None | str
        office_id = self.office_id

        to_number: None | str
        to_number = self.to_number

        from_number: None | str
        from_number = self.from_number

        pages: int | None
        pages = self.pages

        price: dict[str, Any] | None
        if isinstance(self.price, Money):
            price = self.price.to_dict()
        else:
            price = self.price

        sent_at: None | str
        sent_at = self.sent_at

        finished_at: None | str
        finished_at = self.finished_at

        retry_at: None | str
        retry_at = self.retry_at

        failure: None | str
        failure = self.failure

        time_zone: None | str
        time_zone = self.time_zone

        sender_name: None | str
        sender_name = self.sender_name

        cover_confidential = self.cover_confidential

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "direction": direction,
                "status": status,
                "step": step,
                "office_id": office_id,
                "to_number": to_number,
                "from_number": from_number,
                "pages": pages,
                "price": price,
                "sent_at": sent_at,
                "finished_at": finished_at,
                "retry_at": retry_at,
                "failure": failure,
                "time_zone": time_zone,
                "sender_name": sender_name,
                "cover_confidential": cover_confidential,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.money import Money  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        direction = d.pop("direction")

        status = d.pop("status")

        def _parse_step(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        step = _parse_step(d.pop("step"))

        def _parse_office_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        office_id = _parse_office_id(d.pop("office_id"))

        def _parse_to_number(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        to_number = _parse_to_number(d.pop("to_number"))

        def _parse_from_number(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        from_number = _parse_from_number(d.pop("from_number"))

        def _parse_pages(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        pages = _parse_pages(d.pop("pages"))

        def _parse_price(data: object) -> Money | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                price_type_0 = Money.from_dict(data)

                return price_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Money | None, data)

        price = _parse_price(d.pop("price"))

        def _parse_sent_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        sent_at = _parse_sent_at(d.pop("sent_at"))

        def _parse_finished_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        finished_at = _parse_finished_at(d.pop("finished_at"))

        def _parse_retry_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        retry_at = _parse_retry_at(d.pop("retry_at"))

        def _parse_failure(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        failure = _parse_failure(d.pop("failure"))

        def _parse_time_zone(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        time_zone = _parse_time_zone(d.pop("time_zone"))

        def _parse_sender_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        sender_name = _parse_sender_name(d.pop("sender_name"))

        cover_confidential = d.pop("cover_confidential")

        fax = cls(
            id=id,
            direction=direction,
            status=status,
            step=step,
            office_id=office_id,
            to_number=to_number,
            from_number=from_number,
            pages=pages,
            price=price,
            sent_at=sent_at,
            finished_at=finished_at,
            retry_at=retry_at,
            failure=failure,
            time_zone=time_zone,
            sender_name=sender_name,
            cover_confidential=cover_confidential,
        )

        fax.additional_properties = d
        return fax

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

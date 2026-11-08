from typing import Literal

ListFaxesDirection = Literal["received", "sent"]

LIST_FAXES_DIRECTION_VALUES: set[ListFaxesDirection] = {
    "received",
    "sent",
}


def check_list_faxes_direction(value: str) -> ListFaxesDirection:
    if value in LIST_FAXES_DIRECTION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_FAXES_DIRECTION_VALUES!r}")

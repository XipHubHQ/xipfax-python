from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import APIError
from ...models.list_offices_place import ListOfficesPlace
from ...models.office_page import OfficePage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 20,
    starting_after: str | Unset = UNSET,
    search: str | Unset = UNSET,
    place: ListOfficesPlace | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["starting_after"] = starting_after

    params["search"] = search

    json_place: str | Unset = UNSET
    if not isinstance(place, Unset):
        json_place = place

    params["place"] = json_place

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/offices",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> APIError | OfficePage | None:
    if response.status_code == 200:
        response_200 = OfficePage.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = APIError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = APIError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = APIError.from_dict(response.json())

        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[APIError | OfficePage]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 20,
    starting_after: str | Unset = UNSET,
    search: str | Unset = UNSET,
    place: ListOfficesPlace | Unset = UNSET,
) -> Response[APIError | OfficePage]:
    """List the offices

     The government offices XipFax gives the fax number of, from the agencies’ own pages: those `search`
    finds, as XipFax’s own office search finds them for the same words, and for `place` where the agency
    gives a number for each place; in the list’s order, a page at a time. Give a page’s `next_cursor` as
    `starting_after` for the page after it.

    Args:
        limit (int | Unset): How many items the page holds: 20 unless you ask for another number,
            and 100 at most. Default: 20.
        starting_after (str | Unset): The `next_cursor` of the page before, for the page after it;
            none for the first page.
        search (str | Unset): What the office takes, its name or its number, as XipFax’s own
            office search takes them: `Form 2848`, `CP2000`. An office is listed where each word is in
            its name, its number or what it takes. Every office without it; 100 characters at most.
        place (ListOfficesPlace | Unset): Where the person lives, or where the business is, by its
            postal code: `OH` for Ohio, `PR` for Puerto Rico; `APO-FPO` for an APO or FPO address;
            `ABROAD` for anywhere outside the United States. Where the agency gives a number for each
            place, the office for this one is listed, beside those for what applies wherever one
            lives, and the offices for other places are not; where it gives none for this place, all
            of them are.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIError | OfficePage]
    """

    kwargs = _get_kwargs(
        limit=limit,
        starting_after=starting_after,
        search=search,
        place=place,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 20,
    starting_after: str | Unset = UNSET,
    search: str | Unset = UNSET,
    place: ListOfficesPlace | Unset = UNSET,
) -> APIError | OfficePage | None:
    """List the offices

     The government offices XipFax gives the fax number of, from the agencies’ own pages: those `search`
    finds, as XipFax’s own office search finds them for the same words, and for `place` where the agency
    gives a number for each place; in the list’s order, a page at a time. Give a page’s `next_cursor` as
    `starting_after` for the page after it.

    Args:
        limit (int | Unset): How many items the page holds: 20 unless you ask for another number,
            and 100 at most. Default: 20.
        starting_after (str | Unset): The `next_cursor` of the page before, for the page after it;
            none for the first page.
        search (str | Unset): What the office takes, its name or its number, as XipFax’s own
            office search takes them: `Form 2848`, `CP2000`. An office is listed where each word is in
            its name, its number or what it takes. Every office without it; 100 characters at most.
        place (ListOfficesPlace | Unset): Where the person lives, or where the business is, by its
            postal code: `OH` for Ohio, `PR` for Puerto Rico; `APO-FPO` for an APO or FPO address;
            `ABROAD` for anywhere outside the United States. Where the agency gives a number for each
            place, the office for this one is listed, beside those for what applies wherever one
            lives, and the offices for other places are not; where it gives none for this place, all
            of them are.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIError | OfficePage
    """

    return sync_detailed(
        client=client,
        limit=limit,
        starting_after=starting_after,
        search=search,
        place=place,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 20,
    starting_after: str | Unset = UNSET,
    search: str | Unset = UNSET,
    place: ListOfficesPlace | Unset = UNSET,
) -> Response[APIError | OfficePage]:
    """List the offices

     The government offices XipFax gives the fax number of, from the agencies’ own pages: those `search`
    finds, as XipFax’s own office search finds them for the same words, and for `place` where the agency
    gives a number for each place; in the list’s order, a page at a time. Give a page’s `next_cursor` as
    `starting_after` for the page after it.

    Args:
        limit (int | Unset): How many items the page holds: 20 unless you ask for another number,
            and 100 at most. Default: 20.
        starting_after (str | Unset): The `next_cursor` of the page before, for the page after it;
            none for the first page.
        search (str | Unset): What the office takes, its name or its number, as XipFax’s own
            office search takes them: `Form 2848`, `CP2000`. An office is listed where each word is in
            its name, its number or what it takes. Every office without it; 100 characters at most.
        place (ListOfficesPlace | Unset): Where the person lives, or where the business is, by its
            postal code: `OH` for Ohio, `PR` for Puerto Rico; `APO-FPO` for an APO or FPO address;
            `ABROAD` for anywhere outside the United States. Where the agency gives a number for each
            place, the office for this one is listed, beside those for what applies wherever one
            lives, and the offices for other places are not; where it gives none for this place, all
            of them are.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIError | OfficePage]
    """

    kwargs = _get_kwargs(
        limit=limit,
        starting_after=starting_after,
        search=search,
        place=place,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 20,
    starting_after: str | Unset = UNSET,
    search: str | Unset = UNSET,
    place: ListOfficesPlace | Unset = UNSET,
) -> APIError | OfficePage | None:
    """List the offices

     The government offices XipFax gives the fax number of, from the agencies’ own pages: those `search`
    finds, as XipFax’s own office search finds them for the same words, and for `place` where the agency
    gives a number for each place; in the list’s order, a page at a time. Give a page’s `next_cursor` as
    `starting_after` for the page after it.

    Args:
        limit (int | Unset): How many items the page holds: 20 unless you ask for another number,
            and 100 at most. Default: 20.
        starting_after (str | Unset): The `next_cursor` of the page before, for the page after it;
            none for the first page.
        search (str | Unset): What the office takes, its name or its number, as XipFax’s own
            office search takes them: `Form 2848`, `CP2000`. An office is listed where each word is in
            its name, its number or what it takes. Every office without it; 100 characters at most.
        place (ListOfficesPlace | Unset): Where the person lives, or where the business is, by its
            postal code: `OH` for Ohio, `PR` for Puerto Rico; `APO-FPO` for an APO or FPO address;
            `ABROAD` for anywhere outside the United States. Where the agency gives a number for each
            place, the office for this one is listed, beside those for what applies wherever one
            lives, and the offices for other places are not; where it gives none for this place, all
            of them are.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIError | OfficePage
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            starting_after=starting_after,
            search=search,
            place=place,
        )
    ).parsed

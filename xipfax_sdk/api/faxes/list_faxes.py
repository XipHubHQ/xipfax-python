from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import APIError
from ...models.fax_page import FaxPage
from ...models.list_faxes_direction import ListFaxesDirection
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 20,
    starting_after: str | Unset = UNSET,
    direction: ListFaxesDirection | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["starting_after"] = starting_after

    json_direction: str | Unset = UNSET
    if not isinstance(direction, Unset):
        json_direction = direction

    params["direction"] = json_direction

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/faxes",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> APIError | FaxPage | None:
    if response.status_code == 200:
        response_200 = FaxPage.from_dict(response.json())

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
) -> Response[APIError | FaxPage]:
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
    direction: ListFaxesDirection | Unset = UNSET,
) -> Response[APIError | FaxPage]:
    """List the faxes

     Every fax you sent and every fax sent to your number, newest first, a page at a time: the faxes your
    account’s web app logs, page for page. Give a page’s `next_cursor` as `starting_after` for the page
    after it.

    Args:
        limit (int | Unset): How many items the page holds: 20 unless you ask for another number,
            and 100 at most. Default: 20.
        starting_after (str | Unset): The `next_cursor` of the page before, for the page after it;
            none for the first page.
        direction (ListFaxesDirection | Unset): Only the faxes you `sent`, or only those you
            `received`; both without it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIError | FaxPage]
    """

    kwargs = _get_kwargs(
        limit=limit,
        starting_after=starting_after,
        direction=direction,
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
    direction: ListFaxesDirection | Unset = UNSET,
) -> APIError | FaxPage | None:
    """List the faxes

     Every fax you sent and every fax sent to your number, newest first, a page at a time: the faxes your
    account’s web app logs, page for page. Give a page’s `next_cursor` as `starting_after` for the page
    after it.

    Args:
        limit (int | Unset): How many items the page holds: 20 unless you ask for another number,
            and 100 at most. Default: 20.
        starting_after (str | Unset): The `next_cursor` of the page before, for the page after it;
            none for the first page.
        direction (ListFaxesDirection | Unset): Only the faxes you `sent`, or only those you
            `received`; both without it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIError | FaxPage
    """

    return sync_detailed(
        client=client,
        limit=limit,
        starting_after=starting_after,
        direction=direction,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 20,
    starting_after: str | Unset = UNSET,
    direction: ListFaxesDirection | Unset = UNSET,
) -> Response[APIError | FaxPage]:
    """List the faxes

     Every fax you sent and every fax sent to your number, newest first, a page at a time: the faxes your
    account’s web app logs, page for page. Give a page’s `next_cursor` as `starting_after` for the page
    after it.

    Args:
        limit (int | Unset): How many items the page holds: 20 unless you ask for another number,
            and 100 at most. Default: 20.
        starting_after (str | Unset): The `next_cursor` of the page before, for the page after it;
            none for the first page.
        direction (ListFaxesDirection | Unset): Only the faxes you `sent`, or only those you
            `received`; both without it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIError | FaxPage]
    """

    kwargs = _get_kwargs(
        limit=limit,
        starting_after=starting_after,
        direction=direction,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 20,
    starting_after: str | Unset = UNSET,
    direction: ListFaxesDirection | Unset = UNSET,
) -> APIError | FaxPage | None:
    """List the faxes

     Every fax you sent and every fax sent to your number, newest first, a page at a time: the faxes your
    account’s web app logs, page for page. Give a page’s `next_cursor` as `starting_after` for the page
    after it.

    Args:
        limit (int | Unset): How many items the page holds: 20 unless you ask for another number,
            and 100 at most. Default: 20.
        starting_after (str | Unset): The `next_cursor` of the page before, for the page after it;
            none for the first page.
        direction (ListFaxesDirection | Unset): Only the faxes you `sent`, or only those you
            `received`; both without it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIError | FaxPage
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            starting_after=starting_after,
            direction=direction,
        )
    ).parsed

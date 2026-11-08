from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import APIError
from ...models.quote import Quote
from ...types import UNSET, Response


def _get_kwargs(
    *,
    pages: int,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["pages"] = pages

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/quote",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> APIError | Quote | None:
    if response.status_code == 200:
        response_200 = Quote.from_dict(response.json())

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
) -> Response[APIError | Quote]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    pages: int,
) -> Response[APIError | Quote]:
    """Quote a fax

     The price of one fax of so many pages, sent without a plan, from XipFax’s price list: what its
    checkout charges. A fax sent on the plan counts its pages there instead.

    Args:
        pages (int): The pages to send, from 1 to 250.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIError | Quote]
    """

    kwargs = _get_kwargs(
        pages=pages,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    pages: int,
) -> APIError | Quote | None:
    """Quote a fax

     The price of one fax of so many pages, sent without a plan, from XipFax’s price list: what its
    checkout charges. A fax sent on the plan counts its pages there instead.

    Args:
        pages (int): The pages to send, from 1 to 250.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIError | Quote
    """

    return sync_detailed(
        client=client,
        pages=pages,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    pages: int,
) -> Response[APIError | Quote]:
    """Quote a fax

     The price of one fax of so many pages, sent without a plan, from XipFax’s price list: what its
    checkout charges. A fax sent on the plan counts its pages there instead.

    Args:
        pages (int): The pages to send, from 1 to 250.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIError | Quote]
    """

    kwargs = _get_kwargs(
        pages=pages,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    pages: int,
) -> APIError | Quote | None:
    """Quote a fax

     The price of one fax of so many pages, sent without a plan, from XipFax’s price list: what its
    checkout charges. A fax sent on the plan counts its pages there instead.

    Args:
        pages (int): The pages to send, from 1 to 250.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIError | Quote
    """

    return (
        await asyncio_detailed(
            client=client,
            pages=pages,
        )
    ).parsed

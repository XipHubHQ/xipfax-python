from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import APIError
from ...types import Response


def _get_kwargs(
    endpoint_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/webhook-endpoints/{endpoint_id}".format(
            endpoint_id=quote(str(endpoint_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> APIError | Any | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = APIError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = APIError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = APIError.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = APIError.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[APIError | Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    endpoint_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[APIError | Any]:
    """Remove a webhook endpoint

     Removes an endpoint of your account, whichever key registered it: no event goes to it from then on,
    a delivery still to be tried again among them. An API key alone removes one; an app’s token is
    refused `insufficient_scope`.

    Args:
        endpoint_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIError | Any]
    """

    kwargs = _get_kwargs(
        endpoint_id=endpoint_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    endpoint_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> APIError | Any | None:
    """Remove a webhook endpoint

     Removes an endpoint of your account, whichever key registered it: no event goes to it from then on,
    a delivery still to be tried again among them. An API key alone removes one; an app’s token is
    refused `insufficient_scope`.

    Args:
        endpoint_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIError | Any
    """

    return sync_detailed(
        endpoint_id=endpoint_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    endpoint_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[APIError | Any]:
    """Remove a webhook endpoint

     Removes an endpoint of your account, whichever key registered it: no event goes to it from then on,
    a delivery still to be tried again among them. An API key alone removes one; an app’s token is
    refused `insufficient_scope`.

    Args:
        endpoint_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIError | Any]
    """

    kwargs = _get_kwargs(
        endpoint_id=endpoint_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    endpoint_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> APIError | Any | None:
    """Remove a webhook endpoint

     Removes an endpoint of your account, whichever key registered it: no event goes to it from then on,
    a delivery still to be tried again among them. An API key alone removes one; an app’s token is
    refused `insufficient_scope`.

    Args:
        endpoint_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIError | Any
    """

    return (
        await asyncio_detailed(
            endpoint_id=endpoint_id,
            client=client,
        )
    ).parsed

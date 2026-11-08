from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import APIError
from ...models.fax import Fax
from ...types import Response


def _get_kwargs(
    fax_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/faxes/{fax_id}".format(
            fax_id=quote(str(fax_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> APIError | Fax | None:
    if response.status_code == 200:
        response_200 = Fax.from_dict(response.json())

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

    if response.status_code == 404:
        response_404 = APIError.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[APIError | Fax]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    fax_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[APIError | Fax]:
    """Read a fax

     A fax you sent or one sent to your number, as `GET /faxes` gives it, where it stands now; or your
    draft, `draft`, by its id, which the fax keeps once you send it.

    Args:
        fax_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIError | Fax]
    """

    kwargs = _get_kwargs(
        fax_id=fax_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    fax_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> APIError | Fax | None:
    """Read a fax

     A fax you sent or one sent to your number, as `GET /faxes` gives it, where it stands now; or your
    draft, `draft`, by its id, which the fax keeps once you send it.

    Args:
        fax_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIError | Fax
    """

    return sync_detailed(
        fax_id=fax_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    fax_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[APIError | Fax]:
    """Read a fax

     A fax you sent or one sent to your number, as `GET /faxes` gives it, where it stands now; or your
    draft, `draft`, by its id, which the fax keeps once you send it.

    Args:
        fax_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIError | Fax]
    """

    kwargs = _get_kwargs(
        fax_id=fax_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    fax_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> APIError | Fax | None:
    """Read a fax

     A fax you sent or one sent to your number, as `GET /faxes` gives it, where it stands now; or your
    draft, `draft`, by its id, which the fax keeps once you send it.

    Args:
        fax_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIError | Fax
    """

    return (
        await asyncio_detailed(
            fax_id=fax_id,
            client=client,
        )
    ).parsed

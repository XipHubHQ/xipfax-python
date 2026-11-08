from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import APIError
from ...models.draft_document import DraftDocument
from ...types import Response


def _get_kwargs(
    document_id: str,
    *,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/draft/documents/{document_id}/complete".format(
            document_id=quote(str(document_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> APIError | DraftDocument | None:
    if response.status_code == 200:
        response_200 = DraftDocument.from_dict(response.json())

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

    if response.status_code == 409:
        response_409 = APIError.from_dict(response.json())

        return response_409

    if response.status_code == 413:
        response_413 = APIError.from_dict(response.json())

        return response_413

    if response.status_code == 422:
        response_422 = APIError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[APIError | DraftDocument]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    document_id: str,
    *,
    client: AuthenticatedClient | Client,
    idempotency_key: str,
) -> Response[APIError | DraftDocument]:
    """Complete a document

     Reads an uploaded document back: `ready`, its pages counted; or removed and refused, where XipFax
    can’t read it, it’s locked with a password, or it takes the fax past 250 pages, its cover page
    included. A document ready already is answered as it is.

    Args:
        document_id (str):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIError | DraftDocument]
    """

    kwargs = _get_kwargs(
        document_id=document_id,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    document_id: str,
    *,
    client: AuthenticatedClient | Client,
    idempotency_key: str,
) -> APIError | DraftDocument | None:
    """Complete a document

     Reads an uploaded document back: `ready`, its pages counted; or removed and refused, where XipFax
    can’t read it, it’s locked with a password, or it takes the fax past 250 pages, its cover page
    included. A document ready already is answered as it is.

    Args:
        document_id (str):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIError | DraftDocument
    """

    return sync_detailed(
        document_id=document_id,
        client=client,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    document_id: str,
    *,
    client: AuthenticatedClient | Client,
    idempotency_key: str,
) -> Response[APIError | DraftDocument]:
    """Complete a document

     Reads an uploaded document back: `ready`, its pages counted; or removed and refused, where XipFax
    can’t read it, it’s locked with a password, or it takes the fax past 250 pages, its cover page
    included. A document ready already is answered as it is.

    Args:
        document_id (str):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIError | DraftDocument]
    """

    kwargs = _get_kwargs(
        document_id=document_id,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    document_id: str,
    *,
    client: AuthenticatedClient | Client,
    idempotency_key: str,
) -> APIError | DraftDocument | None:
    """Complete a document

     Reads an uploaded document back: `ready`, its pages counted; or removed and refused, where XipFax
    can’t read it, it’s locked with a password, or it takes the fax past 250 pages, its cover page
    included. A document ready already is answered as it is.

    Args:
        document_id (str):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIError | DraftDocument
    """

    return (
        await asyncio_detailed(
            document_id=document_id,
            client=client,
            idempotency_key=idempotency_key,
        )
    ).parsed

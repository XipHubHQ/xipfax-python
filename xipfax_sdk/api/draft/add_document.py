from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import APIError
from ...models.document_added import DocumentAdded
from ...models.new_document import NewDocument
from ...types import Response


def _get_kwargs(
    *,
    body: NewDocument,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/draft/documents",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> APIError | DocumentAdded | None:
    if response.status_code == 201:
        response_201 = DocumentAdded.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = APIError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = APIError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = APIError.from_dict(response.json())

        return response_403

    if response.status_code == 409:
        response_409 = APIError.from_dict(response.json())

        return response_409

    if response.status_code == 413:
        response_413 = APIError.from_dict(response.json())

        return response_413

    if response.status_code == 422:
        response_422 = APIError.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = APIError.from_dict(response.json())

        return response_429

    if response.status_code == 502:
        response_502 = APIError.from_dict(response.json())

        return response_502

    if response.status_code == 503:
        response_503 = APIError.from_dict(response.json())

        return response_503

    if response.status_code == 504:
        response_504 = APIError.from_dict(response.json())

        return response_504

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[APIError | DocumentAdded]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: NewDocument,
    idempotency_key: str,
) -> Response[APIError | DocumentAdded]:
    """Add a document

     Adds a PDF after the draft’s last document. Give `size_bytes` to upload it: the answer gives a link
    to send its bytes to, and the document is `uploading` until you complete it. Or give `url`, for
    XipFax to fetch it: the answer gives it `ready`, its pages counted. A PDF XipFax can’t read, one
    locked with a password, and one that takes the fax past 250 pages, its cover page included, are
    refused. XipFax fetches 10 links a minute for your account at most, and 1,000 a day, whichever key
    or app gives them: past either, a `url` is refused `rate_limit_exceeded`, nothing fetched, and
    `Retry-After` says in seconds when to try again. A document added by its `size_bytes` counts toward
    neither.

    Args:
        idempotency_key (str):
        body (NewDocument):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIError | DocumentAdded]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: NewDocument,
    idempotency_key: str,
) -> APIError | DocumentAdded | None:
    """Add a document

     Adds a PDF after the draft’s last document. Give `size_bytes` to upload it: the answer gives a link
    to send its bytes to, and the document is `uploading` until you complete it. Or give `url`, for
    XipFax to fetch it: the answer gives it `ready`, its pages counted. A PDF XipFax can’t read, one
    locked with a password, and one that takes the fax past 250 pages, its cover page included, are
    refused. XipFax fetches 10 links a minute for your account at most, and 1,000 a day, whichever key
    or app gives them: past either, a `url` is refused `rate_limit_exceeded`, nothing fetched, and
    `Retry-After` says in seconds when to try again. A document added by its `size_bytes` counts toward
    neither.

    Args:
        idempotency_key (str):
        body (NewDocument):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIError | DocumentAdded
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: NewDocument,
    idempotency_key: str,
) -> Response[APIError | DocumentAdded]:
    """Add a document

     Adds a PDF after the draft’s last document. Give `size_bytes` to upload it: the answer gives a link
    to send its bytes to, and the document is `uploading` until you complete it. Or give `url`, for
    XipFax to fetch it: the answer gives it `ready`, its pages counted. A PDF XipFax can’t read, one
    locked with a password, and one that takes the fax past 250 pages, its cover page included, are
    refused. XipFax fetches 10 links a minute for your account at most, and 1,000 a day, whichever key
    or app gives them: past either, a `url` is refused `rate_limit_exceeded`, nothing fetched, and
    `Retry-After` says in seconds when to try again. A document added by its `size_bytes` counts toward
    neither.

    Args:
        idempotency_key (str):
        body (NewDocument):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIError | DocumentAdded]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: NewDocument,
    idempotency_key: str,
) -> APIError | DocumentAdded | None:
    """Add a document

     Adds a PDF after the draft’s last document. Give `size_bytes` to upload it: the answer gives a link
    to send its bytes to, and the document is `uploading` until you complete it. Or give `url`, for
    XipFax to fetch it: the answer gives it `ready`, its pages counted. A PDF XipFax can’t read, one
    locked with a password, and one that takes the fax past 250 pages, its cover page included, are
    refused. XipFax fetches 10 links a minute for your account at most, and 1,000 a day, whichever key
    or app gives them: past either, a `url` is refused `rate_limit_exceeded`, nothing fetched, and
    `Retry-After` says in seconds when to try again. A document added by its `size_bytes` counts toward
    neither.

    Args:
        idempotency_key (str):
        body (NewDocument):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIError | DocumentAdded
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed

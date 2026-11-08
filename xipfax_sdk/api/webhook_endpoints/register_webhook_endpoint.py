from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import APIError
from ...models.new_webhook_endpoint import NewWebhookEndpoint
from ...models.webhook_endpoint import WebhookEndpoint
from ...types import Response


def _get_kwargs(
    *,
    body: NewWebhookEndpoint,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/webhook-endpoints",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> APIError | WebhookEndpoint | None:
    if response.status_code == 201:
        response_201 = WebhookEndpoint.from_dict(response.json())

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

    if response.status_code == 503:
        response_503 = APIError.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[APIError | WebhookEndpoint]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: NewWebhookEndpoint,
    idempotency_key: str,
) -> Response[APIError | WebhookEndpoint]:
    """Register a webhook endpoint

     Registers an endpoint of your own server, which every event XipFax posts goes to from then on, as
    `webhooks` describes them, each signed with the endpoint’s own secret: the answer shows the secret,
    once, so keep it then. XipFax checks that the URL leads to an address on the internet, now and
    before each delivery. Your account keeps 16 endpoints at most, and registers 10 in an hour at most.
    An API key alone registers one, and revoking the key removes those it registered; an app’s token is
    refused `insufficient_scope`.

    Args:
        idempotency_key (str):
        body (NewWebhookEndpoint): A webhook endpoint to register: the URL of your own server that
            takes the events.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIError | WebhookEndpoint]
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
    body: NewWebhookEndpoint,
    idempotency_key: str,
) -> APIError | WebhookEndpoint | None:
    """Register a webhook endpoint

     Registers an endpoint of your own server, which every event XipFax posts goes to from then on, as
    `webhooks` describes them, each signed with the endpoint’s own secret: the answer shows the secret,
    once, so keep it then. XipFax checks that the URL leads to an address on the internet, now and
    before each delivery. Your account keeps 16 endpoints at most, and registers 10 in an hour at most.
    An API key alone registers one, and revoking the key removes those it registered; an app’s token is
    refused `insufficient_scope`.

    Args:
        idempotency_key (str):
        body (NewWebhookEndpoint): A webhook endpoint to register: the URL of your own server that
            takes the events.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIError | WebhookEndpoint
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: NewWebhookEndpoint,
    idempotency_key: str,
) -> Response[APIError | WebhookEndpoint]:
    """Register a webhook endpoint

     Registers an endpoint of your own server, which every event XipFax posts goes to from then on, as
    `webhooks` describes them, each signed with the endpoint’s own secret: the answer shows the secret,
    once, so keep it then. XipFax checks that the URL leads to an address on the internet, now and
    before each delivery. Your account keeps 16 endpoints at most, and registers 10 in an hour at most.
    An API key alone registers one, and revoking the key removes those it registered; an app’s token is
    refused `insufficient_scope`.

    Args:
        idempotency_key (str):
        body (NewWebhookEndpoint): A webhook endpoint to register: the URL of your own server that
            takes the events.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIError | WebhookEndpoint]
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
    body: NewWebhookEndpoint,
    idempotency_key: str,
) -> APIError | WebhookEndpoint | None:
    """Register a webhook endpoint

     Registers an endpoint of your own server, which every event XipFax posts goes to from then on, as
    `webhooks` describes them, each signed with the endpoint’s own secret: the answer shows the secret,
    once, so keep it then. XipFax checks that the URL leads to an address on the internet, now and
    before each delivery. Your account keeps 16 endpoints at most, and registers 10 in an hour at most.
    An API key alone registers one, and revoking the key removes those it registered; an app’s token is
    refused `insufficient_scope`.

    Args:
        idempotency_key (str):
        body (NewWebhookEndpoint): A webhook endpoint to register: the URL of your own server that
            takes the events.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIError | WebhookEndpoint
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed

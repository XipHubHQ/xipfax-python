from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import APIError
from ...models.quote import Quote
from ...models.quote_body import QuoteBody
from ...types import Response


def _get_kwargs(
    *,
    body: QuoteBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/quote",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    body: QuoteBody,
) -> Response[APIError | Quote]:
    """Quote a fax to a number

     The price of one fax of so many pages to the number you name, sent without a plan, from XipFax’s
    price list: what its checkout charges. `plan_covers` says whether the plan covers the number: a fax
    sent on the plan counts its pages there instead. A number XipFax can’t fax is refused
    `parameter_invalid`, or `number_not_faxed` where XipFax’s price list holds no row for it. A quote
    changes nothing, so it takes no `Idempotency-Key`.

    Args:
        body (QuoteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIError | Quote]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: QuoteBody,
) -> APIError | Quote | None:
    """Quote a fax to a number

     The price of one fax of so many pages to the number you name, sent without a plan, from XipFax’s
    price list: what its checkout charges. `plan_covers` says whether the plan covers the number: a fax
    sent on the plan counts its pages there instead. A number XipFax can’t fax is refused
    `parameter_invalid`, or `number_not_faxed` where XipFax’s price list holds no row for it. A quote
    changes nothing, so it takes no `Idempotency-Key`.

    Args:
        body (QuoteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIError | Quote
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: QuoteBody,
) -> Response[APIError | Quote]:
    """Quote a fax to a number

     The price of one fax of so many pages to the number you name, sent without a plan, from XipFax’s
    price list: what its checkout charges. `plan_covers` says whether the plan covers the number: a fax
    sent on the plan counts its pages there instead. A number XipFax can’t fax is refused
    `parameter_invalid`, or `number_not_faxed` where XipFax’s price list holds no row for it. A quote
    changes nothing, so it takes no `Idempotency-Key`.

    Args:
        body (QuoteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIError | Quote]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: QuoteBody,
) -> APIError | Quote | None:
    """Quote a fax to a number

     The price of one fax of so many pages to the number you name, sent without a plan, from XipFax’s
    price list: what its checkout charges. `plan_covers` says whether the plan covers the number: a fax
    sent on the plan counts its pages there instead. A number XipFax can’t fax is refused
    `parameter_invalid`, or `number_not_faxed` where XipFax’s price list holds no row for it. A quote
    changes nothing, so it takes no `Idempotency-Key`.

    Args:
        body (QuoteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIError | Quote
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed

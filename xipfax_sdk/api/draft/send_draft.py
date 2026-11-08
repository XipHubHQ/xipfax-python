from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error import APIError
from ...models.send_draft import SendDraft
from ...models.sent import Sent
from ...types import Response


def _get_kwargs(
    *,
    body: SendDraft,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/draft/send",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> APIError | Sent | None:
    if response.status_code == 200:
        response_200 = Sent.from_dict(response.json())

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

    if response.status_code == 502:
        response_502 = APIError.from_dict(response.json())

        return response_502

    if response.status_code == 503:
        response_503 = APIError.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[APIError | Sent]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: SendDraft,
    idempotency_key: str,
) -> Response[APIError | Sent]:
    """Send the draft

     Sends the draft to the number or the office you name, as far as you let your credential send without
    you. Your API key sends it on your plan, its pages counted there; or, where you have no plan, on the
    card you saved, its price held until the fax ends. An app you connected sends it on your plan alone,
    and only where you let it send straight away. Otherwise nothing is sent or held, the draft keeps
    where you named, and the answer gives the link where the fax waits for you on xipfax.com. So does a
    draft whose cover page is on, which xipfax.com draws there: a send to an office that asks for a
    cover page marked Confidential turns it on. So do a card its bank refused or asked you to confirm,
    and a send past the 20 a day your credentials make without you. `paid_by` and `confirm_url` say
    which. A send refused changes nothing of the draft. Name the draft’s documents as `GET /draft` gives
    them: a draft whose documents aren’t these, in this order, is refused `draft_changed`, so that
    nothing you didn’t name is sent.

    Args:
        idempotency_key (str):
        body (SendDraft):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIError | Sent]
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
    body: SendDraft,
    idempotency_key: str,
) -> APIError | Sent | None:
    """Send the draft

     Sends the draft to the number or the office you name, as far as you let your credential send without
    you. Your API key sends it on your plan, its pages counted there; or, where you have no plan, on the
    card you saved, its price held until the fax ends. An app you connected sends it on your plan alone,
    and only where you let it send straight away. Otherwise nothing is sent or held, the draft keeps
    where you named, and the answer gives the link where the fax waits for you on xipfax.com. So does a
    draft whose cover page is on, which xipfax.com draws there: a send to an office that asks for a
    cover page marked Confidential turns it on. So do a card its bank refused or asked you to confirm,
    and a send past the 20 a day your credentials make without you. `paid_by` and `confirm_url` say
    which. A send refused changes nothing of the draft. Name the draft’s documents as `GET /draft` gives
    them: a draft whose documents aren’t these, in this order, is refused `draft_changed`, so that
    nothing you didn’t name is sent.

    Args:
        idempotency_key (str):
        body (SendDraft):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIError | Sent
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: SendDraft,
    idempotency_key: str,
) -> Response[APIError | Sent]:
    """Send the draft

     Sends the draft to the number or the office you name, as far as you let your credential send without
    you. Your API key sends it on your plan, its pages counted there; or, where you have no plan, on the
    card you saved, its price held until the fax ends. An app you connected sends it on your plan alone,
    and only where you let it send straight away. Otherwise nothing is sent or held, the draft keeps
    where you named, and the answer gives the link where the fax waits for you on xipfax.com. So does a
    draft whose cover page is on, which xipfax.com draws there: a send to an office that asks for a
    cover page marked Confidential turns it on. So do a card its bank refused or asked you to confirm,
    and a send past the 20 a day your credentials make without you. `paid_by` and `confirm_url` say
    which. A send refused changes nothing of the draft. Name the draft’s documents as `GET /draft` gives
    them: a draft whose documents aren’t these, in this order, is refused `draft_changed`, so that
    nothing you didn’t name is sent.

    Args:
        idempotency_key (str):
        body (SendDraft):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIError | Sent]
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
    body: SendDraft,
    idempotency_key: str,
) -> APIError | Sent | None:
    """Send the draft

     Sends the draft to the number or the office you name, as far as you let your credential send without
    you. Your API key sends it on your plan, its pages counted there; or, where you have no plan, on the
    card you saved, its price held until the fax ends. An app you connected sends it on your plan alone,
    and only where you let it send straight away. Otherwise nothing is sent or held, the draft keeps
    where you named, and the answer gives the link where the fax waits for you on xipfax.com. So does a
    draft whose cover page is on, which xipfax.com draws there: a send to an office that asks for a
    cover page marked Confidential turns it on. So do a card its bank refused or asked you to confirm,
    and a send past the 20 a day your credentials make without you. `paid_by` and `confirm_url` say
    which. A send refused changes nothing of the draft. Name the draft’s documents as `GET /draft` gives
    them: a draft whose documents aren’t these, in this order, is refused `draft_changed`, so that
    nothing you didn’t name is sent.

    Args:
        idempotency_key (str):
        body (SendDraft):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIError | Sent
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed

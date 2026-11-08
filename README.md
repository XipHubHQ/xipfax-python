# XipFax for Python

Send faxes from your code with [XipFax](https://xipfax.com): quote a fax, add your PDFs, send them to a
number or a government office, and follow each fax until it's delivered. The SDK is generated from
the API's own document, so its calls and models are the API's. It runs on Python 3.11 or later.

## Install

```sh
pip install xipfax-sdk
```

## Make an API key

Sign in to the [developer console](https://developer.xipfax.com/console/), open API keys and make a
key. You see it whole just once, so copy it then. Every key is live: what it sends is real.

Keep the key on your server. A key in a web page or an app is anyone's.

## Use it

```python
import os

from xipfax_sdk import XipFax
from xipfax_sdk.api.quote import get_quote
from xipfax_sdk.models import APIError

xipfax = XipFax(os.environ["XIPFAX_API_KEY"])

quote = get_quote.sync(client=xipfax, pages=3)
if isinstance(quote, APIError):
    raise SystemExit(f"{quote.error.code}: {quote.error.message}")
print(f"{quote.price_shown}: {quote.terms}")
```

Each call is a module of `xipfax_sdk.api`, which takes the client and what its request carries, as
the [API reference](https://developer.xipfax.com/docs/api/) names it: a path's parameters first,
then the query's and the headers' by name, and `body`, a model of `xipfax_sdk.models`. `sync`
answers the model where the API did what you asked, and `APIError` where it refused, whose
`error.code` is the one to branch on. A status the document doesn't give raises
`xipfax_sdk.errors.UnexpectedStatus`, and a request that never reached XipFax raises the error
`httpx` gave, such as `httpx.TimeoutException`.

`sync_detailed` answers the whole response too, its `status_code`, `headers` and `content` beside
`parsed`. `asyncio` and `asyncio_detailed` are the same calls for `async` code.

## The quickstart

[`examples/quickstart.py`](examples/quickstart.py) takes the steps of
[XipFax's quickstart](https://developer.xipfax.com/docs/guides/quickstart/) through the SDK. Run it
from a clone of this repository, with [uv](https://docs.astral.sh/uv/):

```sh
uv sync
XIPFAX_API_KEY=xipfax_key_live_… uv run python examples/quickstart.py
```

That takes the free steps alone: what a fax costs, and the offices that take Form 2848 from Ohio,
with their fax numbers.

To send a fax too, name a fax number of yours and a public https link to a PDF:

```sh
XIPFAX_TO='+1 202 555 0143' XIPFAX_PDF_URL=https://example.com/letter.pdf \
  XIPFAX_API_KEY=xipfax_key_live_… uv run python examples/quickstart.py
```

**That step sends a real fax, and it's charged.** Its pages count on your plan, or where you have no
plan its price is held on the card you saved, and taken once it's delivered. A fax that fails costs
nothing. The quickstart says so before it sends, and sends only once you type `send`. Then it
follows the fax until it's delivered, and gives the link to its confirmation.

## Calls

| Call                                          | Request                                        | What it does                                                                         |
| --------------------------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------ |
| `quote.get_quote`                             | `GET /quote`                                   | The price of a fax of so many pages, sent without a plan.                            |
| `draft.get_draft`                             | `GET /draft`                                   | Your draft, the fax you prepare, its documents in the order it sends them.           |
| `draft.add_document`                          | `POST /draft/documents`                        | Adds a PDF to the draft, by a link XipFax fetches or by an upload.                   |
| `draft.complete_document`                     | `POST /draft/documents/{document_id}/complete` | Reads an uploaded PDF back, its pages counted.                                       |
| `draft.remove_document`                       | `DELETE /draft/documents/{document_id}`        | Takes a document out of the draft.                                                   |
| `draft.send_draft`                            | `POST /draft/send`                             | Sends the draft to a number or an office.                                            |
| `faxes.list_faxes`                            | `GET /faxes`                                   | The faxes you sent and received, newest first, a page at a time.                     |
| `faxes.get_fax`                               | `GET /faxes/{fax_id}`                          | A fax, where it stands now.                                                          |
| `faxes.get_confirmation`                      | `GET /faxes/{fax_id}/confirmation`             | A delivered fax's confirmation, by a link that reads it for a few minutes.           |
| `plan.get_plan`                               | `GET /plan`                                    | Your plan, or none.                                                                  |
| `offices.list_offices`                        | `GET /offices`                                 | The government offices XipFax gives the fax numbers of.                              |
| `webhook_endpoints.register_webhook_endpoint` | `POST /webhook-endpoints`                      | Registers an endpoint of your server for every event, its signing secret shown once. |
| `webhook_endpoints.remove_webhook_endpoint`   | `DELETE /webhook-endpoints/{endpoint_id}`      | Takes an endpoint away: no event goes to it from then on.                            |

Each is a module of `xipfax_sdk.api`: `from xipfax_sdk.api.draft import add_document`.

### Upload a PDF from your disk

Give its size, send its bytes to the link the answer gives, then complete it:

```python
import uuid
from pathlib import Path

import httpx

from xipfax_sdk.api.draft import add_document, complete_document
from xipfax_sdk.models import DocumentAdded, NewDocument

data = Path("letter.pdf").read_bytes()
added = add_document.sync(
    client=xipfax,
    body=NewDocument(name="letter.pdf", size_bytes=len(data)),
    idempotency_key=str(uuid.uuid4()),
)
if not isinstance(added, DocumentAdded) or added.upload is None:
    raise SystemExit(f"XipFax gave no link to upload to: {added}")
upload = httpx.put(added.upload.url, headers=added.upload.headers.to_dict(), content=data)
upload.raise_for_status()
complete_document.sync(added.document.id, client=xipfax, idempotency_key=str(uuid.uuid4()))
```

## Retries and `Idempotency-Key`

`add_document`, `complete_document`, `send_draft` and `register_webhook_endpoint` take an
`idempotency_key` of your own, such as a UUID, which you keep with the request. Sent again with the
same key within 24 hours, the request is answered as it was the first time rather than done twice,
so a retry after a timeout can't send a fax twice. The SDK makes up no key itself: one it made would
be new on each try, and protect nothing.

The answer to a request sent again keeps none of its signed links, nor an endpoint's secret: a
document's `url` and an endpoint's `secret` come back None. `upload` is signed again instead while
its document is still uploading: asked for again with its key, `add_document` gives a fresh link to
send the bytes to, and None once the document is ready or removed. An endpoint whose first answer
you lost has no secret to check its deliveries by: remove it with `remove_webhook_endpoint`, and
register it again with a new key.

## Webhooks

`register_webhook_endpoint` registers an endpoint of your server, which every event goes to from
then on: when a fax you sent is delivered or fails for good, and when a fax sent to your number
arrives. Its answer shows the endpoint's signing secret once, so keep it then.
`remove_webhook_endpoint` takes an endpoint away, as revoking the key that registered it does. Both
take an API key, not an app's token.

Check each delivery's `webhook-signature` with that secret, against its body exactly as it came,
before you trust it. [XipFax's webhooks guide](https://developer.xipfax.com/docs/guides/webhooks/)
shows how. Its body is then a `FaxEvent`: `FaxEvent.from_dict(json.loads(body))`.

## Versions

Each request names the version of the API the SDK was generated from, `API_VERSION`, in its
`Xip-Version` header, so each answer keeps the shape the SDK's models describe. Where a value is one
of a set the API may add to, such as a fax's `status`, the SDK reads it as the string it is, so an
answer with a value newer than the SDK still reads.

## Where the SDK comes from

`openapi.json` is the API's document, as [api.xipfax.com](https://api.xipfax.com/openapi.json) gives
it, and `scripts/generate.sh` makes the SDK from it with
[openapi-python-client](https://github.com/openapi-generators/openapi-python-client): its models, its
client and one module for each of the document's operations. `xipfax_sdk/xipfax.py` and
`xipfax_sdk/py.typed` are the only files in `xipfax_sdk` edited by hand. To update the SDK, copy the
new document over `openapi.json`, run `scripts/generate.sh`, and commit what changes.

## Help

Write to [help@xipfax.com](mailto:help@xipfax.com).

## License

[MIT](LICENSE). The client that `scripts/generate.sh` writes in from openapi-python-client keeps its
own MIT notice, in [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).

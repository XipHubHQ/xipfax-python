"""Reads what the SDK sends and is answered against the API's document, openapi.json, as the
repository holds it: the operation a request is, and each thing in it the document refuses, from its
address, its key and its version to each parameter and its body; and what in an answer or an event's
body the document's schema refuses. It reads the schema keywords the document uses, and refuses a
schema with one it doesn't read, so that a document that comes to say more than this reads fails the
specs rather than passing unread."""

import json
import re
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import NoReturn, TypeGuard
from urllib.parse import unquote, urlsplit

import httpx

# The API's document, as the repository holds it.
DOCUMENT = Path(__file__).resolve().parent.parent / "openapi.json"

# The methods an operation may have, in the order each path's are read in.
METHODS = ("get", "put", "post", "delete", "options", "head", "patch", "trace")

# The keywords that describe a value without constraining it.
ANNOTATIONS = frozenset({"description", "title", "default", "examples"})

# Each Unicode property a pattern of the document names, as the characters it holds.
PROPERTIES = {"Cc": r"\x00-\x1f\x7f-\x9f", "Zl": r"\u2028", "Zp": r"\u2029"}

BEARER = re.compile(r"Bearer \S+\Z")

# A whole number, as a parameter's text or a status gives one.
INTEGER = re.compile(r"[+-]?[0-9]+")

# A parameter's place in a path, {fax_id}.
PATH_PARAMETER = re.compile(r"\{([^}]+)\}")

# A pattern's pieces: an escape, \p{Name} among them, or one character.
PIECE = re.compile(r"\\p\{(\w+)\}|\\.|.", re.DOTALL)


@dataclass(frozen=True)
class Parameter:
    """A parameter of an operation."""

    name: str
    # Where it is sent: query, header or path.
    location: str
    required: bool
    schema: dict[str, object]


@dataclass(frozen=True)
class Operation:
    """One operation of the document."""

    id: str
    method: str
    path: str
    # The first status of 2xx it answers.
    success: int
    parameters: list[Parameter]
    # The schema of its JSON body, None where it takes none.
    body: dict[str, object] | None
    responses: dict[str, object]
    # Its path on the document's server, each of its parameters' places in it a group.
    pattern: re.Pattern[str]
    # The name of each of its path's parameters, in the order of their groups.
    names: list[str]


class Document:
    """The API's document."""

    def __init__(self, raw: dict[str, object]) -> None:
        self.raw = raw
        # The document's info.version, the version of the API it is.
        self.version = _text(_object(raw.get("info")).get("version"))
        servers = _list(raw.get("servers"))
        if not servers:
            raise ValueError("the document names no server")
        self.server = urlsplit(_text(_object(servers[0]).get("url")))

        # The document's operations, by their paths in order and the method within each.
        self.operations: list[Operation] = []
        paths = _object(raw.get("paths"))
        for route in sorted(paths):
            item = _object(paths[route])
            for method in METHODS:
                if isinstance(item.get(method), dict):
                    self.operations.append(self._operation(route, method, item))

        # The schema of the body each event posts, by the event's name.
        self.webhooks: dict[str, dict[str, object]] = {}
        for name, value in _object(raw.get("webhooks")).items():
            try:
                schema = self._body_schema(_object(_object(value).get("post")))
            except ValueError as error:
                raise ValueError(f"the webhook {name}: {error}") from error
            if schema is None:
                raise ValueError(f"the webhook {name} posts no JSON body the document gives")
            self.webhooks[name] = schema

    def _operation(self, route: str, method: str, item: dict[str, object]) -> Operation:
        """The operation of a path's item by its method."""
        entry = _object(item[method])
        operation_id = _text(entry.get("operationId"))
        try:
            declared: dict[str, Parameter] = {}
            for owner in (item, entry):
                for value in _list(owner.get("parameters")):
                    found = self.resolve(value)
                    parameter = Parameter(
                        name=_text(found.get("name")),
                        location=_text(found.get("in")),
                        required=found.get("required") is True,
                        schema=_object(found.get("schema")),
                    )
                    # One the operation names again, in the same place, stands in for the path's.
                    declared[f"{parameter.location}:{parameter.name.lower()}"] = parameter
            body = self._body_schema(entry)
        except ValueError as error:
            raise ValueError(f"{operation_id}: {error}") from error

        responses = _object(entry.get("responses"))
        success = 0
        for status in sorted(responses):
            if INTEGER.fullmatch(status) and 200 <= int(status) < 300:
                success = int(status)
                break

        # The path on the document's server, each {name} in it a segment of its own.
        parts = PATH_PARAMETER.split(self.server.path.removesuffix("/") + route)[::2]
        return Operation(
            id=operation_id,
            method=method.upper(),
            path=route,
            success=success,
            parameters=list(declared.values()),
            body=body,
            responses=responses,
            pattern=re.compile("([^/]+)".join(re.escape(part) for part in parts)),
            names=PATH_PARAMETER.findall(route),
        )

    def _body_schema(self, entry: dict[str, object]) -> dict[str, object] | None:
        """The schema of the JSON body an operation takes, or an event posts; None where it takes
        none."""
        if "requestBody" not in entry:
            return None
        content = _object(self.resolve(entry["requestBody"]).get("content"))
        media = content.get("application/json")
        if not isinstance(media, dict):
            raise ValueError("its body is not JSON")
        schema = media.get("schema")
        return schema if isinstance(schema, dict) else None

    def resolve(self, value: object) -> dict[str, object]:
        """The object a value is, following each $ref it holds to what it names in the document."""
        found = _object(value)
        while isinstance(ref := found.get("$ref"), str):
            found = self.pointer(ref)
        return found

    def pointer(self, ref: str) -> dict[str, object]:
        """The object a local reference, #/components/schemas/Fax, names."""
        if not ref.startswith("#/"):
            raise ValueError(f"{ref} is no reference into the document")
        value: object = self.raw
        for part in ref.removeprefix("#/").split("/"):
            if not isinstance(value, dict):
                raise ValueError(f"{ref} names nothing in the document")
            value = value.get(part.replace("~1", "/").replace("~0", "~"))
        if not isinstance(value, dict):
            raise ValueError(f"{ref} names nothing in the document")
        return value

    def find(self, request: httpx.Request) -> tuple[Operation, dict[str, str]] | None:
        """The operation a request is, by its method and path on the document's server, with the
        value of each of its path's parameters; None where it is no operation of the document."""
        url = request.url
        if url.scheme != self.server.scheme or url.netloc.decode("ascii") != self.server.netloc:
            return None
        path = url.raw_path.partition(b"?")[0].decode("ascii")
        for operation in self.operations:
            if operation.method != request.method:
                continue
            match = operation.pattern.fullmatch(path)
            if match is not None:
                values = [unquote(value) for value in match.groups()]
                return operation, dict(zip(operation.names, values))
        return None

    def read_request(self, request: httpx.Request, version: str) -> tuple[str, list[str]]:
        """Reads a request against the document: the id of the operation it is, and each thing in
        it the document refuses, none where it fits. Its Xip-Version must name version."""
        found = self.find(request)
        if found is None:
            return "", [f"{request.method} {request.url} is no operation of the document"]
        operation, values = found
        refused: list[str] = []
        keys = request.headers.get_list("Authorization")
        if len(keys) != 1 or BEARER.match(keys[0]) is None:
            refused.append(f"Authorization is {_quoted_list(keys)}, not one bearer key")
        versions = request.headers.get_list("Xip-Version")
        if versions != [version]:
            refused.append(f"Xip-Version is {_quoted_list(versions)}, not {version}")

        query = request.url.params
        takes_query: set[str] = set()
        for parameter in operation.parameters:
            given: list[str] = []
            if parameter.location == "query":
                takes_query.add(parameter.name)
                given = query.get_list(parameter.name)
            elif parameter.location == "header":
                given = request.headers.get_list(parameter.name)
            elif parameter.location == "path" and parameter.name in values:
                given = [values[parameter.name]]
            at = f"{parameter.location} {parameter.name}"
            if len(given) > 1:
                refused.append(f"{at} is sent {len(given)} times")
            elif given:
                refused += self.check_text(parameter.schema, given[0], at)
            elif parameter.required:
                refused.append(f"{at} is missing")
        for name in sorted(query.keys()):
            if name not in takes_query:
                refused.append(f"query {name} is no parameter of {operation.id}")

        if operation.body is not None:
            if not request.headers.get("Content-Type", "").startswith("application/json"):
                refused.append("the body is not sent as JSON")
            try:
                value = _json(request.content)
            except ValueError as error:
                refused.append(f"the body is no JSON: {error}")
            else:
                refused += self.check(operation.body, value, "body")
        elif request.content:
            refused.append("a body the operation takes none of")
        return operation.id, refused

    def read_answer(self, request: httpx.Request, status: int, body: str) -> list[str]:
        """Reads an answer to a request against the document: what in it the operation's answer for
        its status refuses, none where it fits. An empty body is an answer that carries none."""
        found = self.find(request)
        if found is None:
            return [f"{request.method} {request.url} is no operation of the document"]
        operation = found[0]
        answer = operation.responses.get(str(status))
        if answer is None:
            return [f"{operation.id} gives no {status}"]
        try:
            response = self.resolve(answer)
        except ValueError as error:
            return [str(error)]
        content = response.get("content")
        if not isinstance(content, dict):
            return [f"{operation.id}'s {status} carries no body"] if body else []
        schema = _object(_object(content.get("application/json")).get("schema"))
        try:
            value = _json(body)
        except ValueError as error:
            return [f"{operation.id}'s {status} is no JSON: {error}"]
        return self.check(schema, value, "answer")

    def version_refused(self, operation: Operation, version: str) -> list[str]:
        """What the operation's Xip-Version parameter refuses in version, none where it takes it."""
        for parameter in operation.parameters:
            if parameter.location == "header" and parameter.name == "Xip-Version":
                return self.check_text(parameter.schema, version, "header Xip-Version")
        return [f"{operation.id} takes no Xip-Version"]

    def check_text(self, schema: dict[str, object], text: str, at: str) -> list[str]:
        """Checks a parameter's text, read as its schema's type, against the schema."""
        try:
            target = self.resolve(schema)
        except ValueError as error:
            return [f"{at}: {error}"]
        if target.get("type") == "integer":
            if INTEGER.fullmatch(text) is None:
                return [f"{at} is {_quoted(text)}, no integer"]
            return self.check(schema, int(text), at)
        return self.check(schema, text, at)

    def check(self, schema: dict[str, object], value: object, at: str) -> list[str]:
        """What the schema refuses in value, a value as json.loads reads JSON, each thing at its
        place from at; none where it fits."""
        refused: list[str] = []
        for keyword in sorted(schema):
            rule = schema[keyword]
            match keyword:
                case "$ref":
                    try:
                        target = self.pointer(str(rule))
                    except ValueError as error:
                        refused.append(f"{at}: {error}")
                    else:
                        refused += self.check(target, value, at)
                case "type":
                    if not _has_type(rule, value):
                        refused.append(f"{at} is {_type_of(value)}, not {_plain(rule)}")
                case "enum":
                    if not any(_same(allowed, value) for allowed in _list(rule)):
                        refused.append(f"{at} is {_plain(value)}, none of {_plain(rule)}")
                case "const":
                    if not _same(rule, value):
                        refused.append(f"{at} is {_plain(value)}, not {_plain(rule)}")
                case "minLength" | "maxLength":
                    if isinstance(value, str) and _past(keyword, len(value), rule):
                        refused.append(f"{at} has {len(value)} characters, {_limit(keyword, rule)}")
                case "pattern":
                    if isinstance(value, str):
                        refused += _unmatched(rule, value, at)
                case "minimum" | "maximum":
                    if _is_number(value) and _past(keyword, value, rule):
                        refused.append(f"{at} is {_plain(value)}, {_limit(keyword, rule)}")
                case "minItems" | "maxItems":
                    if isinstance(value, list) and _past(keyword, len(value), rule):
                        refused.append(f"{at} has {len(value)} items, {_limit(keyword, rule)}")
                case "items":
                    if isinstance(value, list) and isinstance(rule, dict):
                        for index, item in enumerate(value):
                            refused += self.check(rule, item, f"{at}[{index}]")
                case "properties":
                    if isinstance(value, dict) and isinstance(rule, dict):
                        for name in sorted(rule):
                            if name in value and isinstance(rule[name], dict):
                                refused += self.check(rule[name], value[name], f"{at}.{name}")
                case "required":
                    if isinstance(value, dict):
                        for name in _list(rule):
                            if _plain(name) not in value:
                                refused.append(f"{at}.{_plain(name)} is missing")
                case "additionalProperties":
                    if isinstance(value, dict):
                        named = _object(schema.get("properties"))
                        for name in sorted(value):
                            if name in named:
                                continue
                            if rule is False:
                                refused.append(f"{at}.{name} is no member it takes")
                            elif isinstance(rule, dict):
                                refused += self.check(rule, value[name], f"{at}.{name}")
                case "propertyNames":
                    if isinstance(value, dict) and isinstance(rule, dict):
                        for name in sorted(value):
                            refused += self.check(rule, name, f"{at} name {name}")
                case "anyOf":
                    members = [member for member in _list(rule) if isinstance(member, dict)]
                    if all(self.check(member, value, at) for member in members):
                        refused.append(f"{at} fits none of its anyOf")
                case _ if keyword not in ANNOTATIONS:
                    unread = f"the contract reads no {keyword}, which its schema gives"
                    refused.append(f"{at}: {unread}")
        return refused


@cache
def load() -> Document:
    """The API's document, as the repository holds it, read once."""
    return Document(_object(json.loads(DOCUMENT.read_text(encoding="utf-8"))))


def _object(value: object) -> dict[str, object]:
    """The value as a JSON object, or an empty one where it is none."""
    return value if isinstance(value, dict) else {}


def _list(value: object) -> list[object]:
    """The value as a JSON array, or an empty one where it is none."""
    return value if isinstance(value, list) else []


def _text(value: object) -> str:
    """The value as a JSON string, or an empty one where it is none."""
    return value if isinstance(value, str) else ""


def _json(text: str | bytes) -> object:
    """The value JSON text holds, refusing NaN and the infinities, which JSON has no words for."""
    return json.loads(text, parse_constant=_no_constant)


def _no_constant(name: str) -> NoReturn:
    """Refuses a word for a number that JSON doesn't have."""
    raise ValueError(f"{name} is no JSON value")


def _is_number(value: object) -> TypeGuard[float]:
    """Whether value is a JSON number, which a bool never is here."""
    return isinstance(value, int | float) and not isinstance(value, bool)


def _past(keyword: str, amount: float, limit: object) -> bool:
    """Whether amount is past a schema's limit: under it for a min keyword, over it for a max one,
    and never where the limit is no number."""
    if not _is_number(limit):
        return False
    return amount < limit if keyword.startswith("min") else amount > limit


def _limit(keyword: str, rule: object) -> str:
    """The words for a value past a schema's limit."""
    return f"past its {keyword} of {_plain(rule)}"


def _unmatched(rule: object, text: str, at: str) -> list[str]:
    """What a schema's pattern refuses in text: none where the pattern matches it."""
    try:
        expression = _pattern(str(rule))
    except (re.error, ValueError) as error:
        return [f"{at}: its pattern {_plain(rule)} doesn't compile: {error}"]
    if expression.search(text) is None:
        return [f"{at} is {_quoted(text)}, not of the pattern {_plain(rule)}"]
    return []


@cache
def _pattern(source: str) -> re.Pattern[str]:
    r"""A schema's pattern, ECMA-262's as JSON Schema gives it, as Python reads it. Outside a set of
    characters, $ is \Z, since ECMA-262's $ matches only at the end of the text, where Python's also
    matches before a last line break; and each \p{...} the document names is the characters it
    holds. Any other escape of a letter or a digit, and a . outside a set, which Python reads
    otherwise, are refused rather than read wrong."""
    pieces: list[str] = []
    in_set = False
    for piece in PIECE.finditer(source):
        text, name = piece.group(0), piece.group(1)
        if name is not None:
            if name not in PROPERTIES:
                raise ValueError(f"the specs read no \\p{{{name}}}")
            text = PROPERTIES[name] if in_set else f"[{PROPERTIES[name]}]"
        elif text.startswith("\\"):
            if text[1:].isalnum():
                raise ValueError(f"the specs read no {text}")
        elif in_set:
            in_set = text != "]"
        elif text == "$":
            text = r"\Z"
        elif text == ".":
            raise ValueError("the specs read no . outside a set of characters")
        else:
            in_set = text == "["
        pieces.append(text)
    return re.compile("".join(pieces))


def _has_type(rule: object, value: object) -> bool:
    """Whether value is of the type, or one of the types, a schema's type names."""
    if isinstance(rule, str):
        return _is_type(rule, value)
    return any(_is_type(str(name), value) for name in _list(rule))


def _is_type(name: str, value: object) -> bool:
    """Whether value is of the JSON type name."""
    match name:
        case "null":
            return value is None
        case "boolean":
            return isinstance(value, bool)
        case "string":
            return isinstance(value, str)
        case "number":
            return _is_number(value)
        case "integer":
            return _is_number(value) and (isinstance(value, int) or value.is_integer())
        case "array":
            return isinstance(value, list)
        case "object":
            return isinstance(value, dict)
    return False


def _type_of(value: object) -> str:
    """The narrowest JSON type value is of."""
    for name in ("null", "boolean", "integer", "number", "string", "array", "object"):
        if _is_type(name, value):
            return name
    return type(value).__name__


def _same(one: object, other: object) -> bool:
    """Whether two JSON values are the same: numbers by their values, never a bool and a number,
    and lists and objects by each item and member."""
    if isinstance(one, bool) or isinstance(other, bool):
        return one is other
    if _is_number(one) and _is_number(other):
        return one == other
    if isinstance(one, list) and isinstance(other, list):
        return len(one) == len(other) and all(map(_same, one, other))
    if isinstance(one, dict) and isinstance(other, dict):
        return one.keys() == other.keys() and all(_same(one[key], other[key]) for key in one)
    return type(one) is type(other) and one == other


def _plain(value: object) -> str:
    """A value as the reader's sentences write it: a text as it is, a list as its items between
    brackets, a whole number with no point, and null, true and false by their names."""
    if value is None or isinstance(value, bool):
        return json.dumps(value)
    if isinstance(value, float) and value.is_integer() and abs(value) < 1e21:
        return str(int(value))
    if isinstance(value, list):
        return "[" + " ".join(_plain(item) for item in value) + "]"
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def _quoted(text: str) -> str:
    """The text between double quotes, each character JSON escapes escaped."""
    return json.dumps(text, ensure_ascii=False)


def _quoted_list(texts: list[str]) -> str:
    """The texts, each quoted, between brackets."""
    return "[" + " ".join(_quoted(text) for text in texts) + "]"

# Writes the document openapi-python-client generates the SDK from, out of openapi.json, the API's
# document. Each step sets aside what XipFax, the SDK's client, sends itself, or what the generated
# code would read more narrowly than the API answers, and refuses a document whose shape the step
# doesn't know, so that a change there is looked at before the SDK is generated from it.

def operations(f): .paths |= map_values(map_values(if type == "object" then f else . end));

# The SDK takes an API key alone, as the TypeScript SDK does, and XipFax sends it on every request.
# The document's security, which also names an app's token, is set aside, so every call takes the
# client alike.
if (.components.securitySchemes | keys) != ["apiKey", "appToken"]
  or .components.securitySchemes.apiKey.type != "http"
  or .components.securitySchemes.apiKey.scheme != "bearer"
then error("openapi.json's security schemes aren't apiKey, a bearer token, and appToken: see what the SDK should offer before generating it")
else . end
| del(.components.securitySchemes, .security)
| operations(del(.security))

# XipFax names API_VERSION in Xip-Version on every request, so no call takes a version of its own.
| .info.version as $version
| if (.components.parameters.XipVersion | .name != "Xip-Version" or .in != "header" or (.required // false) or .schema.enum != [$version]) then
    error("openapi.json's Xip-Version isn't an optional header taking \($version) alone: see how the SDK should offer a choice of versions before generating it")
  else . end
| operations(if has("parameters") then .parameters |= map(select(. != {"$ref": "#/components/parameters/XipVersion"})) else . end)
| del(.components.parameters.XipVersion)
| if [.. | objects | select(.name? == "Xip-Version" or ."$ref"? == "#/components/parameters/XipVersion")] != [] then
    error("openapi.json names Xip-Version somewhere other than its parameter XipVersion: see how the SDK should send it before generating it")
  else . end

# An answer's set of values may gain one within its version, which the SDK reads rather than refuses,
# as the document's Additions rule asks: each enum under the schemas is set aside, and its value is
# read as the string it is, the schema's description still naming the values the version gives. The
# schemas only answers use are the ones set aside: so the step refuses a request body that isn't
# JSON by a reference to one of the schemas, a schema a request body names that holds an enum or a
# reference of its own, and an enum on anything but a string. A request's parameters keep theirs.
| . as $document
| [.paths[][] | objects | select(has("requestBody")) | .requestBody] as $bodies
| if [$bodies[] | select(
      (.content | type) != "object"
      or (.content | keys) != ["application/json"]
      or (.content["application/json"].schema | type) != "object"
      or (.content["application/json"].schema | keys) != ["$ref"]
      or (.content["application/json"].schema."$ref" | type) != "string"
      or (.content["application/json"].schema."$ref" | startswith("#/components/schemas/") | not)
      or ($document.components.schemas[.content["application/json"].schema."$ref" | ltrimstr("#/components/schemas/")] | type) != "object"
    )] != [] then
    error("a request body in openapi.json isn't JSON by a reference to one of its schemas: see how the SDK should read its values before generating it")
  else . end
| if [$bodies[] | .content["application/json"].schema."$ref" | ltrimstr("#/components/schemas/") | $document.components.schemas[.] | .. | objects | select((.enum? | type == "array") or has("$ref"))] != [] then
    error("a schema a request body names holds an enum or a reference: see how the SDK should read an answer's values apart from a request's before generating it")
  else . end
| if [.components.schemas | .. | objects | select(.enum? | type == "array") | select(.type != "string")] != [] then
    error("an enum under openapi.json's schemas isn't on a string: see how the SDK should read it before generating it")
  else . end
| .components.schemas |= walk(if type == "object" and (.enum? | type == "array") then del(.enum) else . end)

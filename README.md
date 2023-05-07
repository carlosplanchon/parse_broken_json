# parse_broken_json

Small lib to help parsing broken or invalid JSONs

It only consists of one function:

parse_broken_json(text: str, allowed_keys: list[str]) -> Any:

text is the json to be parsed, allowed_keys are the keys allowed on
the JSON nodes.

Internally, this library uses the interpreter pattern.

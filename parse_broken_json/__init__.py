#!/usr/bin/env python3

import decimal
import io
import json

import ijson

from typing import Any



class JSONEventPartialItpr:
    def __init__(self, text: str, allowed_keys: list[str]) -> None:
        self.text: str = text
        self.allowed_keys = allowed_keys

        # Escape backslashes.
        self.text: str = text.replace("\\", "\\\\")

        self.parsed_objects = []

        self.prefix: str | None = None
        self.event: str | None = None
        self.value: str | None = None

        self.actual_element = {}
        return None

    def advance(self):
        try:
            prefix, event, value = next(self.parse_event)
            self.prefix = prefix
            self.event = event
            self.value = value
            # print("*" * 50)
            # print(f"Prefix: {prefix}")
            # print(f"Event: {event}")
            # print(f"Value: {value}")
        except Exception as e:
            # print(f"Exception: {e}")
            raise StopIteration

    def eat(self) -> None:
        while self.value != "skip":
            self.eat_element()

    def eat_element(self) -> dict[str, str] | None:
        self.eat_startmap()
        self.eat_key_values()
        if self.event != "end_map":
            return None

        self.eat_endmap()

    def eat_startmap(self) -> None:
        while self.event != "start_map":
            self.advance()

        if self.event == "start_map":
            # print(">>> INTERPRETER > START_MAP FOUND !!!")
            self.reset_element()

    def reset_element(self) -> None:
        # print(">>> INTERPRETER > RESETTING ELEMENT!!!")
        self.actual_element = {}

    def eat_key_values(self) -> None:
        self.advance()
        # print(">>> STARTING EAT KEY VALUES")
        while self.event in [
                "map_key", "string", "number", "boolean", "null"]:
            key: str | None = self.eat_key()
            self.advance()
            value: str | None = self.eat_value()

            # print(f"> Key: {key}, Value: {value}")

            if key is not None and value is not None:
                self.actual_element[key] = value

        # print(">>> ENDING EAT KEY VALUES")
        return None

    def eat_key(self) -> str | None:
        if self.event == "map_key":
            if self.value in self.allowed_keys:
                return self.value
        return None

    def eat_value(self) -> str | None:
        if self.event in ["string", "number", "boolean", "null"]:
            if self.event == "null":
                return "None"
            return self.value
        return None

    def eat_endmap(self) -> None:
        while self.event != "end_map":
            self.advance()

        if self.event == "end_map":
            # print(">>> INTERPRETER > END_MAP FOUND !!!")
            self.add_element()

    def add_element(self) -> None:
        if self.actual_element != {}:
            # print(">>> INTERPRETER > ADDING ELEMENT!!!")
            self.parsed_objects.append(self.actual_element)
            self.reset_element()

    def traverse_events(self) -> None:
        f = io.StringIO(self.text)
        self.parse_event = ijson.parse(f, use_float=True)

        try:
            while self.value != "skip":
                self.eat()
        except StopIteration as e:
            # print(f"StopIteration: {e}")
            self.add_element()
            return None

        return None


def remove_leading_unwanted_text(text: str) -> str:
    rect_index: int | None = None
    curvy_index: int | None = None

    if "[" in text:
        rect_index = text.index("[")
    if "{" in text:
        curvy_index = text.index("{")

    if (rect_index, curvy_index) == (None, None):
        cut_index: int = 0
    elif rect_index is None and curvy_index is not None:
        cut_index = curvy_index
    elif rect_index is not None and curvy_index is None:
        cut_index = rect_index
    else:
        cut_index: int = min([rect_index, curvy_index])

    text: str = text[cut_index:]

    if text.endswith("\n"):
        text = text[:-1]

    return text


def parse_broken_json(text: str, allowed_keys: list[str]) -> Any:
    text: str = remove_leading_unwanted_text(text=text)

    if text.rstrip("\n ").endswith("None"):
        return []

    try:
        parsed_json = json.loads(text)
        return parsed_json
    except Exception as e:
        ...

    if text.startswith("{") and text.endswith("}"):
        text: str = f"[{text}]"

    f = io.StringIO(text)

    objects = ijson.items(f, "item", use_float=True)

    parsed_objs = []
    i = 0
    while True:
        try:
            parsed_obj = next(objects)
            parsed_objs.append(parsed_obj)
            i += 1
        except Exception as e:
            break

    if len(parsed_objs) > 0:
        return parsed_objs

    json_partial_itpr = JSONEventPartialItpr(
        text=text,
        allowed_keys=allowed_keys
    )
    json_partial_itpr.traverse_events()

    if json_partial_itpr.parsed_objects != []:
        return json_partial_itpr.parsed_objects

    return None

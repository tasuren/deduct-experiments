from __future__ import annotations

__all__ = ("ParsedRule", "Kind", "parse")

from typing import Final, Literal

from MeCab import Tagger

wakati: Final = Tagger("-Owakati")
simple: Final = Tagger()


type Kind = Literal["object", "const"]


class ParsedRule:
    def __init__(
        self, composition: list[bool], args: list[str], syntax: list[str]
    ) -> None:
        self.composition = composition
        self.args = args
        self.syntax = syntax

    def eq_rule(self, another: ParsedRule) -> bool:
        return self.syntax == another.syntax


def parse(line: str) -> ParsedRule:
    args = []
    syntax = []
    composition = []

    for line in simple.parse(line).splitlines():
        if line == "EOS":
            break

        text, feature = line.split("\t")

        if feature[:2] == "名詞":
            if feature[3:5] == "接尾":
                args[-1] = f"{args[-1]}{text}"
            else:
                args.append(text)
                composition.append(True)
        else:
            syntax.append(text)
            composition.append(False)

    return ParsedRule(composition, args, syntax)

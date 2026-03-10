from collections.abc import Iterable, Sequence

from deduct_alpha.model import Effect as BaseEffect
from deduct_alpha.model import Entity, Object
from deduct_alpha.model import Rule as BaseRule
from deduct_ja.parser import parse


def make_line(
    composition: Iterable[bool], args: Sequence[Object], syntax: Sequence[str]
):
    line = ""
    args_index = 0
    syntax_index = 0

    for is_name in composition:
        if is_name:
            line += str(args[args_index])
            args_index += 1
        else:
            line += syntax[syntax_index]
            syntax_index += 1

    return line


class Rule(BaseRule):
    def __init__(
        self,
        line: str,
        generics: list[str],
        premise: list[BaseEffect],
        conclusion: list[BaseEffect],
        *,
        entities: list[str],
    ) -> None:
        raw = parse(line)
        self.composition = raw.composition

        # 引数が正しいか検証を行う。
        for obj in raw.args:
            if obj not in generics and obj not in entities:
                raise ValueError("宣言されていないジェネリクスが使われています。")

        # 初期化する。
        args = [Entity(obj) if obj in entities else obj for obj in raw.args]
        self.syntax = raw.syntax
        identifier = "%s-%s-%s" % (
            self.syntax,
            self.syntax[:-1],
            tuple(filter(lambda a: isinstance(a, Entity), args)),
        )

        super().__init__(
            identifier,
            args,
            premise,
            conclusion,
        )

    def __eq__(self, another: object) -> bool:
        return isinstance(another, Rule) and self.identifier == another.identifier

    def __str__(self) -> str:
        return make_line(self.composition, self.args, self.syntax)


class Effect(BaseEffect):
    def __init__(self, line: str, rules: list[Rule], entities: list[str]) -> None:
        raw = parse(line)
        self.composition = raw.composition
        self.syntax = raw.syntax

        # ルールを特定する。
        for rule in rules:
            if rule.syntax == raw.syntax:
                base = rule
                break
        else:
            raise ValueError(
                f"エフェクト「{line}」で使われているルールが見つかりいませんでした。"
            )

        # ジェネリクスの関連付けを特定する。
        associated = {}
        self.arg_keys = []

        for i, arg in enumerate(base.args):
            if isinstance(arg, str):
                if raw.args[i] in entities:
                    associated[arg] = Entity(raw.args[i])
                else:
                    associated[arg] = raw.args[i]
                self.arg_keys.append(arg)

        super().__init__(base, associated)

    def __str__(self) -> str:
        return make_line(
            self.composition,
            tuple(self.associated[key] for key in self.arg_keys),
            self.syntax,
        )

from collections import deque

import yaml

from deduct_alpha import Checker
from deduct_alpha.model import Entity
from deduct_ja.model import Effect, Rule


def load(path: str) -> Checker:
    with open(path, "r") as f:
        data = yaml.load(f, yaml.Loader)

    entities = data["エンティティ"]

    rules = []
    for rule in data["ルール"]:
        rules.append(
            Rule(
                rule["内容"],
                rule["ジェネリクス"],
                [Effect(line, rules, entities) for line in rule.get("前提", [])],
                [Effect(line, rules, entities) for line in rule.get("結論", [])],
                entities=entities,
            )
        )

    theory = [Effect(line, rules, entities) for line in data["理論"].splitlines()]

    return Checker(deque(theory), list(map(Entity, entities)), {})

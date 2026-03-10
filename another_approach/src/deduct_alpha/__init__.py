__all__ = ("Checker",)

from collections import deque
from collections.abc import Iterator

from deduct_alpha.model import Effect, Entity, Object


class Checker(Iterator):
    def __init__(
        self,
        theory: deque[Effect],
        entities: list[Entity],
        context: dict[str, Object],
    ) -> None:
        self.theory = theory
        self.entities = entities
        self.context = context

        self.state = list[Effect]()

        for i, effect in enumerate(theory):
            for obj in effect.associated.values():
                self._validate_theory_associate(i, obj)

    def _validate_theory_associate(self, i: int, obj: Object) -> None:
        template = (
            f"渡された理論の{i}番目のエフェクトには%s%sが使われていましたが、"
            "これはチェッカーに設定されていません。"
        )

        match obj:
            case Entity() if obj not in self.entities:
                raise ValueError(template % ("エンティティ", obj.identifier))
            case str() if obj not in self.context:
                raise ValueError(template % ("ジェネリック", obj))

    def check_premise(self, effect: Effect) -> None:
        effect = effect.hydrate(self.context)

        for i, premise_effect in enumerate(effect.rule.premise):
            hydrated = premise_effect.hydrate(effect.associated)

            # 前提を満たしているかを確認。
            try:
                self.state.remove(hydrated)
            except ValueError:
                raise ValueError(f"エフェクトの{i}番目の前提が満たされていません。")

    def apply_effect(self, effect: Effect) -> None:
        # エフェクトを適用する。
        if effect.rule.conclusion:
            for conclusion_effect in effect.rule.conclusion:
                self.state.append(conclusion_effect.hydrate(effect.associated))
        else:
            self.state.append(effect)

    def __next__(self) -> Effect:
        effect = self.theory.popleft()

        self.check_premise(effect)
        self.apply_effect(effect)

        return effect

    def __iter__(self) -> Iterator[Effect]:
        while self.theory:
            yield next(self)

    def check_all(self) -> None:
        for _ in self:
            pass

from collections import deque

from deduct_alpha import Checker
from deduct_alpha.model import Effect, Entity, Rule

having = Rule("持つ", ["S", "O"], [], [])
give = Rule(
    "渡す",
    ["X", "Y", "O"],
    [Effect(having, {"S": "X", "O": "O"})],
    [Effect(having, {"S": "Y", "O": "O"})],
)

takagi = Entity("髙木")
cat = Entity("猫")
marisa = Entity("魔理沙")

theory = deque(
    (
        Effect(having, {"S": takagi, "O": cat}),
        Effect(give, {"X": takagi, "Y": marisa, "O": cat}),
    )
)

checker = Checker(theory, [takagi, cat, marisa], {})
checker.check_all()

print("\n".join(map(str, checker.state)))

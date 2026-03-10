from sys import argv

from deduct_ja.loader import load

checker = load(argv[-1])
checker.check_all()

for effect in checker.state:
    print(effect)

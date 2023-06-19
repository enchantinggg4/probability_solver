from collections import namedtuple
from typing import List


clrs = ["R", "B"]
Card = namedtuple("Card", ["letter", "color"])
State = namedtuple("State", ["prefixes", "suffixes"])
Condition = namedtuple("Condition", ["operator", "pool"])

prefix_pool = ["J", "A", "K", "Q", "B"]
suffix_pool = ["10", "9", "8", "7", "6"]

prefix_pool = sum([
    [Card(c, clr) for clr in clrs] for c in prefix_pool
], [])

suffix_pool = sum([
    [Card(c, clr) for clr in clrs] for c in suffix_pool
], [])


def any_state() -> State:
    return State(Condition('or', prefix_pool), Condition('or', suffix_pool))


def only_color(pool: List[Card], clr: str) -> List[Card]:
    return [x for x in pool if x.color == clr]

# def and_or_state(card)

from collections import namedtuple
from typing import List


clrs = ["R", "B"]
Card = namedtuple("Card", ["letter", "color"])
State = namedtuple("State", ["conditions"])
Condition = namedtuple("Condition", ["operator", "pool"])
BiCondition = namedtuple("BiCondition", ["operator", "affix"])

prefix_pool = ["J", "A", "K", "Q", "B"]
suffix_pool = ["10", "9", "8", "7", "6"]

prefix_pool = sum([[Card(c, clr) for clr in clrs] for c in prefix_pool], [])

suffix_pool = sum([[Card(c, clr) for clr in clrs] for c in suffix_pool], [])


def any_state() -> State:
    return State(Condition("or", prefix_pool), Condition("or", suffix_pool))


def only_color(pool: List[Card], clr: str) -> List[Card]:
    return [x for x in pool if x.color == clr]


# def and_or_state(card)


# J & 6,7 OR K & 8,9
BiCondition("or", [
    # J & 6,7
    BiCondition('and', [
        # prefix
        Condition('or', [
            Card('J', 'K'),
            Card('J', 'B'),
        ]),
        Condition('or', [
            
        ])
        # suffix
    ])
])

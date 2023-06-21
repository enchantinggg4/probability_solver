from typing import List
from logical_types import (
    Condition,
    State,
    Card,
    prefix_pool,
    suffix_pool,
    any_state,
    only_color,
)
from util import state_chance


def add_probs(s1: State, pool: List[tuple[List | bool, List | bool]]) -> float:
    s = 0
    per_b = 1 / len(pool)
    for pp, sp in pool:
        p0 = state_chance(s1.prefixes, _pp=pp, _sp=sp) if type(pp) is list else 1
        s0 = state_chance(s1.suffixes, _pp=pp, _sp=sp) if type(sp) is list else 1
        s += p0 * s0 * per_b  # todo mb not even probabilitie of P(b)

    return s


def full_random_roll(s1: State) -> tuple[State, float]:
    prob = add_probs(s1, [(prefix_pool, suffix_pool)])
    return any_state(), prob


def prefix_reroll(s1: State) -> tuple[State, float]:
    p_prob = add_probs(s1, [(prefix_pool, True)])

    return State(Condition("or", prefix_pool), s1.suffixes), p_prob


def roll_guarantee_red(s1: State) -> tuple[State, float]:
    prob2 = add_probs(
        s1,
        [
            (only_color(prefix_pool, "R"), suffix_pool),
            (prefix_pool, only_color(suffix_pool, "R")),
        ],
    )

    return any_state(), prob2


def reroll_randomly(s1: State) -> tuple[State, float]:
    prob = add_probs(s1, [(prefix_pool, True), (True, suffix_pool)])

    s0 = State(Condition("or", []))

    return s0, prob

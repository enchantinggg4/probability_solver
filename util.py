from functools import reduce
from logical_types import State,  Condition, Card, suffix_pool, prefix_pool


def prob_add_excl(x, y):
    return x + y - x * y


def prob_add(x, y):
    return x + y


# By default = random pick
# How to add modifiers?


def state_chance(card: Condition | Card, _pp=prefix_pool, _sp=suffix_pool):
    if isinstance(card, Card):
        ap = _sp if card in suffix_pool else _pp
        if card not in ap:
            return 0.0
        else:
            return 1 / len(ap)

    if card.operator == 'and':
        return reduce(lambda x, y: x * y, [state_chance(it, _pp, _sp) for it in card.pool])
    elif card.operator == 'or':
        return reduce(prob_add, [state_chance(it, _pp, _sp) for it in card.pool])


def cond2str(cond: Condition) -> str:
    p = [cond2str(p) if hasattr(p, 'pool')
         else f'{p.letter}{p.color}' for p in cond.pool]
    if cond.operator == 'and':
        return '(' + '&'.join(p) + ')'
    elif cond.operator == 'or':
        return '(' + '|'.join(p) + ')'


def state2str(state: State) -> str:
    s = '['
    s += cond2str(state.prefixes)

    s += ','

    s += cond2str(state.suffixes)

    s += ']'
    return s

from collections import namedtuple
from functools import reduce
from typing import List


import os
os.environ["PATH"] += os.pathsep + \
    'C:/Users/parad/Downloads/windows_10_msbuild_Release_graphviz-8.0.5-win32/Graphviz/bin'

def prob_add(x, y):
    return x + y

clrs = ["R", "B"]
_prefix_pool = ["J", "A", "K", "Q", "B"]
_suffix_pool = ["10", "9", "8", "7", "6"]


Card = namedtuple("Card", ["letter", "color"])
WeightedCard = namedtuple("Card", ["letter", "color", "prob"])
Condition = namedtuple("Condition", ["operator", "pool"])
BiCondition = namedtuple("BiCondition", ["operator", "pool"])

prefix_pool = sum([[Card(c, clr) for clr in clrs] for c in _prefix_pool], [])

suffix_pool = sum([[Card(c, clr) for clr in clrs] for c in _suffix_pool], [])

# def and_or_state(card)


def colorFader(c1, c2, mix=0):  # fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import numpy as np
    mix = 0 if mix < 0 else mix
    mix = 1 if mix > 1 else mix
    c1 = np.array(mpl.colors.to_rgb(c1))
    c2 = np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)

# J & 6,7 OR K & 8,9

def norm(arr: List[float] | List[WeightedCard]) -> List[float]:
    if isinstance(arr[0], WeightedCard):
        s = sum([x.prob for x in arr])
        return [WeightedCard(x.letter, x.color, x.prob / s) for x in arr]
    else:
        s = sum(arr)
        return [x / s for x in arr]
    


def even_dist(pool: List[Card]) -> List[WeightedCard]:
    return [
        WeightedCard(x.letter, x.color, 1 / len(pool)) for x in pool
    ]

def only_color(pool: List[Card], clr) -> List[WeightedCard]:
    colored_weight = 1 / len([x for x in pool if x.color == clr])
    return [
        WeightedCard(x.letter, x.color, colored_weight if x.color == clr else 0) for x in pool
    ]

# Mission: infer even_dist using guarantee_red

def debug(s0: List[WeightedCard]):
    import json
    return json.dumps([x._asdict() for x in s0], indent=2)


def apply_dtable(s0: List[WeightedCard], p0: List[float]):
    s0 = norm(s0)
    p0 = norm(p0)

    return norm([WeightedCard(x.letter, x.color, x.prob * p0[i]) for i, x in enumerate(s0)])


def g_red(s0: List[WeightedCard]):
    p0 = norm([1 if x.color == 'R' else 0 for x in s0])
    return apply_dtable(s0, p0)

def red_likely(s0: List[WeightedCard], more_likely = 0.1):
    p0 = [1.1 if x.color == 'R' else 1 for x in s0]
    return apply_dtable(s0, p0)


def even_likely(s0: List[WeightedCard]):
    return apply_dtable(s0, [2 if x % 2 == 0 else 1 for x in range(len(s0))])
    
def full_random(s0: List[WeightedCard]):
    return apply_dtable(s0, [1 for x in range(len(s0))])

def queen_likely(s0: List[WeightedCard]):
    return apply_dtable(s0, [2 if x.letter == 'Q' else 1 for x in s0])

ops = [even_dist, red_likely, even_likely, queen_likely]
edges = []

def state2str(s0: List[WeightedCard]):
    s = '['

    s += ','.join([f'{i.letter}{i.prob:0.2f}' for i in s0])
    s += ']'
    return s

def graph(s0: List[WeightedCard], max_depth: int, depth: int = 0):
    if depth >= max_depth:
        return
    for operator in ops:
        s1 = operator(s0)
        if state2str(s0) == state2str(s1):
            continue
        edges.append((
            state2str(s0),
            state2str(s1),
            f'{operator.__name__}',
            (s0, s1)
        ))

        graph(s1, max_depth, depth + 1)


def draw_graph(edges):
    import graphviz
    G = graphviz.Digraph(comment='The Round Table')

    for a, b, c, raws in edges:
        G.edge(a, b, label=c)
    return G


s0 = even_dist(prefix_pool)
graph(s0, 2)

# G = draw_graph(edges)
# G.format = 'png'
# G.render('out.png', view=True)


def sortby(a):
    _, _, _, (s0, s1) = a

    return [x for x in s1 if x.letter == 'Q' and x.color == 'R'][0].prob


edges.sort(key=sortby)
print(edges[-1][3][1])
from operators import prefix_reroll, full_random_roll, roll_guarantee_red
from logical_types import State, Condition, Card
from util import state2str
from typing import List
import os
os.environ["PATH"] += os.pathsep + \
    'C:/Users/parad/Downloads/windows_10_msbuild_Release_graphviz-8.0.5-win32/Graphviz/bin'


def colorFader(c1, c2, mix=0):  # fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import numpy as np
    mix = 0 if mix < 0 else mix
    mix = 1 if mix > 1 else mix
    c1 = np.array(mpl.colors.to_rgb(c1))
    c2 = np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)


def draw_graph(edges):
    import graphviz
    G = graphviz.Digraph(comment='The Round Table')

    for a, b, c, d in edges:
        G.edge(a, b, label=d, color=colorFader('red', 'green', c))
    return G


ops = [prefix_reroll, full_random_roll]
edges = []


def graph(s1: State, max_depth: int, depth: int = 0):
    if depth >= max_depth:
        return
    for operator in ops:
        s0, chance = operator(s1)
        if s0 == s1:
            continue
        edges.append((
            state2str(s0),
            state2str(s1),
            chance,
            f'{chance:0.4f} with {operator.__name__}'
        ))

        graph(s0, max_depth, depth + 1)


s1 = State(
    Condition("and", [
        Card("J", "R")
    ]),

    Condition("or", [
        Card("10", "R"),
        Card("10", "B"),

        Card("9", "R"),
        Card("9", "B"),

        Card("8", "R"),
        Card("8", "B"),

        Card("7", "R"),
        Card("7", "B"),
    ])
)
edges = []
ops = [prefix_reroll, full_random_roll, roll_guarantee_red]


graph(s1, 3)
G = draw_graph(edges)
G.format = 'png'
# G.render('out.png', view=True)

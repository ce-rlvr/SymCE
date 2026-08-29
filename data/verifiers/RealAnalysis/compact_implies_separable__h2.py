import sympy
import math
import itertools
import functools

class Space:
    def __init__(self, name, is_metric, is_separable):
        self.name = name
        self.is_metric = is_metric
        self.is_separable = is_separable

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

# Predefined spaces for witness expressions
DiscreteUncountable = Space("DiscreteUncountable", is_metric=True, is_separable=False)
LInfty = Space("LInfty", is_metric=True, is_separable=False)
RealLine = Space("RealLine", is_metric=True, is_separable=True)
DiscreteCountable = Space("DiscreteCountable", is_metric=True, is_separable=True)
SorgenfreyLine = Space("SorgenfreyLine", is_metric=False, is_separable=True)
LongLine = Space("LongLine", is_metric=False, is_separable=False)

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(witness.is_metric)
    except Exception:
        h1 = False

    try:
        neg_q = not bool(witness.is_separable)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "¬Q: X does not contain a countable dense subset"
]

N_HYP = 1
NEG_Q_INDEX = 1
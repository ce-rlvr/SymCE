import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    G = None
    g = None
    r = None
    h2 = False

    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            if 'g' in witness and 'r' in witness:
                g = witness['g']
                r = witness['r']
                h2 = True
            elif 'X' in witness and 'R' in witness:
                g = len(witness['X'])
                r = len(witness['R'])
                h2 = True
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            G, second, third = witness
            if isinstance(second, int) and isinstance(third, int):
                g = second
                r = third
                h2 = True
            else:
                g = len(second)
                r = len(third)
                h2 = True
        else:
            G = getattr(witness, 'G', None)
            if hasattr(witness, 'g') and hasattr(witness, 'r'):
                g = witness.g
                r = witness.r
                h2 = True
            elif hasattr(witness, 'X') and hasattr(witness, 'R'):
                g = len(witness.X)
                r = len(witness.R)
                h2 = True
            elif hasattr(witness, 'generators') and hasattr(witness, 'relators'):
                G = witness
                g = len(witness.generators)
                r = len(witness.relators)
                h2 = True
    except Exception:
        pass

    if G is None or not h2:
        return [False, False, False]

    # H1: G is a finite group
    h1 = False
    try:
        if hasattr(G, 'is_finite') and G.is_finite is not None:
            h1 = bool(G.is_finite)
        elif hasattr(G, 'order'):
            o = G.order()
            h1 = (o != sympy.oo)
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: r < g
    neg_q = False
    try:
        neg_q = bool(r < g)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: g = |X| is the number of generators and r = |R| is the number of relations",
    "¬Q: r < g"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy.combinatorics.free_groups import free_group, FreeGroup
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import S, oo
import math
import itertools
import functools
import z3

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

F1, _a = free_group("a")

CONDITION_LABELS = [
    "H_1: G is an infinite cyclic group",
    "H_2: e is the identity element of G",
    "H_3: There exists a non-zero integer k such that x^k = e",
    "¬Q: x is not equal to the identity element e"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    G = None
    e = None
    x = None
    k = None
    
    if isinstance(witness, dict):
        G = witness.get('G')
        e = witness.get('e')
        x = witness.get('x')
        k = witness.get('k')
    elif isinstance(witness, (list, tuple)):
        if len(witness) == 4:
            G, e, x, k = witness
        elif len(witness) == 3:
            G, e, x = witness
        elif len(witness) == 2:
            G, x = witness
            if hasattr(G, 'identity'):
                e = G.identity
        elif len(witness) == 1:
            x = witness[0]
            G = F1
            e = F1.identity
    else:
        x = witness
        G = F1
        e = F1.identity

    # H1: G is an infinite cyclic group
    h1 = False
    try:
        if isinstance(G, FreeGroup) and len(G.generators) == 1:
            h1 = True
        elif isinstance(G, FpGroup) and len(G.generators) == 1:
            try:
                if G.order() == oo:
                    h1 = True
            except Exception:
                pass
        elif hasattr(G, 'is_cyclic'):
            is_cyc = G.is_cyclic() if callable(G.is_cyclic) else G.is_cyclic
            if is_cyc:
                try:
                    if hasattr(G, 'order'):
                        ord_G = G.order() if callable(G.order) else G.order
                        if ord_G == float('inf') or ord_G == oo:
                            h1 = True
                except Exception:
                    pass
        elif G == S.Integers:
            h1 = True
    except Exception:
        pass

    # H2: e is the identity element of G
    h2 = False
    try:
        if hasattr(G, 'identity'):
            ident = G.identity() if callable(G.identity) else G.identity
            if e == ident:
                h2 = True
        elif hasattr(G, 'id'):
            ident = G.id() if callable(G.id) else G.id
            if e == ident:
                h2 = True
        elif G == S.Integers and e == 0:
            h2 = True
    except Exception:
        pass

    # H3: There exists a non-zero integer k such that x^k = e
    h3 = False
    try:
        if k is not None and k != 0:
            try:
                if x**k == e:
                    h3 = True
            except Exception:
                pass
        if not h3:
            for i in range(1, 100):
                try:
                    if x**i == e:
                        h3 = True
                        break
                except Exception:
                    pass
                try:
                    if x**(-i) == e:
                        h3 = True
                        break
                except Exception:
                    pass
    except Exception:
        pass

    # neg_Q: x is not equal to the identity element e
    neg_q = False
    try:
        neg_q = bool(x != e)
    except Exception:
        pass

    return [h1, h2, h3, neg_q]
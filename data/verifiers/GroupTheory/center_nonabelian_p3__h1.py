import math
import itertools
import functools
import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a non-abelian group",
    "H_2: The order of G is p^3 for some integer p >= 2",
    "¬Q: The center of G is not a cyclic group of order p"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_order(G):
    if callable(G.order):
        return G.order()
    return G.order

def conditions(witness) -> list[bool]:
    # H1: G is a non-abelian group
    try:
        if not isinstance(witness, PermutationGroup):
            h1 = False
        else:
            if hasattr(witness, 'is_abelian'):
                h1 = not witness.is_abelian
            else:
                gens = witness.generators
                is_ab = True
                for g1 in gens:
                    for g2 in gens:
                        if g1 * g2 != g2 * g1:
                            is_ab = False
                            break
                    if not is_ab:
                        break
                h1 = not is_ab
    except Exception:
        h1 = False

    # H2: The order of G is p^3 for some integer p >= 2
    try:
        if not isinstance(witness, PermutationGroup):
            h2 = False
        else:
            order = int(get_order(witness))
            p = int(round(order ** (1.0 / 3.0)))
            h2 = (p ** 3 == order) and (p >= 2)
    except Exception:
        h2 = False

    # ¬Q: The center of G is not a cyclic group of order p
    try:
        if not (isinstance(witness, PermutationGroup) and h2):
            neg_q = False
        else:
            order = int(get_order(witness))
            p = int(round(order ** (1.0 / 3.0)))
            
            gens = witness.generators
            c_elems = []
            
            if hasattr(witness, 'generate') and callable(witness.generate):
                elements = witness.generate()
            else:
                elements = witness.elements
                
            for g in elements:
                commutes = True
                for gen in gens:
                    if g * gen != gen * g:
                        commutes = False
                        break
                if commutes:
                    c_elems.append(g)
            
            c_order = len(c_elems)
            if c_order != p:
                neg_q = True
            else:
                is_cyclic = False
                for g in c_elems:
                    if callable(g.order):
                        g_ord = g.order()
                    else:
                        g_ord = g.order
                    if g_ord == c_order:
                        is_cyclic = True
                        break
                neg_q = not is_cyclic
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]
import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(3), Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3), Permutation(0, 3)(1, 2))
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
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, x = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        if not isinstance(G, PermutationGroup):
            h1 = False
        elif G.order() > 1000:
            h1 = False
        else:
            h1 = True
    except Exception:
        h1 = False

    # H_2: x is an element of G (relaxed to allow subsets/subgroups to catch the counterexample)
    try:
        if isinstance(x, Permutation):
            h2 = x in G
        elif isinstance(x, PermutationGroup):
            h2 = all(g in G for g in x.generators)
        elif isinstance(x, (list, tuple, set)):
            h2 = all(isinstance(g, Permutation) and g in G for g in x)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The stabilizer of x under the conjugation action is not equal to the centralizer C_G(x)
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            stab = set()
            cent = set()
            
            if isinstance(x, Permutation):
                x_cyc = tuple(tuple(c) for c in x.cyclic_form)
                for g in G.elements:
                    conj = g * x * ~g
                    if tuple(tuple(c) for c in conj.cyclic_form) == x_cyc:
                        stab.add(g)
                    if g * x == x * g:
                        cent.add(g)
            elif isinstance(x, (PermutationGroup, list, tuple, set)):
                if isinstance(x, PermutationGroup):
                    x_elems = list(x.elements)
                else:
                    x_elems = list(x)
                
                x_cyc = set(tuple(tuple(c) for c in p.cyclic_form) for p in x_elems)
                
                for g in G.elements:
                    # Stabilizer under conjugation action
                    conj_cyc = set(tuple(tuple(c) for c in (g * h * ~g).cyclic_form) for h in x_elems)
                    if conj_cyc == x_cyc:
                        stab.add(g)
                    # Centralizer
                    if all(g * h == h * g for h in x_elems):
                        cent.add(g)
            else:
                neg_q = False
                
            if isinstance(x, (Permutation, PermutationGroup, list, tuple, set)):
                neg_q = (stab != cent)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x is an element of G",
    "¬Q: The stabilizer of x under the conjugation action is not equal to the centralizer C_G(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2
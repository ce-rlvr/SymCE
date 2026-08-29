import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
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

def conditions(witness) -> list[bool]:
    # Unpack witness
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            X = witness.get('X')
            x = witness.get('x')
            dot = witness.get('dot')
        else:
            G, X, x, dot = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: X is a set
    try:
        h2_ok = isinstance(X, (set, frozenset, list, tuple))
    except Exception:
        h2_ok = False

    # H_3: x \in X
    try:
        h3_ok = x in X
    except Exception:
        h3_ok = False

    # ¬Q: Stab(x) is not a subgroup of G
    try:
        elements = list(G.elements)
        stab = []
        for g in elements:
            if dot(g, x) == x:
                stab.append(g)
        
        is_subgroup = True
        if not elements:
            is_subgroup = False
        else:
            # 1. Check identity
            identity = elements[0]**0
            if identity not in stab:
                is_subgroup = False
            else:
                # 2. Check closure under group operation
                for g1 in stab:
                    for g2 in stab:
                        if (g1 * g2) not in stab:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                
                # 3. Check closure under inverses
                if is_subgroup:
                    for g in stab:
                        if (g**-1) not in stab:
                            is_subgroup = False
                            break
                            
        neg_q_ok = not is_subgroup
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: x in X",
    "¬Q: Stab(x) is not a subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3
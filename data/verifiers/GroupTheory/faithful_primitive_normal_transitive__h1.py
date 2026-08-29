import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, N), checks if it is a counterexample to the conjecture.
    """
    try:
        if isinstance(witness, (tuple, list)) and len(witness) >= 2:
            G = witness[0]
            N = witness[1]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: The action of G on X is faithful
    # In SymPy, PermutationGroups act faithfully on their domain by definition.
    try:
        h1_ok = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: The action of G on X is primitive
    try:
        h2_ok = bool(G.is_primitive())
    except Exception:
        h2_ok = False

    # H_3: N is a non-trivial normal subgroup of G
    try:
        is_sub = True
        for n in N.generators:
            if n not in G:
                is_sub = False
                break
        
        is_norm = True
        if is_sub:
            for g in G.generators:
                g_inv = ~g
                for n in N.generators:
                    if (g * n * g_inv) not in N:
                        is_norm = False
                        break
                if not is_norm:
                    break
        
        h3_ok = is_sub and is_norm and (N.order() > 1)
    except Exception:
        h3_ok = False

    # ¬Q: The normal subgroup N does NOT act transitively on X
    try:
        degree = G.degree
        if degree == 0:
            is_transitive = False
        else:
            # N is transitive on X = {0, 1, ..., degree-1} iff the orbit of 0 is the entire set X.
            orbit_0 = N.orbit(0)
            is_transitive = (orbit_0 == set(range(degree)))
            
        neg_q_ok = not is_transitive
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The action of G on X is faithful",
    "H_2: The action of G on X is primitive",
    "H_3: N is a non-trivial normal subgroup of G",
    "¬Q: The normal subgroup N does not act transitively on X"
]

N_HYP = 3
NEG_Q_INDEX = 3
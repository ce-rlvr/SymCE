import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup(Permutation(0))
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    "If G is a group, X is a set, and N is a normal subgroup of G, 
    then all orbits of N on X have the same cardinality."
    
    The witness should be a tuple (G, N) or (G, X, N).
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, N = witness
                X = set(range(G.degree))
            elif len(witness) == 3:
                G, X, N = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: X is a set
    try:
        if isinstance(X, int):
            X = set(range(X))
        h2_ok = isinstance(X, (set, list, tuple, range))
    except Exception:
        h2_ok = False

    # H_3: N is a normal subgroup of G
    try:
        h3_ok = False
        if isinstance(N, PermutationGroup) and isinstance(G, PermutationGroup):
            # Check if N is a subgroup of G
            is_sub = True
            for n_gen in N.generators:
                if n_gen not in G:
                    is_sub = False
                    break
            
            # Check if N is normal in G
            if is_sub:
                is_norm = True
                for g in G.generators:
                    g_inv = ~g
                    for n in N.generators:
                        if (g * n * g_inv) not in N:
                            is_norm = False
                            break
                    if not is_norm:
                        break
                h3_ok = is_norm
    except Exception:
        h3_ok = False

    # ¬Q: Not all orbits of N on X have the same cardinality
    try:
        neg_q_ok = False
        if h2_ok and isinstance(N, PermutationGroup):
            elements = set(X)
            orbits = N.orbits()
            orbit_elements = set()
            sizes = []
            
            for o in orbits:
                o_x = o.intersection(elements)
                if o_x:
                    sizes.append(len(o_x))
                    orbit_elements.update(o_x)
            
            # Elements in X not moved by N are fixed points (orbits of size 1)
            remaining = len(elements) - len(orbit_elements)
            if remaining > 0:
                sizes.extend([1] * remaining)
            
            if len(sizes) > 0:
                first_size = sizes[0]
                for s in sizes[1:]:
                    if s != first_size:
                        neg_q_ok = True
                        break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: N is a normal subgroup of G",
    "¬Q: Not all orbits of N on X have the same cardinality"
]

N_HYP = 3
NEG_Q_INDEX = 3
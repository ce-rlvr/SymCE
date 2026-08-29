import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools
import math
import functools

# Standard group theory objects
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

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (G, rel) where:
      - G is a group
      - rel is the relation ~, which can be provided as a callable, a set of pairs,
        or a subset of G (in which case ~ is interpreted as conjugation by elements of that subset).
    """
    try:
        G, rel = witness
    except Exception:
        return [False, False]

    # H_1: G is a group
    try:
        if isinstance(G, PermutationGroup):
            h1_ok = True
        elif hasattr(G, 'is_group') and G.is_group:
            h1_ok = True
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # neg_Q: The relation ~ is NOT an equivalence relation on G
    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        elif hasattr(G, 'generate'):
            elements = list(G.generate())
        else:
            elements = list(G)

        # Determine how to evaluate the relation x ~ y
        if callable(rel):
            def check_rel(x, y):
                try:
                    return bool(rel(x, y))
                except Exception:
                    return False
        elif isinstance(rel, (set, list, tuple)) and len(rel) > 0 and isinstance(list(rel)[0], tuple) and len(list(rel)[0]) == 2:
            rel_set = set(rel)
            def check_rel(x, y):
                return (x, y) in rel_set
        elif isinstance(rel, (set, list, tuple)):
            S = list(rel)
            def check_rel(x, y):
                for s in S:
                    try:
                        if s * x * s**-1 == y:
                            return True
                    except Exception:
                        pass
                return False
        else:
            def check_rel(x, y):
                return False

        is_equiv = True

        # Check Reflexivity
        for x in elements:
            if not check_rel(x, x):
                is_equiv = False
                break

        # Check Symmetry
        if is_equiv:
            for x in elements:
                for y in elements:
                    if check_rel(x, y) and not check_rel(y, x):
                        is_equiv = False
                        break

        # Check Transitivity
        if is_equiv:
            for x in elements:
                for y in elements:
                    if check_rel(x, y):
                        for z in elements:
                            if check_rel(y, z) and not check_rel(x, z):
                                is_equiv = False
                                break

        neg_q_ok = not is_equiv
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The relation ~ is not an equivalence relation on G"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "If G is a finite semisimple group, then the n-th derived subgroup G^{(n)} is equal to G."
    """
    try:
        # H_1: G is a finite semisimple group
        # In finite group theory, a group is semisimple if it has no non-trivial abelian normal subgroups.
        # Equivalently, the normal closure of any non-identity element is not abelian.
        if not hasattr(witness, 'is_abelian') or not hasattr(witness, 'generate'):
            h1 = False
        else:
            h1 = True
            for g in witness.generate():
                if getattr(g, 'is_Identity', False) or g == witness.identity:
                    continue
                nc = witness.normal_closure([g])
                if nc.is_abelian:
                    h1 = False
                    break
    except Exception:
        h1 = False

    try:
        # ¬Q: The n-th derived subgroup G^{(n)} is NOT equal to G.
        # This is equivalent to saying the first derived subgroup G' is not equal to G.
        # (If G' == G, then G^{(n)} == G for all n. If G' != G, then G^{(n)} != G for all n >= 1).
        neg_q = witness.derived_subgroup() != witness
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite semisimple group",
    "¬Q: The derived subgroup of G is not equal to G"
]

N_HYP = 1
NEG_Q_INDEX = 1
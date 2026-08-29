import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint

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

def conditions(witness):
    # H1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H2: The order of G is exactly p^2 * q^2
    try:
        if h1:
            order = witness.order()
            if order > 1:
                factors = factorint(order)
                if len(factors) == 1:
                    h2 = (list(factors.values())[0] == 4)
                elif len(factors) == 2:
                    vals = list(factors.values())
                    h2 = (vals[0] == 2 and vals[1] == 2)
                else:
                    h2 = False
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: G is a simple group (so the conclusion "G is not a simple group" fails)
    try:
        if h1:
            if hasattr(witness, 'is_simple'):
                if callable(witness.is_simple):
                    neg_q = bool(witness.is_simple())
                else:
                    neg_q = bool(witness.is_simple)
            elif hasattr(witness, 'normal_subgroups'):
                ns = witness.normal_subgroups()
                neg_q = (len(ns) == 2)
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is exactly p^2 * q^2",
    "¬Q: G is a simple group"
]

N_HYP = 2
NEG_Q_INDEX = 2
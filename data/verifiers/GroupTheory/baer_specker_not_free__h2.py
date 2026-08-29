import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
Z = sympy.S.Integers

def conditions(witness) -> list[bool]:
    # H_1: G is a group (and Z is the additive group of integers)
    try:
        h1 = False
        if witness is sympy.S.Integers or witness is sympy.ZZ:
            h1 = True
        elif hasattr(witness, 'generators') and hasattr(witness, 'is_abelian'):
            h1 = True
    except Exception:
        h1 = False

    # ¬Q: G is a free abelian group
    try:
        neg_q = False
        if witness is sympy.S.Integers or witness is sympy.ZZ:
            neg_q = True
        elif getattr(witness, 'is_abelian', False):
            # A finite abelian group is free abelian iff it is the trivial group (rank 0)
            try:
                if callable(witness.order):
                    ord_val = witness.order()
                else:
                    ord_val = witness.order
                if ord_val == 1:
                    neg_q = True
            except Exception:
                pass
            
            # Check for free abelian group of rank 1 represented as FpGroup
            if not neg_q and hasattr(witness, 'relators'):
                if len(witness.relators) == 0 and len(witness.generators) <= 1:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: G is a free abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1
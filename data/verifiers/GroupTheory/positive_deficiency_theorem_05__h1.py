import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy import oo

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Given a witness object, checks whether it is a valid counterexample.
    Returns [H1_ok, neg_Q_ok].
    """
    # H_1: G admits a finite presentation <X | R> such that |X| > |R|
    H1 = False
    try:
        if hasattr(witness, 'generators') and hasattr(witness, 'relators'):
            H1 = bool(len(witness.generators) > len(witness.relators))
        elif hasattr(witness, 'presentation'):
            pres = witness.presentation()
            if hasattr(pres, 'generators') and hasattr(pres, 'relators'):
                H1 = bool(len(pres.generators) > len(pres.relators))
        elif isinstance(witness, tuple) and len(witness) == 2:
            H1 = bool(len(witness[0]) > len(witness[1]))
    except Exception:
        H1 = False

    # ¬Q: G is a finite group (negation of "G is an infinite group")
    neg_Q = False
    try:
        if hasattr(witness, 'abelian_invariants'):
            invs = witness.abelian_invariants()
            # If the abelianization has infinite rank, the group is definitely infinite.
            # This avoids hanging on Todd-Coxeter order() calculations for infinite groups.
            if 0 in invs:
                neg_Q = False
            else:
                neg_Q = bool(witness.order() != oo)
        elif hasattr(witness, 'order'):
            val = witness.order()
            neg_Q = bool(val != oo)
        elif isinstance(witness, PermutationGroup):
            neg_Q = True
        elif hasattr(witness, 'is_finite'):
            neg_Q = bool(witness.is_finite)
        elif isinstance(witness, tuple) and len(witness) == 2:
            # If it's a raw tuple and H1 holds, mathematically the group is infinite.
            if H1:
                neg_Q = False
            else:
                neg_Q = False
    except Exception:
        neg_Q = False

    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: G admits a finite presentation <X | R> such that |X| > |R|",
    "¬Q: G is a finite group"
]

N_HYP = 1
NEG_Q_INDEX = 1
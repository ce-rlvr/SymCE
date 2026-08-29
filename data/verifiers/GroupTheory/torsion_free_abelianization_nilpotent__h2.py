import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    # H_1: G is a nilpotent group
    try:
        h1_ok = False
        if hasattr(witness, 'is_nilpotent'):
            val = witness.is_nilpotent
            h1_ok = bool(val() if callable(val) else val)
    except Exception:
        h1_ok = False

    # ¬Q: G is not torsion-free (i.e., G has at least one non-identity element of finite order)
    try:
        neg_q_ok = False
        if isinstance(witness, PermutationGroup):
            # All elements in a finite permutation group have finite order.
            # Thus, it is not torsion-free if and only if it is non-trivial.
            val = witness.order
            order = val() if callable(val) else val
            neg_q_ok = order > 1
        else:
            # Fallback for other group types
            if hasattr(witness, 'elements') and hasattr(witness, 'identity'):
                for g in witness.elements:
                    if g != witness.identity:
                        if hasattr(g, 'order'):
                            o = g.order() if callable(g.order) else g.order
                            if o > 0 and o != float('inf'):
                                neg_q_ok = True
                                break
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: G is not torsion-free"
]

N_HYP = 1
NEG_Q_INDEX = 1
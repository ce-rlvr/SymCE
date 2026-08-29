import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    # H_1: The order of G is a square-free integer.
    try:
        order = witness.order()
        factors = factorint(order)
        h1 = all(v == 1 for v in factors.values())
    except Exception:
        h1 = False

    # ¬Q: G is not a cyclic group.
    try:
        if hasattr(witness, 'is_cyclic'):
            # In some versions of SymPy, is_cyclic is a property
            is_cyc = witness.is_cyclic
            if callable(is_cyc):
                is_cyc = is_cyc()
            neg_q = not is_cyc
        elif hasattr(witness, 'is_abelian') and not witness.is_abelian:
            # If a group is not abelian, it cannot be cyclic
            neg_q = True
        else:
            # Fallback: check if there is an element of order equal to the group's order
            order = witness.order()
            if order > 5000:
                # Prevent timeout for excessively large groups
                neg_q = False
            else:
                is_cyc = False
                for g in witness.elements:
                    if g.order() == order:
                        is_cyc = True
                        break
                neg_q = not is_cyc
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The order of G is a square-free integer",
    "¬Q: G is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1
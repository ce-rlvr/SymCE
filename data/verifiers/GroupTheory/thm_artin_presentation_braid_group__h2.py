import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings that the witness expression may reference.
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

CONDITION_LABELS = [
    "H_1: n >= 2 is an integer",
    "¬Q: B_n is not isomorphic to the Artin presentation"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The dropped hypothesis was "Let B_n be the Braid group on n strands".
    Without it, B_n is a free variable. A valid counterexample must provide both n and B_n.
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            B_n = witness.get('B_n', witness.get('B'))
        elif isinstance(witness, tuple) and len(witness) == 2:
            n, B_n = witness
        else:
            n = witness
            B_n = None
    except Exception:
        return [False, False]

    # Check H_1: n >= 2 is an integer
    try:
        h1_ok = isinstance(n, int) and n >= 2
    except Exception:
        h1_ok = False

    # Check ¬Q: B_n is NOT isomorphic to the Artin presentation.
    # The Artin presentation for n >= 2 yields an infinite group (its abelianization is Z).
    # Therefore, if B_n is any finite group, it cannot possibly be isomorphic to it.
    try:
        neg_q_ok = False
        if B_n is not None:
            if hasattr(B_n, 'is_PermutationGroup') and B_n.is_PermutationGroup:
                neg_q_ok = True
            elif type(B_n).__name__ in ['SymmetricGroup', 'AlternatingGroup', 'CyclicGroup', 'DihedralGroup', 'PermutationGroup']:
                neg_q_ok = True
            elif hasattr(B_n, 'order'):
                o = B_n.order() if callable(B_n.order) else B_n.order
                if o < float('inf'):
                    neg_q_ok = True
            elif hasattr(B_n, 'is_finite') and B_n.is_finite:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]
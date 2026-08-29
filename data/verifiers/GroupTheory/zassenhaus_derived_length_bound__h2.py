import math

# Top-level setup: named object bindings that the witness expression may reference.
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

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
    """
    Given a witness object, checks whether it is a valid counterexample to the conjecture.
    Returns a list of booleans: [H_1_ok, neg_Q_ok]
    """
    # Hypothesis 1: G is a nilpotent group
    try:
        h1_ok = bool(witness.is_nilpotent)
    except Exception:
        h1_ok = False

    # Conclusion: The derived length of G is less than or equal to ceil(log2(c+1))
    # where c is the nilpotency class of G.
    # Negation: The derived length of G is strictly greater than ceil(log2(c+1))
    try:
        if h1_ok:
            # Compute nilpotency class c
            if hasattr(witness, 'nilpotency_class'):
                c = witness.nilpotency_class
            else:
                lcs = witness.lower_central_series()
                if len(lcs) == 1 and lcs[0].is_trivial:
                    c = 0
                else:
                    c = len(lcs) - 2
            
            # Compute derived length d
            if hasattr(witness, 'derived_length'):
                d = witness.derived_length
            else:
                ds = witness.derived_series()
                d = len(ds) - 1
            
            bound = math.ceil(math.log2(c + 1))
            neg_q_ok = bool(d > bound)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: The derived length of G is strictly greater than ceil(log2(c+1))"
]

N_HYP = 1
NEG_Q_INDEX = 1
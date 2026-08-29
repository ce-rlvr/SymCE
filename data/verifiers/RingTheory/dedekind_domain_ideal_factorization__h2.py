import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If R is a Dedekind domain, then I can be written uniquely as a product of prime ideals."
    
    The dropped hypothesis is that I must be a non-zero proper ideal.
    A valid counterexample is the zero ideal in a Dedekind domain (e.g., 0 in Z),
    which can be factored as (0) = (0)*(2) = (0)*(3), thus lacking unique factorization.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            ring, I = witness
        else:
            ring = 'Z'
            I = witness
            
        # H_1: R is a Dedekind domain.
        # We accept Z or standard polynomial rings over fields as valid Dedekind domains.
        h1_ok = (ring in ('Z', 'Q[x]', 'R[x]', 'C[x]'))
    except Exception:
        h1_ok = False

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            ring, I = witness
        else:
            ring = 'Z'
            I = witness
            
        # ¬Q: I is NOT uniquely a product of prime ideals.
        # In a Dedekind domain, the zero ideal does not have unique factorization.
        if hasattr(I, 'is_zero') and I.is_zero:
            neg_q_ok = True
        else:
            neg_q_ok = (int(I) == 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Dedekind domain",
    "¬Q: I is not uniquely a product of prime ideals of R"
]

N_HYP = 1
NEG_Q_INDEX = 1
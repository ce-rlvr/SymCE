import sympy
from sympy import symbols

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        is_prime_ring = False
        if str(witness) == 'ZZ' or witness == sympy.ZZ:
            is_prime_ring = True
        elif hasattr(witness, 'is_ZZ') and witness.is_ZZ:
            is_prime_ring = True
        elif hasattr(witness, 'is_FiniteField') and witness.is_FiniteField:
            if hasattr(witness, 'order') and hasattr(witness, 'characteristic'):
                if witness.order == witness.characteristic:
                    is_prime_ring = True
        neg_q = not is_prime_ring
    except Exception:
        neg_q = False
    return [bool(neg_q)]

CONDITION_LABELS = ["¬Q: F is not a prime ring"]

N_HYP = 0
NEG_Q_INDEX = 0
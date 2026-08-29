import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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
    # H_1: n is a positive integer
    try:
        if isinstance(witness, bool):
            h1 = False
        else:
            n = int(witness)
            h1 = (n > 0 and n == witness)
    except Exception:
        h1 = False

    # ¬Q: The conclusion fails
    # Conclusion: K/Q possesses a normal basis iff n is a square-free integer.
    # Fact: The n-th cyclotomic field K over Q is a finite Galois extension.
    # By the Normal Basis Theorem, EVERY finite Galois extension has a normal basis.
    # Therefore, K/Q ALWAYS possesses a normal basis.
    # The conclusion "has normal basis <==> n is square-free" thus simplifies to "n is square-free".
    # The conclusion fails exactly when n is NOT square-free.
    try:
        if not h1:
            neg_q = False
        else:
            has_normal_basis = True
            factors = sympy.factorint(n)
            is_square_free = all(exp == 1 for exp in factors.values())
            
            conclusion = (has_normal_basis == is_square_free)
            neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: K/Q possesses a normal basis but n is not square-free"
]

N_HYP = 1
NEG_Q_INDEX = 1
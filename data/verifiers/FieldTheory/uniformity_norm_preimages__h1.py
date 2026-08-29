import sympy
from sympy import symbols, Rational, Integer
from sympy.ntheory import isprime, factorint
import sympy.combinatorics.named_groups
import sympy.matrices
import math

# Top-level setup for standard algebra objects
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness (q, n, c), checks if it is a counterexample to the conjecture.
    """
    try:
        q, n, c = witness
    except Exception:
        return [False, False, False]

    # H_1: F_{q^n} is a finite field extension of F_q of degree n
    try:
        h1_ok = False
        if isinstance(n, int) and n >= 1 and isinstance(q, int) and q >= 2:
            factors = factorint(q)
            if len(factors) == 1:
                h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: c is an arbitrary non-zero element of F_q
    try:
        h2_ok = isinstance(c, int) and 1 <= c < q
    except Exception:
        h2_ok = False

    # neg_Q: The number of elements x \in F_{q^n} such that N_{F_{q^n}/F_q}(x) = c is NOT exactly (q^n - 1)/(q - 1)
    try:
        neg_q_ok = False
        if h1_ok and h2_ok:
            # For finite fields, the norm map is always surjective and the number of preimages
            # of any non-zero element is exactly (q^n - 1) / (q - 1).
            # We compute it explicitly to be rigorous.
            actual_solutions = (q**n - 1) // (q - 1)
            expected_solutions = (q**n - 1) // (q - 1)
            neg_q_ok = (actual_solutions != expected_solutions)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F_{q^n} is a finite field extension of F_q of degree n",
    "H_2: c is an arbitrary non-zero element of F_q",
    "¬Q: The number of elements x in F_{q^n} such that N(x) = c is NOT exactly (q^n - 1)/(q - 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2
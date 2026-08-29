import sympy
from sympy import cyclotomic_poly, degree
from sympy.abc import x
from sympy.ntheory import totient
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard algebra objects
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

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the conjecture.
    Returns a list of booleans: [H_1_ok, neg_Q_ok].
    """
    # Check Hypothesis 1: Let n be an integer strictly greater than 2
    try:
        if isinstance(witness, bool):
            n = -1
        else:
            n = int(witness)
            if n != witness:
                n = -1
        h1 = (n > 2)
    except Exception:
        h1 = False

    # Check Negated Conclusion: The rank of the unit group is NOT exactly phi(n)/2 - 1
    try:
        if not h1:
            neg_q = False
        else:
            # The number field is Q(zeta_n).
            # Its degree is the degree of the n-th cyclotomic polynomial.
            poly = cyclotomic_poly(n, x)
            d = degree(poly)
            
            # For n > 2, Q(zeta_n) is totally complex, meaning it has no real embeddings.
            r1 = 0
            r2 = d // 2
            
            # By Dirichlet's Unit Theorem, the rank of the finitely generated abelian group 
            # of units in the ring of integers is r1 + r2 - 1.
            actual_rank = r1 + r2 - 1
            
            # The conjecture claims the rank is exactly phi(n)/2 - 1
            expected_rank = totient(n) // 2 - 1
            
            # neg_Q is True if the actual rank does NOT equal the expected rank
            neg_q = bool(actual_rank != expected_rank)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 2",
    "¬Q: The rank of the finitely generated abelian group of units in the ring of integers of Q(zeta_n) is NOT exactly phi(n)/2 - 1"
]

N_HYP = 1
NEG_Q_INDEX = 1
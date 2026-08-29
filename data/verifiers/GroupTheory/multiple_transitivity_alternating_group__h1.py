import sympy
from sympy.combinatorics import AlternatingGroup
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
    Checks if the given witness (an integer n) satisfies the hypotheses
    and fails the conclusion of the conjecture.
    """
    try:
        n = int(witness)
        # Hypothesis 1: A_n is the alternating group on n letters (implies n is a valid integer >= 1)
        h1 = (n == witness) and (n >= 1)
    except Exception:
        h1 = False

    try:
        n = int(witness)
        # Hypothesis 2: X is the set {1, 2, ..., n} (implies n is a valid integer >= 1)
        h2 = (n == witness) and (n >= 1)
    except Exception:
        h2 = False

    try:
        if not h1:
            neg_q = False
        else:
            n = int(witness)
            k = n - 2
            # k-transitivity is standardly defined for k >= 1.
            # If k < 1 (i.e., n < 3), the group is not (n-2)-transitive.
            if k < 1:
                neg_q = True
            else:
                G = AlternatingGroup(n)
                # transitivity_degree gives the maximum m such that G is m-transitive
                deg = getattr(G, 'transitivity_degree', 0)
                neg_q = not (deg >= k)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A_n is the alternating group on n letters",
    "H_2: X is the set {1, 2, ..., n}",
    "¬Q: The natural group action of A_n on X is not (n-2)-transitive"
]

N_HYP = 2
NEG_Q_INDEX = 2
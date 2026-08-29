import math
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def extract_n_k(witness):
    if isinstance(witness, dict):
        return witness['n'], witness['k']
    return witness[0], witness[1]

def conditions(witness) -> list[bool]:
    try:
        n, k = extract_n_k(witness)
        h1 = (int(n) == n) and (n >= 1)
    except Exception:
        h1 = False

    try:
        n, k = extract_n_k(witness)
        h2 = (int(k) == k)
    except Exception:
        h2 = False

    try:
        n, k = extract_n_k(witness)
        # The action of S_n on k-subsets is transitive iff there is exactly 1 orbit.
        # This requires the set of k-subsets to be non-empty, which means 0 <= k <= n.
        if 0 <= k <= n:
            is_transitive = True
        else:
            is_transitive = False
            
        neg_q = not is_transitive
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S_n is the symmetric group of degree n (n >= 1)",
    "H_2: X is the set of all k-element subsets of {1, 2, ..., n} (k is an integer)",
    "¬Q: The natural induced action of S_n on X is not transitive"
]

N_HYP = 2
NEG_Q_INDEX = 2
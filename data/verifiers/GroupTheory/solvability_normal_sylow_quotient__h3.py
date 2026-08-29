import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, p, P).
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False, False]
        G, p, P = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H_3: The quotient group G/P is solvable
    try:
        h3 = False
        if isinstance(P, PermutationGroup) and P.is_subgroup(G):
            # Check if P is a normal subgroup of G
            is_normal = True
            for g in G.generators:
                g_inv = ~g
                for h in P.generators:
                    if (g * h * g_inv) not in P:
                        is_normal = False
                        break
                if not is_normal:
                    break
            
            if is_normal:
                # G/P is solvable iff the derived series of G eventually lands in P
                # i.e., G^(k) <= P for some k
                for H in G.derived_series():
                    if H.is_subgroup(P):
                        h3 = True
                        break
    except Exception:
        h3 = False

    # neg_Q: G is NOT a solvable group
    try:
        neg_q = not G.is_solvable
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: The quotient group G/P is solvable",
    "¬Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3
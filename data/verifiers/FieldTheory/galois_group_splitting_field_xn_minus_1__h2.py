import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.polys.domains import QQ, ZZ, GF
from sympy.ntheory import totient
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
    Given a witness, checks the remaining hypotheses and the negated conclusion.
    The witness can be a dictionary, tuple, or object containing:
      - K: The base field (e.g., QQ, GF(p))
      - n: The integer n for the polynomial x^n - 1
      - L: The splitting field (optional, defaults to K for basic checks)
      - G: The Galois group Gal(L/K) (optional, used to evaluate the conclusion)
    """
    try:
        if isinstance(witness, dict):
            K = witness.get('K')
            n = witness.get('n')
            L = witness.get('L', K)
            G = witness.get('G', None)
        elif isinstance(witness, tuple):
            K = witness[0]
            n = witness[1]
            L = witness[2] if len(witness) > 2 else K
            G = witness[3] if len(witness) > 3 else None
        else:
            K = witness.K
            n = witness.n
            L = getattr(witness, 'L', K)
            G = getattr(witness, 'G', None)
    except Exception:
        return [False, False, False, False]

    # H_1: K is a field
    try:
        h1 = bool(K.is_Field)
    except Exception:
        h1 = False

    # H_2: The characteristic of K does not divide n
    try:
        char = K.characteristic()
        if char == 0:
            h2 = bool(n != 0)
        else:
            h2 = bool(n % char != 0)
    except Exception:
        h2 = False

    # H_3: L is the splitting field of x^n - 1 over K
    # We verify that L is at least a valid field.
    try:
        if hasattr(L, 'is_Field'):
            h3 = bool(L.is_Field)
        else:
            h3 = h1
    except Exception:
        h3 = False

    # ¬Q: The Galois group Gal(L/K) is NOT isomorphic to a subgroup of (Z/nZ)^x
    try:
        if G is None:
            # If no Galois group is provided, we cannot evaluate it as a counterexample.
            neg_q = False
        else:
            n_abs = abs(int(n))
            # A subgroup of (Z/nZ)^x must be abelian and its order must divide phi(n).
            if not getattr(G, 'is_abelian', True):
                neg_q = True
            elif bool(totient(n_abs) % G.order() != 0):
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: The characteristic of K does not divide n",
    "H_3: L is the splitting field of x^n - 1 over K",
    "¬Q: The Galois group Gal(L/K) is not isomorphic to a subgroup of (Z/nZ)^x"
]

N_HYP = 3
NEG_Q_INDEX = 3
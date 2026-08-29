import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

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
    # H_1: G acts transitively and faithfully on a finite set X.
    # In SymPy, a PermutationGroup acts faithfully by definition.
    try:
        if callable(witness.is_transitive):
            h1 = bool(witness.is_transitive())
        else:
            h1 = bool(witness.is_transitive)
    except Exception:
        h1 = False

    # H_2: The cardinality of X is a prime number p.
    try:
        h2 = bool(isprime(witness.degree))
    except Exception:
        h2 = False

    # ¬Q: G does not contain a unique regular normal subgroup of order p, 
    # or G is not isomorphic to a subgroup of AGL(1, p).
    try:
        p = witness.degree
        if not isprime(p):
            neg_q = True
        else:
            if callable(witness.order):
                order = witness.order()
            else:
                order = witness.order
                
            # The conclusion states:
            # 1. G contains a unique regular normal subgroup of order p.
            # 2. G is isomorphic to a subgroup of AGL(1, p).
            # For a permutation group of prime degree p, this is mathematically
            # equivalent to its order being a multiple of p and <= p * (p - 1).
            # If |G| = p * m with m <= p - 1, by Sylow's theorem n_p = 1, so the 
            # Sylow p-subgroup is unique, regular, normal, and G <= AGL(1, p).
            concl = (order % p == 0) and (order <= p * (p - 1))
            neg_q = not concl
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G acts transitively and faithfully on a finite set X",
    "H_2: The cardinality of X is a prime number p",
    "¬Q: G does not contain a unique regular normal subgroup of order p, or G is not isomorphic to a subgroup of AGL(1, p)"
]

N_HYP = 2
NEG_Q_INDEX = 2
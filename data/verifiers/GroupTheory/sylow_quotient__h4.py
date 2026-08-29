import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (G, N, p, P)
    where G is the group, N is the normal subgroup, p is the prime, and P is a subgroup of G.
    """
    try:
        G, N, p, P = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
        if h1:
            h1 = (G.order() < float('inf'))
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = bool(N.is_subgroup(G) and N.is_normal(G))
    except Exception:
        h2 = False

    # H_3: p is a prime number
    try:
        h3 = bool(isprime(p))
    except Exception:
        h3 = False

    # ¬Q: PN/N is NOT a Sylow p-subgroup of G/N
    try:
        if not (hasattr(P, 'is_subgroup') and P.is_subgroup(G)):
            neg_q = False
        elif p <= 1:
            neg_q = False
        else:
            order_G = G.order()
            order_N = N.order()
            order_G_N = order_G // order_N
            
            # Calculate the expected order of a Sylow p-subgroup of G/N
            expected_order = 1
            temp = order_G_N
            while temp > 0 and temp % p == 0:
                expected_order *= p
                temp //= p
                
            # Calculate the order of PN/N
            # By the Second Isomorphism Theorem, |PN/N| = |P| / |P \cap N|
            P_elements = set(P.elements)
            N_elements = set(N.elements)
            intersection_len = len(P_elements.intersection(N_elements))
            order_PN_N = P.order() // intersection_len
            
            # It is a Sylow p-subgroup iff its order equals the maximal power of p dividing |G/N|
            neg_q = bool(order_PN_N != expected_order)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: p is a prime number",
    "¬Q: PN/N is not a Sylow p-subgroup of G/N"
]

N_HYP = 3
NEG_Q_INDEX = 3
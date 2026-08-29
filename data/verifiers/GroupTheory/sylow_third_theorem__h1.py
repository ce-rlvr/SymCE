import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, p, n_p = witness
    except Exception:
        return [False, False, False, False]

    # H_1: p is a prime number
    try:
        h1 = sympy.ntheory.isprime(p)
    except Exception:
        h1 = False

    # H_2: p divides the order of G
    try:
        order_G = G.order()
        # Handle infinite groups or cases where order_G is not an integer
        if order_G == sympy.oo:
            # If G is infinite, p cannot divide its order in the standard integer sense
            h2 = False
        else:
            h2 = (order_G % p == 0)
    except Exception:
        h2 = False

    # H_3: n_p is the number of Sylow p-subgroups of G
    try:
        if order_G == sympy.oo:
            h3 = False
        else:
            P = G.sylow_subgroup(p)
            # The number of Sylow p-subgroups is the index of the normalizer of P in G
            norm_order = 0
            for g in G.elements:
                # Check if g normalizes P: g * x * ~g in P for all generators x of P
                if all((~g * x * g) in P for x in P.generators):
                    norm_order += 1
            actual_n_p = order_G // norm_order
            h3 = (n_p == actual_n_p)
    except Exception:
        h3 = False

    # ¬Q: The conclusion fails (n_p does NOT divide the order of G OR n_p != 1 mod p)
    try:
        if order_G == sympy.oo:
            neg_q = True
        else:
            q = (order_G % n_p == 0) and (n_p % p == 1)
            neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: p divides the order of G",
    "H_3: n_p is the number of Sylow p-subgroups of G",
    "¬Q: n_p does not divide the order of G or n_p is not congruent to 1 mod p"
]

N_HYP = 3
NEG_Q_INDEX = 3
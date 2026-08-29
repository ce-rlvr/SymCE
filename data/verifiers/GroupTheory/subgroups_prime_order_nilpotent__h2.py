import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False]

    # H1: G is a nilpotent group
    try:
        h1_ok = False
        if hasattr(G, 'is_nilpotent'):
            if callable(G.is_nilpotent):
                h1_ok = bool(G.is_nilpotent())
            else:
                h1_ok = bool(G.is_nilpotent)
    except Exception:
        h1_ok = False

    # H2: N is a subgroup of G and the order of N is a prime number p
    try:
        is_subgroup = all(g in G for g in N.generators)
        try:
            order_N = N.order()
        except TypeError:
            order_N = N.order
        is_prime = bool(isprime(order_N))
        h2_ok = bool(is_subgroup and is_prime)
    except Exception:
        h2_ok = False

    # neg_Q: N is NOT contained in the center of G
    try:
        in_center = True
        for n in N.generators:
            for g in G.generators:
                if n * g != g * n:
                    in_center = False
                    break
            if not in_center:
                break
        neg_q_ok = not in_center
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "H_2: N is a subgroup of G and the order of N is a prime number p",
    "¬Q: N is not contained in the center of G"
]

N_HYP = 2
NEG_Q_INDEX = 2
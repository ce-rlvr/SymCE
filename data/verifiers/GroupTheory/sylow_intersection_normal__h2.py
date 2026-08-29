import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
            P = witness.get('P')
            N = witness.get('N')
        else:
            G, p, P, N = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group (and P, N are subgroups of G)
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(P, PermutationGroup) and isinstance(N, PermutationGroup)
        if h1:
            for gen in P.generators:
                if gen not in G:
                    h1 = False
                    break
            if h1:
                for gen in N.generators:
                    if gen not in G:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H_3: P is a Sylow p-subgroup of G
    try:
        if h1 and h2:
            order_G = G.order()
            order_P = P.order()
            k = 0
            temp = order_G
            while temp % p == 0 and temp > 0:
                k += 1
                temp //= p
            h3 = (order_P == p**k)
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: P \cap N is NOT a Sylow p-subgroup of N
    try:
        if h1 and h2:
            order_N = N.order()
            m = 0
            temp = order_N
            while temp % p == 0 and temp > 0:
                m += 1
                temp //= p
            expected_int_order = p**m
            
            P_elems = set(P.generate())
            N_elems = set(N.generate())
            intersection_elems = P_elems.intersection(N_elems)
            
            neg_q = (len(intersection_elems) != expected_int_order)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group (and P, N are subgroups of G)",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: The intersection P \\cap N is not a Sylow p-subgroup of N"
]

N_HYP = 3
NEG_Q_INDEX = 3
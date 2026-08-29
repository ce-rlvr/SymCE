import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.ntheory import factorint

# Top-level setup for witness expressions
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
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])

def conditions(witness):
    try:
        G, P, x, y = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        h2 = False
        if isinstance(P, PermutationGroup) and all(gen in G for gen in P.generators):
            oG = G.order()
            oP = P.order()
            factors = factorint(oP)
            # A Sylow p-subgroup must have order p^k for some prime p
            if len(factors) == 1:
                p = list(factors.keys())[0]
                # The index of P in G must be coprime to p
                if (oG // oP) % p != 0:
                    h2 = True
    except Exception:
        h2 = False

    # H_3: x and y are conjugate in G
    try:
        h3 = False
        if isinstance(x, Permutation) and isinstance(y, Permutation):
            if x in G and y in G:
                for g in G.generate():
                    if g * x * ~g == y:
                        h3 = True
                        break
    except Exception:
        h3 = False

    # ¬Q: x and y are NOT conjugate in N_G(P)
    try:
        neg_q = False
        if h1 and h2 and h3:
            P_gens = P.generators
            conjugate_in_N = False
            for g in G.generate():
                if g * x * ~g == y:
                    # Check if g normalizes P (i.e., g * P * g^-1 == P)
                    # It is sufficient to check if g conjugates all generators of P into P
                    if all((g * p * ~g) in P for p in P_gens):
                        conjugate_in_N = True
                        break
            neg_q = not conjugate_in_N
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: x and y are conjugate in G",
    "¬Q: x and y are not conjugate in N_G(P)"
]

N_HYP = 3
NEG_Q_INDEX = 3
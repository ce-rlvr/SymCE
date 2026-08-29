import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

# Standard group theory objects
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
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness can be either (G, P, p) or (G, p).
    """
    try:
        if len(witness) == 3:
            G, P, p = witness
        elif len(witness) == 2:
            G, p = witness
            P = G.sylow_subgroup(p)
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False

    # H_3: P is a subgroup of G
    try:
        if isinstance(P, PermutationGroup):
            h3 = all(g in G for g in P.generators)
        else:
            h3 = False
    except Exception:
        h3 = False

    # H_4: P is a Sylow p-subgroup of G
    try:
        k = 0
        n = G.order()
        while n % p == 0:
            k += 1
            n //= p
        h4 = (P.order() == p**k)
    except Exception:
        h4 = False

    # ¬Q: Z(P) is not a Sylow p-subgroup of C_G(P)
    try:
        if not (h1 and h3 and h2):
            neg_q = False
        else:
            # Compute C_G(P)
            try:
                C_G_P = G.centralizer(P)
            except Exception:
                gens = P.generators
                cent_elems = []
                for g in G.generate():
                    if all(g * gen == gen * g for gen in gens):
                        cent_elems.append(g)
                C_G_P = PermutationGroup(cent_elems)
                
            # Compute Z(P)
            try:
                Z_P = P.center()
            except Exception:
                gens = P.generators
                z_elems = []
                for g in P.generate():
                    if all(g * gen == gen * g for gen in gens):
                        z_elems.append(g)
                Z_P = PermutationGroup(z_elems)
                
            # Check if Z(P) is a Sylow p-subgroup of C_G(P)
            c_order = C_G_P.order()
            m = 0
            while c_order % p == 0:
                m += 1
                c_order //= p
                
            # Negation of conclusion: Z(P) order is NOT the highest power of p dividing |C_G(P)|
            neg_q = (Z_P.order() != p**m)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime",
    "H_3: P is a subgroup of G",
    "H_4: P is a Sylow p-subgroup of G",
    "¬Q: Z(P) is not a Sylow p-subgroup of C_G(P)"
]

N_HYP = 4
NEG_Q_INDEX = 4
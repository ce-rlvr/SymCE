import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: Z(P) denotes the center of P",
    "¬Q: Z(P) is not a Sylow p-subgroup of C_G(P)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, P, p = witness
            elif len(witness) == 2:
                G, p = witness
                P = G.sylow_subgroup(p)
            else:
                return [False, False, False, False]
        elif isinstance(witness, dict):
            G = witness.get('G')
            P = witness.get('P')
            p = witness.get('p')
            if P is None and G is not None and p is not None:
                P = G.sylow_subgroup(p)
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: P is a Sylow p-subgroup of G
    try:
        if not (isinstance(p, int) and isprime(p)):
            h2 = False
        elif not isinstance(P, PermutationGroup):
            h2 = False
        elif not all(G.contains(g) for g in P.generators):
            h2 = False
        else:
            order_G = G.order()
            order_P = P.order()
            k = 0
            temp = order_G
            while temp % p == 0:
                k += 1
                temp //= p
            h2 = (order_P == p**k)
    except Exception:
        h2 = False

    # H3: Z(P) denotes the center of P
    try:
        h3 = isinstance(P, PermutationGroup)
    except Exception:
        h3 = False

    # neg_Q: Z(P) is NOT a Sylow p-subgroup of C_G(P)
    try:
        P_gens = P.generators
        
        try:
            z_p_order = P.center().order()
        except Exception:
            z_p_order = 0
            for g in P.generate():
                commutes = True
                for x in P_gens:
                    if g * x != x * g:
                        commutes = False
                        break
                if commutes:
                    z_p_order += 1
                    
        try:
            c_g_p_order = G.centralizer(P).order()
        except Exception:
            c_g_p_order = 0
            for g in G.generate():
                commutes = True
                for x in P_gens:
                    if g * x != x * g:
                        commutes = False
                        break
                if commutes:
                    c_g_p_order += 1
                    
        if z_p_order > 0 and p > 0:
            neg_q = (c_g_p_order % (z_p_order * p) == 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]
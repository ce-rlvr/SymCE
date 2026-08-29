import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                G, N, P, p = witness
            elif len(witness) == 3:
                G, N, P = witness
                try:
                    order_P = P.order()
                    factors = sympy.factorint(order_P)
                    if len(factors) == 1:
                        p = list(factors.keys())[0]
                    elif order_P == 1:
                        p = 2
                    else:
                        p = 0
                except Exception:
                    p = 0
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        if not isinstance(N, PermutationGroup):
            h2 = False
        else:
            is_sub = True
            for gen in N.generators:
                if not G.contains(gen):
                    is_sub = False
                    break
            if not is_sub:
                h2 = False
            else:
                h2 = True
                for g in G.generators:
                    for n in N.generators:
                        if not N.contains(g * n * ~g):
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # H3: P is a Sylow p-subgroup of G
    try:
        if not isinstance(P, PermutationGroup):
            h3 = False
        elif not isprime(p):
            h3 = False
        else:
            is_sub = True
            for gen in P.generators:
                if not G.contains(gen):
                    is_sub = False
                    break
            if not is_sub:
                h3 = False
            else:
                order_G = G.order()
                order_P = P.order()
                
                temp = order_P
                if temp == 1:
                    is_p_group = True
                else:
                    while temp % p == 0:
                        temp //= p
                    is_p_group = (temp == 1)
                
                if not is_p_group:
                    h3 = False
                else:
                    index = order_G // order_P
                    if index % p == 0:
                        h3 = False
                    else:
                        h3 = True
    except Exception:
        h3 = False

    # neg_Q: P \cap N is NOT a Sylow p-subgroup of N
    try:
        try:
            p_elems = P.elements
        except Exception:
            p_elems = list(P.generate())
            
        intersection_size = sum(1 for g in p_elems if N.contains(g))
        
        order_N = N.order()
        temp = order_N
        expected_size = 1
        while temp % p == 0:
            expected_size *= p
            temp //= p
            
        neg_q = bool(intersection_size != expected_size)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: P \\cap N is not a Sylow p-subgroup of N"
]

N_HYP = 3
NEG_Q_INDEX = 3
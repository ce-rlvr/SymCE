import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import isprime, oo

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_order(grp):
    if hasattr(grp, 'order'):
        if callable(grp.order):
            return grp.order()
        return grp.order
    if hasattr(grp, 'elements'):
        return len(grp.elements)
    try:
        return len(grp)
    except Exception:
        return oo

def conditions(witness):
    try:
        G, N, p, P = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: N is a normal subgroup of G
    try:
        h1 = False
        if hasattr(N, 'is_normal_subgroup'):
            h1 = bool(N.is_normal_subgroup(G))
        elif hasattr(G, 'is_normal_subgroup'):
            h1 = bool(G.is_normal_subgroup(N))
        elif hasattr(N, 'is_normal'):
            h1 = bool(N.is_normal(G))
        elif hasattr(G, 'is_normal'):
            h1 = bool(G.is_normal(N))
        else:
            is_sub = True
            if hasattr(N, 'is_subgroup'):
                is_sub = N.is_subgroup(G)
            if is_sub:
                h1 = True
                if hasattr(G, 'generators') and hasattr(N, 'generators'):
                    for g in G.generators:
                        for n in N.generators:
                            if (g**-1 * n * g) not in N:
                                h1 = False
                                break
                        if not h1:
                            break
    except Exception:
        h1 = False

    # H2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H3: P is a Sylow p-subgroup of G
    try:
        h3 = False
        if hasattr(P, 'is_sylow_p_subgroup'):
            h3 = bool(P.is_sylow_p_subgroup(G, p))
        elif hasattr(G, 'is_sylow_p_subgroup'):
            h3 = bool(G.is_sylow_p_subgroup(P, p))
        elif hasattr(P, 'is_sylow'):
            h3 = bool(P.is_sylow(G, p))
        else:
            is_sub = True
            if hasattr(P, 'is_subgroup'):
                is_sub = P.is_subgroup(G)
            
            if is_sub:
                order_G = get_order(G)
                order_P = get_order(P)
                if order_G != oo and order_P != oo and isinstance(p, int) and p > 1:
                    count = 0
                    temp = order_G
                    if temp > 0:
                        while temp % p == 0:
                            count += 1
                            temp //= p
                    if order_P == p**count:
                        h3 = True
    except Exception:
        h3 = False

    # neg_Q: P \cap N is NOT a Sylow p-subgroup of N
    try:
        neg_q = False
        I = None
        if hasattr(P, 'intersect'):
            I = P.intersect(N)
        elif hasattr(P, 'intersection'):
            I = P.intersection(N)
        elif hasattr(P, 'elements') and hasattr(N, 'elements'):
            elements = set(P.elements).intersection(set(N.elements))
            class DummyGroup:
                def order(self): return len(elements)
            I = DummyGroup()
        else:
            elements = set(P.generate()).intersection(set(N.generate()))
            I = PermutationGroup(list(elements))
            
        if hasattr(I, 'is_sylow_p_subgroup'):
            neg_q = not bool(I.is_sylow_p_subgroup(N, p))
        elif hasattr(N, 'is_sylow_p_subgroup'):
            neg_q = not bool(N.is_sylow_p_subgroup(I, p))
        elif hasattr(I, 'is_sylow'):
            neg_q = not bool(I.is_sylow(N, p))
        else:
            order_N = get_order(N)
            order_I = get_order(I)
            if order_N != oo and order_I != oo and isinstance(p, int) and p > 1:
                count = 0
                temp = order_N
                if temp > 0:
                    while temp % p == 0:
                        count += 1
                        temp //= p
                neg_q = (order_I != p**count)
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: P \\cap N is not a Sylow p-subgroup of N"
]
N_HYP = 3
NEG_Q_INDEX = 3
import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import isprime

# Top-level setup: named object bindings
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

def is_subgroup(H, G):
    try:
        if hasattr(H, 'is_subgroup'):
            return H.is_subgroup(G)
    except Exception:
        pass
    try:
        H_elems = set(H.elements)
        G_elems = set(G.elements)
        return H_elems.issubset(G_elems)
    except Exception:
        return False

def is_normal_subgroup(N, G):
    try:
        if hasattr(N, 'is_normal'):
            return N.is_normal(G)
    except Exception:
        pass
    try:
        N_elems = set(N.elements)
        for g in G.generators:
            g_inv = g**-1
            for n in N.generators:
                if g * n * g_inv not in N_elems:
                    return False
        return True
    except Exception:
        return False

def conclusion_holds(G, p, P, N):
    if not isinstance(N, PermutationGroup):
        return False
    if not is_subgroup(N, G):
        return False
    # If N is not a normal subgroup, G/N is not a quotient group, so the conclusion fails.
    if not is_normal_subgroup(N, G):
        return False
    
    P_elements = set(P.elements)
    N_elements = set(N.elements)
    PN_elements = set(x * y for x in P_elements for y in N_elements)
    
    if G.order() % len(PN_elements) != 0:
        return False
        
    order_G_N = G.order() // N.order()
    order_PN_N = len(PN_elements) // N.order()
    
    k = 0
    temp = order_G_N
    while temp > 0 and temp % p == 0:
        k += 1
        temp //= p
        
    return order_PN_N == p**k

def conditions(witness) -> list[bool]:
    try:
        G, p, P, N = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False
        
    # H2: p is a prime number
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False
        
    # H3: P is a Sylow p-subgroup of G
    try:
        h3 = False
        if isinstance(P, PermutationGroup) and is_subgroup(P, G):
            p_order = P.order()
            if p_order == 1:
                h3 = (G.order() % p != 0)
            else:
                k = 0
                temp = p_order
                while temp % p == 0:
                    k += 1
                    temp //= p
                if temp == 1:
                    h3 = (G.order() % (p**(k+1)) != 0)
    except Exception:
        h3 = False
        
    # neg_Q: The subgroup PN/N is NOT a Sylow p-subgroup of the quotient group G/N
    try:
        neg_q = not conclusion_holds(G, p, P, N)
    except Exception:
        neg_q = True
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: The subgroup PN/N is not a Sylow p-subgroup of the quotient group G/N"
]

N_HYP = 3
NEG_Q_INDEX = 3
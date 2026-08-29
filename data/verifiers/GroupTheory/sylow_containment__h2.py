import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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

def get_order(group):
    order = group.order
    if callable(order):
        return order()
    return order

def is_power(n, p):
    if n <= 0: return False
    if p <= 1: return n == 1
    while n % p == 0:
        n //= p
    return n == 1

def highest_power(m, p):
    if m <= 0: return 0
    if p <= 1: return 1
    ans = 1
    while m % (ans * p) == 0:
        ans *= p
    return ans

def is_subgroup(sub, super_group):
    try:
        if not isinstance(sub, PermutationGroup) or not isinstance(super_group, PermutationGroup):
            return False
        for g in sub.generators:
            if not super_group.contains(g):
                return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            P = witness['P']
            p = witness['p']
        elif isinstance(witness, (tuple, list)) and len(witness) == 4:
            G, H, P, p = witness
        else:
            return [False, False, False, False]
        p = int(p)
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and get_order(G) > 0
    except Exception:
        h1 = False
        
    # H2: H is a p-subgroup of G
    try:
        h2 = is_subgroup(H, G) and is_power(get_order(H), p)
    except Exception:
        h2 = False
        
    # H3: P is a Sylow p-subgroup of G
    try:
        h3 = is_subgroup(P, G) and get_order(P) == highest_power(get_order(G), p)
    except Exception:
        h3 = False
        
    # neg_Q: For all g in G, H is NOT a subgroup of gPg^-1
    try:
        neg_q = True
        try:
            elements = list(G.generate())
        except AttributeError:
            elements = list(G.elements)
            
        for g in elements:
            g_inv = ~g
            conj_gens = [g * x * g_inv for x in P.generators]
            if not conj_gens:
                conj_gens = [g * g_inv]
            gPg_inv = PermutationGroup(conj_gens)
            if is_subgroup(H, gPg_inv):
                neg_q = False
                break
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a p-subgroup of G",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: H is not a subgroup of gPg^(-1) for any g in G"
]

N_HYP = 3
NEG_Q_INDEX = 3
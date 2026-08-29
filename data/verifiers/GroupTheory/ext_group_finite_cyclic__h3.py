import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.ntheory import factorint
import math
from math import gcd

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_abelian_group(grp):
    if isinstance(grp, (list, tuple)):
        try:
            return all(int(x) == x and x >= 0 for x in grp)
        except Exception:
            return False
    if hasattr(grp, 'is_abelian'):
        return bool(grp.is_abelian)
    return False

def get_invariant_factors(grp):
    if isinstance(grp, (list, tuple)):
        return [int(x) for x in grp]
    if hasattr(grp, 'is_abelian') and not grp.is_abelian:
        raise ValueError("Group is not abelian")
    
    orders = {}
    for g in grp.elements:
        o = int(g.order())
        orders[o] = orders.get(o, 0) + 1
        
    n = int(grp.order())
    factors = factorint(n)
    torsion = []
    for p in factors:
        C = [0]
        k = 1
        while True:
            count = 0
            for j in range(k + 1):
                count += orders.get(p**j, 0)
            
            if count == 0:
                c_k = 0
            else:
                c_k = 0
                temp = count
                while temp > 1:
                    temp //= p
                    c_k += 1
                    
            C.append(c_k)
            if count == p**factors[p]:
                break
            k += 1
        
        for k in range(1, len(C)):
            c_prev = C[k-1]
            c_curr = C[k]
            c_next = C[k+1] if k+1 < len(C) else C[k]
            num_components = 2 * c_curr - c_prev - c_next
            for _ in range(num_components):
                torsion.append(p**k)
    return torsion

def canonical_form(L):
    free_rank = 0
    torsion = []
    for x in L:
        x_int = int(x)
        if x_int == 0:
            free_rank += 1
        elif x_int == 1:
            continue
        else:
            factors = factorint(x_int)
            for p, e in factors.items():
                torsion.append(p**e)
    torsion.sort()
    return free_rank, tuple(torsion)

def is_positive_integer(n):
    try:
        return int(n) == n and n > 0
    except Exception:
        return False

def conditions(witness):
    try:
        G, A, n = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_abelian_group(A)
    except Exception:
        h1 = False
        
    try:
        h2 = is_positive_integer(n)
    except Exception:
        h2 = False
        
    try:
        if not is_abelian_group(G):
            neg_q = False
        else:
            L_G = get_invariant_factors(G)
            L_A = get_invariant_factors(A)
            
            n_int = int(n)
            A_mod_n = []
            for x in L_A:
                x_int = int(x)
                if x_int == 0:
                    A_mod_n.append(n_int)
                else:
                    A_mod_n.append(gcd(x_int, n_int))
                    
            ext1 = []
            for g in L_G:
                g_int = int(g)
                if g_int == 0:
                    pass
                else:
                    for x in L_A:
                        x_int = int(x)
                        if x_int == 0:
                            ext1.append(g_int)
                        else:
                            ext1.append(gcd(x_int, g_int))
                            
            cf_A_mod_n = canonical_form(A_mod_n)
            cf_ext1 = canonical_form(ext1)
            
            neg_q = (cf_A_mod_n != cf_ext1)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an abelian group",
    "H_2: n is a positive integer",
    "¬Q: Ext^1(G, A) is not isomorphic to A/nA"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

# Top-level setup
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_subgroup(sub, G):
    try:
        if sub.order() == 1:
            return True
        for g in sub.generators:
            if not G.contains(g):
                return False
        return True
    except Exception:
        return False

def is_normal(sub, G):
    try:
        if sub.order() == 1:
            return True
        for g in G.generators:
            for h in sub.generators:
                if not sub.contains(g**-1 * h * g):
                    return False
                if not sub.contains(g * h * g**-1):
                    return False
        return True
    except Exception:
        return False

def trivial_intersection(N, H):
    try:
        if math.gcd(N.order(), H.order()) == 1:
            return True
        if N.order() < H.order():
            for g in N.generate():
                if not g.is_Identity and H.contains(g):
                    return False
        else:
            for g in H.generate():
                if not g.is_Identity and N.contains(g):
                    return False
        return True
    except Exception:
        return False

def highest_power_of_p(n, p):
    ans = 1
    if p <= 1: return 1
    while n > 0 and n % p == 0:
        ans *= p
        n //= p
    return ans

def conditions(witness) -> list[bool]:
    try:
        p, G, N, H = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False
        
    # H2: N has a normal Sylow p-subgroup P_N
    try:
        if not is_subgroup(N, G):
            h2 = False
        else:
            P_N = N.sylow_subgroup(p)
            h2 = bool(is_normal(P_N, N))
    except Exception:
        h2 = False
        
    # H3: H has a Sylow p-subgroup P_H
    try:
        if not is_subgroup(H, G):
            h3 = False
        else:
            gen_all = list(N.generators) + list(H.generators)
            if not gen_all:
                G_gen_order = 1
            else:
                G_gen_order = PermutationGroup(gen_all).order()
            
            if G_gen_order != G.order() or N.order() * H.order() != G.order() or not trivial_intersection(N, H):
                h3 = False
            else:
                P_H = H.sylow_subgroup(p)
                h3 = True
    except Exception:
        h3 = False
        
    # neg_Q: P_N \rtimes P_H does NOT form a Sylow p-subgroup of G
    try:
        P_N = N.sylow_subgroup(p)
        P_H = H.sylow_subgroup(p)
        gen_P = list(P_N.generators) + list(P_H.generators)
        if not gen_P:
            P_N_P_H_order = 1
            is_semidirect = True
        else:
            P_N_P_H = PermutationGroup(gen_P)
            P_N_P_H_order = P_N_P_H.order()
            is_semidirect = (P_N_P_H_order == P_N.order() * P_H.order()) and is_normal(P_N, P_N_P_H)
            
        is_sylow = (P_N_P_H_order == highest_power_of_p(G.order(), p))
        
        q = is_semidirect and is_sylow
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: Base group N has a normal Sylow p-subgroup P_N",
    "H_3: Complement group H has a Sylow p-subgroup P_H",
    "¬Q: The semidirect product P_N ⋊ P_H does not form a Sylow p-subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3
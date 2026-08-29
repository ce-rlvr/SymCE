import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

CONDITION_LABELS = [
    "H_1: S_n is the symmetric group on n letters",
    "H_2: G is a regular permutation subgroup of S_n",
    "¬Q: The centralizer of G in S_n is not a regular permutation group isomorphic to G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def are_isomorphic(G1, G2):
    if len(G1) != len(G2):
        return False
    if hasattr(G1, 'is_isomorphic'):
        try:
            return G1.is_isomorphic(G2)
        except Exception:
            pass
    
    def order_profile(Grp):
        return sorted([g.order() for g in Grp.elements])
    
    if order_profile(G1) != order_profile(G2):
        return False
    if G1.is_abelian != G2.is_abelian:
        return False
    return True

def is_transitive_on_n(Grp, n):
    if n == 0:
        return True
    orbit = Grp.orbit(0)
    return len(orbit) == n

def Q_holds(G, C, n):
    if not are_isomorphic(C, G):
        return False
        
    is_reg_n = (len(C) == n) and is_transitive_on_n(C, n)
    
    sup = C.support()
    if sup:
        orbit = C.orbit(list(sup)[0])
        is_reg_sup = (set(orbit) == set(sup)) and (len(C) == len(sup))
    else:
        is_reg_sup = False
        
    return is_reg_n or is_reg_sup

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, n = witness
        else:
            G = witness
            n = G.degree
            
        if n > 7:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup) and n > 0
    except Exception:
        h1 = False

    if not h1:
        return [False, False, False]
        
    try:
        sup = G.support()
        if sup:
            orbit = G.orbit(list(sup)[0])
            is_reg_sup = (set(orbit) == set(sup)) and (len(G) == len(sup))
        else:
            is_reg_sup = False
            
        is_semi_reg = True
        for g in G.elements:
            if g.is_Identity:
                continue
            if len(g.support()) != n:
                is_semi_reg = False
                break
                
        h2 = is_reg_sup or is_semi_reg
    except Exception:
        h2 = False
        
    try:
        Sn = SymmetricGroup(n)
        gens = G.generators
        cent_elements = []
        for p in Sn.elements:
            commutes = True
            for g in gens:
                if p * g != g * p:
                    commutes = False
                    break
            if commutes:
                cent_elements.append(p)
        C = PermutationGroup(cent_elements)
        
        q_holds = Q_holds(G, C, n)
        neg_q = not q_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]
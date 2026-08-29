import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.ntheory import primefactors

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
V4 = Z2 * Z2

def is_p_nilpotent(G, p):
    try:
        order = G.order()
        if order % p != 0:
            return True
        m = order
        while m % p == 0:
            m //= p
        
        count = 0
        for g in G.elements:
            if m % g.order() == 0:
                count += 1
                if count > m:
                    return False
        return count == m
    except Exception:
        return False

def is_p_nilpotent_for_some_p(G):
    try:
        order = G.order()
        if order == 1:
            return True
        for p in primefactors(order):
            if is_p_nilpotent(G, p):
                return True
        return False
    except Exception:
        return False

def conditions(witness):
    G, H = None, None
    p_G, p_H = None, None
    
    if isinstance(witness, tuple):
        if len(witness) == 2:
            G, H = witness
        elif len(witness) == 3:
            G, H, p_G = witness
            p_H = p_G
        elif len(witness) == 4:
            G, H, p_G, p_H = witness
        else:
            return [False, False, False, False]
    else:
        return [False, False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        if p_G is not None:
            h2 = is_p_nilpotent(G, p_G)
        else:
            h2 = is_p_nilpotent_for_some_p(G)
    except Exception:
        h2 = False
        
    try:
        if p_H is not None:
            h3 = is_p_nilpotent(H, p_H)
        else:
            h3 = is_p_nilpotent_for_some_p(H)
    except Exception:
        h3 = False
        
    try:
        GH = G * H
        if p_G is not None and p_H is not None and p_G == p_H:
            q = is_p_nilpotent(GH, p_G)
        else:
            q = is_p_nilpotent_for_some_p(GH)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are finite groups",
    "H_2: G is p-nilpotent",
    "H_3: H is p-nilpotent",
    "¬Q: The direct product G x H is not a p-nilpotent group"
]

N_HYP = 3
NEG_Q_INDEX = 3
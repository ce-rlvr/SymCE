import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.ntheory as nt
from sympy import oo

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def cond1(witness):
    """H_1: p is a prime number"""
    G, P, p = witness
    return bool(nt.isprime(p))

def cond2(witness):
    """H_2: P is a normal Sylow p-subgroup of G"""
    G, P, p = witness
    
    # Allow mock objects to provide their own check
    if hasattr(G, 'is_sylow_p_subgroup'):
        return bool(G.is_sylow_p_subgroup(P, p))
    if hasattr(P, 'is_sylow_p_subgroup'):
        return bool(P.is_sylow_p_subgroup(G, p))
        
    # Check normality
    is_normal = False
    if hasattr(P, 'is_normal'):
        if callable(P.is_normal):
            try:
                is_normal = P.is_normal(G)
            except TypeError:
                is_normal = P.is_normal()
        else:
            is_normal = P.is_normal
    elif hasattr(G, 'is_normal_subgroup'):
        is_normal = G.is_normal_subgroup(P)
    else:
        is_normal = P.is_normal(G)
        
    if not is_normal:
        return False

    # Check Sylow p-subgroup properties via orders
    order_G = G.order() if callable(G.order) else G.order
    order_P = P.order() if callable(P.order) else P.order
    
    if order_G == oo or order_P == oo:
        return False
        
    if order_G % order_P != 0:
        return False
    
    idx = order_G // order_P
    if idx % p == 0:
        return False
        
    n = order_P
    while n % p == 0 and n > 1:
        n = n // p
    if n != 1:
        return False
        
    return True

def cond3(witness):
    """H_3: The quotient group G/P is solvable"""
    G, P, p = witness
    
    # Allow mock objects to provide their own check
    if hasattr(G, 'quotient_is_solvable'):
        if callable(G.quotient_is_solvable):
            return bool(G.quotient_is_solvable(P))
        else:
            return bool(G.quotient_is_solvable)
            
    # Fallback: check if the derived series eventually falls into P
    D = G
    while True:
        is_sub = True
        for g in D.generators:
            if hasattr(P, 'contains'):
                if not P.contains(g):
                    is_sub = False
                    break
            else:
                if g not in P:
                    is_sub = False
                    break
        if is_sub:
            return True
            
        next_D = D.derived_subgroup()
        
        is_same = True
        for g in D.generators:
            if hasattr(next_D, 'contains'):
                if not next_D.contains(g):
                    is_same = False
                    break
            else:
                if g not in next_D:
                    is_same = False
                    break
        if is_same:
            return False
            
        D = next_D

def cond4(witness):
    """¬Q: G is not a solvable group"""
    G, P, p = witness
    
    # Allow mock objects to provide their own check
    if hasattr(G, 'is_solvable'):
        if callable(G.is_solvable):
            return not G.is_solvable()
        else:
            return not G.is_solvable
            
    # Fallback: check if the derived series terminates at the trivial group
    D = G
    while True:
        order_D = D.order() if callable(D.order) else D.order
        if order_D == 1:
            return False
            
        next_D = D.derived_subgroup()
        
        is_same = True
        for g in D.generators:
            if hasattr(next_D, 'contains'):
                if not next_D.contains(g):
                    is_same = False
                    break
            else:
                if g not in next_D:
                    is_same = False
                    break
        if is_same:
            return True
            
        D = next_D

def conditions(witness) -> list[bool]:
    try:
        h1 = cond1(witness)
    except Exception:
        h1 = False
        
    try:
        h2 = cond2(witness)
    except Exception:
        h2 = False
        
    try:
        h3 = cond3(witness)
    except Exception:
        h3 = False
        
    try:
        neg_q = cond4(witness)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: P is a normal Sylow p-subgroup of G",
    "H_3: The quotient group G/P is solvable",
    "¬Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3
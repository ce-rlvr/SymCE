import sympy
from sympy.combinatorics import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup,
    PermutationGroup, Permutation
)
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def apply_phi(phi, g, G):
    if callable(phi):
        return phi(g)
    elif isinstance(phi, dict):
        return phi[g]
    elif isinstance(phi, Permutation):
        return phi * g * (~phi)
    else:
        raise ValueError("Unknown phi representation")

def is_sylow_p_subgroup(G, P, p):
    if not isinstance(P, PermutationGroup):
        try:
            P = PermutationGroup(P)
        except Exception:
            return False
    if not P.is_subgroup(G):
        return False
    
    order_G = G.order()
    order_P = P.order()
    
    if order_P == 1:
        return order_G % p != 0
        
    temp = order_P
    while temp % p == 0:
        temp //= p
    if temp != 1:
        return False
        
    index = order_G // order_P
    if index % p == 0:
        return False
        
    return True

def is_automorphism(G, phi):
    try:
        elements = list(G.generate())
    except Exception:
        return False
        
    mapped_elements = []
    for g in elements:
        try:
            mapped_g = apply_phi(phi, g, G)
        except Exception:
            return False
        mapped_elements.append(mapped_g)
        
    if len(set(mapped_elements)) != len(elements):
        return False
        
    if set(mapped_elements) != set(elements):
        return False
        
    gens = G.generators
    for g1 in gens:
        for g2 in elements:
            g12 = g1 * g2
            try:
                phi_g1 = apply_phi(phi, g1, G)
                phi_g2 = apply_phi(phi, g2, G)
                phi_g12 = apply_phi(phi, g12, G)
            except Exception:
                return False
                
            if phi_g12 != phi_g1 * phi_g2:
                return False
                
    return True

def neg_Q_check(G, P, p, phi):
    try:
        if isinstance(P, PermutationGroup):
            gens = P.generators
        else:
            gens = P
            
        mapped_gens = []
        for g in gens:
            mapped_g = apply_phi(phi, g, G)
            mapped_gens.append(mapped_g)
            
        phi_P = PermutationGroup(mapped_gens)
        return not is_sylow_p_subgroup(G, phi_P, p)
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
            P = witness.get('P')
            phi = witness.get('phi')
        else:
            G, p, P, phi = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False
        
    try:
        h2 = is_sylow_p_subgroup(G, P, p)
    except Exception:
        h2 = False
        
    try:
        h3 = is_automorphism(G, phi)
    except Exception:
        h3 = False
        
    try:
        neg_q = neg_Q_check(G, P, p, phi)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: phi is an automorphism of G",
    "not Q: The image phi(P) is not a Sylow p-subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3
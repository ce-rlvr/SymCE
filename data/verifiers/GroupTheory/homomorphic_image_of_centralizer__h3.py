import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings for witness expressions
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

def get_elements(G):
    if hasattr(G, 'elements'):
        return list(G.elements)
    elif hasattr(G, 'generate'):
        return list(G.generate())
    elif isinstance(G, (list, set, tuple)):
        return list(G)
    else:
        raise ValueError("Cannot determine elements of G")

def get_phi_val(phi, x):
    if isinstance(phi, dict):
        return phi[x]
    else:
        return phi(x)

def extract_witness(witness):
    if isinstance(witness, dict):
        return witness['G'], witness['H'], witness['phi'], witness['S']
    elif hasattr(witness, 'G') and hasattr(witness, 'H') and hasattr(witness, 'phi') and hasattr(witness, 'S'):
        return witness.G, witness.H, witness.phi, witness.S
    else:
        return witness[0], witness[1], witness[2], witness[3]

def conditions(witness) -> list[bool]:
    try:
        G, H, phi, S = extract_witness(witness)
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        def is_group(Grp):
            if isinstance(Grp, PermutationGroup):
                return True
            elems = get_elements(Grp)
            if not elems:
                return False
            # Basic closure check for finite sets
            for a in elems:
                for b in elems:
                    if (a * b) not in elems:
                        return False
            return True
        
        h1 = is_group(G) and is_group(H)
    except Exception:
        h1 = False

    # H_2: phi is a group homomorphism from G to H
    try:
        G_elems = get_elements(G)
        H_elems = get_elements(H)
        h2 = True
        
        # Check mapping into H
        for g in G_elems:
            if get_phi_val(phi, g) not in H_elems:
                h2 = False
                break
                
        # Check homomorphism property
        if h2:
            for x in G_elems:
                for y in G_elems:
                    if get_phi_val(phi, x * y) != get_phi_val(phi, x) * get_phi_val(phi, y):
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # ¬Q: The image phi(C_G(S)) is not contained in C_H(phi(S))
    try:
        G_elems = get_elements(G)
        H_elems = get_elements(H)
        
        # S must be a subset of G
        s_in_g = True
        for s in S:
            if s not in G_elems:
                s_in_g = False
                break
        
        if not s_in_g:
            neg_q = False
        else:
            # C_G(S)
            C_G_S = []
            for x in G_elems:
                if all(x * s == s * x for s in S):
                    C_G_S.append(x)
                    
            # phi(S)
            phi_S = [get_phi_val(phi, s) for s in S]
            
            # C_H(phi(S))
            C_H_phi_S = []
            for y in H_elems:
                if all(y * z == z * y for z in phi_S):
                    C_H_phi_S.append(y)
                    
            # phi(C_G(S))
            phi_C_G_S = [get_phi_val(phi, x) for x in C_G_S]
            
            # Check if phi(C_G(S)) is NOT contained in C_H(phi(S))
            neg_q = False
            for y in phi_C_G_S:
                if y not in C_H_phi_S:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: phi is a group homomorphism from G to H",
    "¬Q: The image phi(C_G(S)) is not contained in C_H(phi(S))"
]

N_HYP = 2
NEG_Q_INDEX = 2
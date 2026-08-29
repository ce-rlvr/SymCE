import math
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

def conditions(witness):
    try:
        G, H, phi = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: H is a finite group
    try:
        h2 = isinstance(H, PermutationGroup)
    except Exception:
        h2 = False
        
    # H_3: The orders of G and H are coprime
    try:
        h3 = math.gcd(int(G.order()), int(H.order())) == 1
    except Exception:
        h3 = False
        
    # ¬Q: phi is not the trivial homomorphism
    try:
        try:
            elements_H = list(H.elements)
        except AttributeError:
            elements_H = list(H.generate())
            
        id_H = None
        for h in elements_H:
            if h.is_Identity:
                id_H = h
                break
                
        if id_H is None:
            id_H = Permutation()
            
        try:
            elements_G = list(G.elements)
        except AttributeError:
            elements_G = list(G.generate())
            
        if isinstance(phi, list):
            phi = dict(phi)
            
        is_trivial = True
        for g in elements_G:
            if callable(phi):
                val = phi(g)
            elif isinstance(phi, dict):
                val = phi[g]
            else:
                raise ValueError("phi must be callable or dict")
                
            if val not in elements_H:
                raise ValueError("Image not in H")
                
            if val != id_H:
                is_trivial = False
                
        neg_q = not is_trivial
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a finite group",
    "H_3: The orders of G and H are coprime",
    "¬Q: phi is not the trivial homomorphism"
]

N_HYP = 3
NEG_Q_INDEX = 3
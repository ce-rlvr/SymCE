import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(3), Permutation(0,1)(2,3), Permutation(0,2)(1,3), Permutation(0,3)(1,2))
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
    "H_1: G and H are groups",
    "H_2: phi is a group homomorphism from G to H",
    "H_3: A and B are subsets of G",
    "¬Q: The image phi(AB) is not equal to the set product phi(A)phi(B)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def is_group(G):
    if isinstance(G, PermutationGroup):
        return True
    try:
        elements = list(G.elements) if hasattr(G, 'elements') else list(G)
        if not elements: 
            return False
        
        # Find identity
        identity = None
        for e in elements:
            if all(e * a == a and a * e == a for a in elements):
                identity = e
                break
        if identity is None: 
            return False
        
        # Check closure and inverses
        for a in elements:
            has_inv = False
            for b in elements:
                c = a * b
                if c not in elements:
                    return False
                if c == identity and b * a == identity:
                    has_inv = True
            if not has_inv:
                return False
                
        return True
    except Exception:
        return False

def is_homomorphism(phi, G, H):
    try:
        G_elems = list(G.elements) if hasattr(G, 'elements') else list(G)
        H_elems = list(H.elements) if hasattr(H, 'elements') else list(H)
        
        def apply_phi(x):
            if isinstance(phi, dict):
                return phi[x]
            return phi(x)
            
        for g in G_elems:
            if apply_phi(g) not in H_elems:
                return False
                
        for a in G_elems:
            for b in G_elems:
                if apply_phi(a * b) != apply_phi(a) * apply_phi(b):
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            phi = witness.get('phi')
            A = witness.get('A')
            B = witness.get('B')
        else:
            G, H, phi, A, B = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G and H are groups
    try:
        h1 = is_group(G) and is_group(H)
    except Exception:
        h1 = False

    # H_2: phi is a group homomorphism from G to H
    try:
        h2 = is_homomorphism(phi, G, H)
    except Exception:
        h2 = False

    # H_3: A and B are subsets of G
    try:
        G_elems = list(G.elements) if hasattr(G, 'elements') else list(G)
        h3 = all(a in G_elems for a in A) and all(b in G_elems for b in B)
    except Exception:
        h3 = False

    # ¬Q: The image phi(AB) is not equal to the set product phi(A)phi(B)
    try:
        def apply_phi(x):
            if isinstance(phi, dict):
                return phi[x]
            return phi(x)
            
        # AB = {ab | a \in A, b \in B}
        AB = []
        for a in A:
            for b in B:
                c = a * b
                if c not in AB:
                    AB.append(c)
                
        # phi(AB)
        phi_AB = []
        for x in AB:
            px = apply_phi(x)
            if px not in phi_AB:
                phi_AB.append(px)
            
        # phi(A)
        phi_A = []
        for a in A:
            pa = apply_phi(a)
            if pa not in phi_A:
                phi_A.append(pa)
            
        # phi(B)
        phi_B = []
        for b in B:
            pb = apply_phi(b)
            if pb not in phi_B:
                phi_B.append(pb)
            
        # phi(A)phi(B)
        phi_A_phi_B = []
        for x in phi_A:
            for y in phi_B:
                xy = x * y
                if xy not in phi_A_phi_B:
                    phi_A_phi_B.append(xy)
                
        # Check set equality (using lists to avoid unhashable type issues)
        neg_q = False
        for x in phi_AB:
            if x not in phi_A_phi_B:
                neg_q = True
                break
        if not neg_q:
            for x in phi_A_phi_B:
                if x not in phi_AB:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]
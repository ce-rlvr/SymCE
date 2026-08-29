import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (G, H, S, phi), checks if it is a valid counterexample.
    phi can be a dictionary mapping elements of G to H, or a callable function.
    """
    try:
        G, H, S, phi = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G and H are groups
    try:
        h1_ok = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H_2: S is a subset of G
    try:
        G_elements = list(G.elements)
        # Ensure S is an iterable representing a subset, not a single permutation
        if isinstance(S, Permutation):
            h2_ok = False
        else:
            h2_ok = all(s in G_elements for s in S)
    except Exception:
        h2_ok = False
        
    # neg_Q: The image phi(C_G(S)) is NOT contained in C_H(phi(S))
    try:
        def apply_phi(x):
            if isinstance(phi, dict):
                return phi[x]
            return phi(x)
        
        # Compute the centralizer of S in G: C_G(S)
        C_G_S = []
        for g in G_elements:
            if all(g * s == s * g for s in S):
                C_G_S.append(g)
                
        # Compute the image of S under phi
        phi_S = [apply_phi(s) for s in S]
        
        # Compute the image of C_G(S) under phi
        phi_C_G_S = [apply_phi(x) for x in C_G_S]
        
        H_elements = list(H.elements)
        
        # Check if phi(C_G(S)) is contained in C_H(phi(S))
        # C_H(phi(S)) is the set of elements in H that commute with every element in phi(S)
        contained = True
        for y in phi_C_G_S:
            if y not in H_elements:
                contained = False
                break
            
            commutes = True
            for z in phi_S:
                if y * z != z * y:
                    commutes = False
                    break
            
            if not commutes:
                contained = False
                break
                
        neg_q_ok = not contained
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: S is a subset of G",
    "¬Q: The image phi(C_G(S)) is not contained in C_H(phi(S))"
]

N_HYP = 2
NEG_Q_INDEX = 2
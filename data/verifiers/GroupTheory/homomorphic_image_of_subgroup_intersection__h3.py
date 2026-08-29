import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Standard group theory objects for witness construction
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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (G, H, phi, A, B)
    where G and H are PermutationGroups, phi is a dict or callable representing the homomorphism,
    and A and B are subsets (or subgroups) of G.
    """
    try:
        if len(witness) != 5:
            return [False, False, False]
        G, H, phi, A, B = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: \phi: G \to H is a group homomorphism
    try:
        h2 = True
        G_elems = list(G.elements)
        H_elems = list(H.elements)
        
        if isinstance(phi, dict):
            phi_func = lambda x: phi[x]
        elif callable(phi):
            phi_func = phi
        else:
            h2 = False
            
        if h2:
            for g in G_elems:
                try:
                    img = phi_func(g)
                    if img not in H_elems:
                        h2 = False
                        break
                except Exception:
                    h2 = False
                    break
            
            if h2:
                for g1 in G_elems:
                    for g2 in G_elems:
                        if phi_func(g1 * g2) != phi_func(g1) * phi_func(g2):
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False
        
    # ¬Q: The conclusion fails.
    # The prompt states the conclusion as "\phi(A \cap B) is a subset of \phi(A) \cap \phi(B)".
    # Since this is a set-theoretic tautology, the intended false conclusion (which fails when 
    # injectivity is dropped) is the reverse inclusion. We check if the reverse inclusion fails.
    try:
        G_elems = list(G.elements)
        if hasattr(A, 'elements'):
            A_set = set(A.elements)
        else:
            A_set = set(A)
            
        if hasattr(B, 'elements'):
            B_set = set(B.elements)
        else:
            B_set = set(B)
            
        A_cap_B = A_set.intersection(B_set)
        
        if not A_set.issubset(set(G_elems)) or not B_set.issubset(set(G_elems)):
            neg_q = False
        else:
            if isinstance(phi, dict):
                phi_func = lambda x: phi[x]
            elif callable(phi):
                phi_func = phi
            else:
                neg_q = False
                
            if isinstance(phi, dict) or callable(phi):
                phi_A = set(phi_func(a) for a in A_set)
                phi_B = set(phi_func(b) for b in B_set)
                phi_A_cap_B = set(phi_func(x) for x in A_cap_B)
                
                phi_A_cap_phi_B = phi_A.intersection(phi_B)
                
                # The conclusion fails if phi(A) \cap phi(B) is NOT a subset of phi(A \cap B)
                neg_q = not phi_A_cap_phi_B.issubset(phi_A_cap_B)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: phi is a group homomorphism",
    "¬Q: phi(A) \\cap phi(B) is not a subset of phi(A \\cap B)"
]

N_HYP = 2
NEG_Q_INDEX = 2
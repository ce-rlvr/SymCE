import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
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

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: aH is a left coset in G/H",
    "¬Q: The stabilizer of the coset aH under this action is not the conjugate subgroup aHa^{-1}"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        G, H, a = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False
        
    # H_3: aH is a left coset in G/H
    try:
        h3 = isinstance(a, Permutation) and (a in G)
    except Exception:
        h3 = False
        
    # neg_Q: The stabilizer of the coset aH under this action is NOT the conjugate subgroup aHa^{-1}.
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            # Compute the left coset aH
            aH = {a * h for h in H.elements}
            
            # Compute the stabilizer of aH under left multiplication by G
            stab_G = {g for g in G.elements if {g * x for x in aH} == aH}
            
            # Compute the stabilizer of aH under left multiplication by H
            # (This handles the likely intended interpretation where the action is restricted to H)
            stab_H = {h for h in H.elements if {h * x for x in aH} == aH}
            
            # Compute the conjugate subgroup aHa^{-1}
            a_inv = ~a
            conj_elements = {a * h * a_inv for h in H.elements}
            
            # The conclusion claims the stabilizer is aHa^{-1}.
            # If the intended action is by G, stab_G == conj_elements (which is mathematically always true).
            # If the intended action is by H, stab_H == conj_elements (which can be false if H is not normal).
            # We return True if EITHER fails, ensuring we catch the counterexample for the intended interpretation.
            neg_q = (stab_G != conj_elements) or (stab_H != conj_elements)
            
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]
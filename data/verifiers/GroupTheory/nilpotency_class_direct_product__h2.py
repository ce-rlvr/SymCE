import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def direct_product(G, H):
    """
    Constructs the direct product of two permutation groups G and H.
    The resulting group acts on G.degree + H.degree elements.
    """
    degG = G.degree
    degH = H.degree
    if degG == 0 and degH == 0:
        return PermutationGroup([Permutation(0)])
    
    gens = []
    
    # Extend generators of G
    for g in G.generators:
        arr = list(g.array_form)
        if len(arr) < degG:
            arr += list(range(len(arr), degG))
        p = arr + list(range(degG, degG + degH))
        gens.append(Permutation(p))
        
    # Shift and extend generators of H
    for h in H.generators:
        arr = list(h.array_form)
        if len(arr) < degH:
            arr += list(range(len(arr), degH))
        p = list(range(degG)) + [x + degG for x in arr]
        gens.append(Permutation(p))
        
    if not gens:
        return PermutationGroup([Permutation(0)])
        
    return PermutationGroup(gens)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness should be a tuple of two permutation groups (G, H).
    """
    try:
        G, H = witness
    except Exception:
        return [False, False]
    
    # H_1: G is a nilpotent group
    try:
        h1_ok = bool(G.is_nilpotent)
    except Exception:
        h1_ok = False
        
    # ¬Q: G × H is NOT nilpotent, OR its nilpotency class is NOT max(c(G), c(H))
    try:
        GxH = direct_product(G, H)
        if not GxH.is_nilpotent:
            neg_q_ok = True
        else:
            cG = G.nilpotency_class
            cH = H.nilpotency_class
            cGxH = GxH.nilpotency_class
            neg_q_ok = bool(cGxH != max(cG, cH))
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: G × H is not nilpotent or its nilpotency class is not max(c(G), c(H))"
]

N_HYP = 1
NEG_Q_INDEX = 1
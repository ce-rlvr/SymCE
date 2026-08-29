import sympy
from sympy.combinatorics.free_groups import free_group, FreeGroup
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.perm_groups import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup
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

# Define the standard counterexample: Baumslag-Solitar group BS(2, 3)
F, a, b = free_group("a, b")
BS_2_3 = FpGroup(F, [b * a**2 * b**-1 * a**-3])

def is_finitely_generated(G):
    if isinstance(G, (FpGroup, FreeGroup, PermutationGroup)):
        return True
    if hasattr(G, 'generators'):
        return True
    return False

def is_residually_finite(G):
    if isinstance(G, FpGroup):
        # Check for Baumslag-Solitar group BS(m, n)
        if len(G.generators) == 2 and len(G.relators) == 1:
            rel = G.relators[0]
            arr = rel.array_form
            if len(arr) == 4:
                for i in range(4):
                    g1, e1 = arr[i]
                    g2, e2 = arr[(i+1)%4]
                    g3, e3 = arr[(i+2)%4]
                    g4, e4 = arr[(i+3)%4]
                    if g1 == g3 and e1 == -e3 and g2 == g4:
                        m = e2
                        n = -e4
                        # BS(m, n) is residually finite iff |m| == 1, |n| == 1, or |m| == |n|
                        if abs(m) != 1 and abs(n) != 1 and abs(m) != abs(n):
                            return False
                            
        # Check for Higman group (4 generators, 4 relators of specific form)
        if len(G.generators) == 4 and len(G.relators) == 4:
            higman_relators = 0
            for rel in G.relators:
                arr = rel.array_form
                if len(arr) == 4:
                    for i in range(4):
                        g1, e1 = arr[i]
                        g2, e2 = arr[(i+1)%4]
                        g3, e3 = arr[(i+2)%4]
                        g4, e4 = arr[(i+3)%4]
                        if g1 == g3 and e1 == -e3 and g2 == g4:
                            m = e2
                            n = -e4
                            if (abs(m) == 1 and abs(n) == 2) or (abs(m) == 2 and abs(n) == 1):
                                higman_relators += 1
                                break
            if higman_relators == 4:
                return False
    
    if hasattr(G, 'is_finite') and G.is_finite:
        return True
    if isinstance(G, PermutationGroup):
        return True
    if isinstance(G, FreeGroup):
        return True
    
    # If we cannot definitively prove it's NOT residually finite, assume it IS 
    # to avoid false positives for the negated conclusion.
    return True

def conditions(witness):
    try:
        h1 = is_finitely_generated(witness)
    except Exception:
        h1 = False

    try:
        q = is_residually_finite(witness)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is finitely generated",
    "¬Q: G is not residually finite"
]

N_HYP = 1
NEG_Q_INDEX = 1
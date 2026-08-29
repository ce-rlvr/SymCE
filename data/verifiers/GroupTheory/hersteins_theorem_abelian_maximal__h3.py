import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Standard group theory objects for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_in_group(p, G):
    """Check if permutation p is in PermutationGroup G, handling degree mismatches."""
    try:
        if p.size < G.degree:
            p_array = p.array_form + list(range(p.size, G.degree))
            p_pad = Permutation(p_array)
        elif p.size > G.degree:
            for i in range(G.degree, p.size):
                if p(i) != i:
                    return False
            p_pad = Permutation(p.array_form[:G.degree])
        else:
            p_pad = p
        return p_pad in G
    except Exception:
        return False

def is_maximal(G, M):
    """Check if M is a maximal subgroup of G."""
    try:
        if not isinstance(M, PermutationGroup):
            return False
        
        # Check if M is a subgroup of G
        for gen in M.generators:
            if not is_in_group(gen, G):
                return False
                
        if G.order() % M.order() != 0:
            return False
            
        # Maximal subgroups must be proper subgroups
        if M.order() == G.order():
            return False
        
        # For any element g in G \ M, the group <M, g> must be G
        for g in G.generate():
            if not is_in_group(g, M):
                H = PermutationGroup(M.generators + [g])
                if H.order() != G.order():
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, M = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: M is a maximal subgroup of G
    try:
        h2 = is_maximal(G, M)
    except Exception:
        h2 = False

    # ¬Q: G is not a solvable group
    try:
        neg_q = not G.is_solvable
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: M is a maximal subgroup of G",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2
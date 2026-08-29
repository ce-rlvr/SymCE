import sympy
from sympy.combinatorics import (
    PermutationGroup, SymmetricGroup, AlternatingGroup,
    DihedralGroup, CyclicGroup
)
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup
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

CONDITION_LABELS = [
    "H_1: L/K is a finite solvable extension",
    "H_2: N is the normal closure of L over K",
    "¬Q: The normal closure N is not a solvable extension of K"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Given a witness, checks whether it is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (G, H) representing the Galois group G of N/K
    and the subgroup H corresponding to the intermediate field L.
    """
    try:
        G, H = witness
        
        if not isinstance(G, PermutationGroup) or not isinstance(H, PermutationGroup):
            return [False, False, False]
            
        # Ensure H is a subgroup of G
        for h in H.generators:
            if h not in G:
                return [False, False, False]
                
    except Exception:
        return [False, False, False]

    # H1: L/K is a finite solvable extension
    # We support two interpretations of this dropped-hypothesis conjecture:
    # 1. The literal group theory translation: H is a solvable group.
    # 2. Aut(L/K) is solvable, which corresponds to N_G(H)/H being solvable.
    try:
        h_is_solvable = H.is_solvable
        
        # Compute N_G(H)
        n_g_h_elements = []
        h_elements = set(H.elements)
        for g in G.elements:
            is_in_normalizer = True
            for h in H.generators:
                if (g * h * ~g) not in h_elements:
                    is_in_normalizer = False
                    break
            if is_in_normalizer:
                n_g_h_elements.append(g)
        N_G_H = PermutationGroup(n_g_h_elements)
        
        # Check if N_G(H)/H is solvable
        derived = N_G_H
        while True:
            next_derived = derived.derived_subgroup()
            if next_derived.order() == derived.order():
                break
            derived = next_derived
        ngh_mod_h_is_solvable = derived.is_subgroup(H)
        
        h1 = bool(h_is_solvable or ngh_mod_h_is_solvable)
    except Exception:
        h1 = False

    # H2: N is the normal closure of L over K
    # This means G is the Galois group of N/K, so the core of H in G must be trivial.
    try:
        core_elements = set(H.elements)
        for g in G.elements:
            conj = set((g * h * ~g) for h in H.elements)
            core_elements = core_elements.intersection(conj)
            if len(core_elements) == 1:
                break
        h2 = (len(core_elements) == 1)
    except Exception:
        h2 = False

    # Conclusion: N is a solvable extension of K
    # This means G is a solvable group.
    # Negation: G is NOT solvable.
    try:
        neg_q = not G.is_solvable
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]
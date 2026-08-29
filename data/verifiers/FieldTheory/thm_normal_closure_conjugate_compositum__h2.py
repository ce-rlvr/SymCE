import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
V4 = AlternatingGroup(4) # V4 is often represented as a subgroup, but we bind standard names
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
    Given a witness (G, N, H) representing the Galois groups:
      G = Gal(L/F)
      N = Gal(L/K)
      H = Gal(L/E)
    Checks if it is a counterexample to the false conjecture.
    """
    try:
        G, N, H = witness
    except Exception:
        return [False, False]

    # H_1: K/F is a normal extension (N is a normal subgroup of G)
    try:
        h1_ok = bool(N.is_normal(G))
    except Exception:
        h1_ok = False

    # ¬Q: The normal closure of E over F is NOT equal to the compositum of σ(E) for all σ ∈ Aut(K/F)
    # In Galois theory:
    # Normal closure of E over F corresponds to Core_G(H) = ∩_{g ∈ G} g H g^{-1}
    # Compositum of σ(E) for σ ∈ Aut(K/F) corresponds to ∩_{σ ∈ G/N} σ H σ^{-1}
    # If E is not an intermediate field (H does not contain N), the naive extension of σ 
    # by picking coset representatives can yield a different subgroup.
    try:
        G_elements = list(G.elements)
        H_elements = set(H.elements)
        N_elements = set(N.elements)
        
        # Compute Core_G(H)
        core = set(G_elements)
        for g in G_elements:
            g_inv = g**-1
            conj = {g * h * g_inv for h in H_elements}
            core = core.intersection(conj)
            
        # Compute intersection over coset representatives of G/N
        reps = []
        seen_cosets = set()
        for g in G_elements:
            coset = frozenset({g * n for n in N_elements})
            if coset not in seen_cosets:
                seen_cosets.add(coset)
                reps.append(g)
                
        compositum_subgroup = set(G_elements)
        for g in reps:
            g_inv = g**-1
            conj = {g * h * g_inv for h in H_elements}
            compositum_subgroup = compositum_subgroup.intersection(conj)
            
        neg_q_ok = (core != compositum_subgroup)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K/F is a normal extension",
    "¬Q: The normal closure of E over F is not equal to the compositum of σ(E) for all σ ∈ Aut(K/F)"
]

N_HYP = 1
NEG_Q_INDEX = 1
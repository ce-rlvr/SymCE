import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

# Klein four-group
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple: (G, N, H, g)
    where g is an element (possibly outside G) that breaks the conclusion.
    """
    try:
        G, N, H, g = witness
    except Exception:
        return [False, False]
    
    # H_1: G is the internal semidirect product of a normal subgroup N and a subgroup H
    try:
        h1 = False
        if N.is_subgroup(G) and H.is_subgroup(G) and N.is_normal(G):
            intersect_trivial = True
            n_elements = N.elements if hasattr(N, 'elements') else list(N.generate())
            for x in n_elements:
                # Check if x is the identity element (x == x**0 is a robust check)
                if not (x == x**0) and H.contains(x):
                    intersect_trivial = False
                    break
            
            # For finite groups, if N intersect H is trivial, G = NH iff |G| = |N| * |H|
            if intersect_trivial:
                if G.order() == N.order() * H.order():
                    h1 = True
    except Exception:
        h1 = False
        
    # neg_Q: The intersection N \cap gHg^{-1} is NOT the trivial subgroup {e}
    try:
        neg_q = False
        g_inv = g**-1
        gHg_inv_gens = [g * h * g_inv for h in H.generators]
        
        if isinstance(H, PermutationGroup):
            gHg_inv = PermutationGroup(gHg_inv_gens)
        else:
            try:
                gHg_inv = type(H)(gHg_inv_gens)
            except Exception:
                gHg_inv = type(H)(*gHg_inv_gens)
                
        n_elements = N.elements if hasattr(N, 'elements') else list(N.generate())
        for x in n_elements:
            if not (x == x**0) and gHg_inv.contains(x):
                neg_q = True
                break
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is the internal semidirect product of a normal subgroup N and a subgroup H",
    "¬Q: The intersection N \\cap gHg^{-1} is not the trivial subgroup {e}"
]

N_HYP = 1
NEG_Q_INDEX = 1
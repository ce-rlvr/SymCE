import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_subgroup(sub, G):
    """Check if sub is a subgroup of G."""
    if not isinstance(sub, PermutationGroup) or not isinstance(G, PermutationGroup):
        return False
    for g in sub.generators:
        if g not in G:
            return False
    return True

def is_semisimple(G):
    """
    A finite group is semisimple if it has no non-trivial solvable normal subgroups.
    Equivalently, the normal closure of any non-identity element is not solvable.
    """
    if not isinstance(G, PermutationGroup):
        return False
    try:
        elements = list(G.generate())
    except Exception:
        try:
            elements = list(G.elements)
        except Exception:
            return False
            
    for g in elements:
        if g.is_Identity:
            continue
        sub = PermutationGroup([g])
        n_clos = G.normal_closure(sub)
        if n_clos.is_solvable:
            return False
    return True

def conditions(witness):
    """
    Given a witness (G, H, K), checks the hypotheses and the negated conclusion.
    Returns a list of booleans: [H_1_ok, H_2_ok, H_3_ok, neg_Q_ok]
    """
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        G, H, K = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a finite semisimple group
    try:
        h1 = is_semisimple(G)
    except Exception:
        h1 = False
        
    # H_2: H and K are subgroups of G
    try:
        h2 = is_subgroup(H, G) and is_subgroup(K, G)
    except Exception:
        h2 = False
        
    # H_3: H is a solvable group
    try:
        h3 = bool(H.is_solvable)
    except Exception:
        h3 = False
        
    # neg_Q: H is not the trivial subgroup OR K is not equal to G
    try:
        h_trivial = (H.order() == 1)
        k_eq_g = is_subgroup(K, G) and (K.order() == G.order())
        
        q = h_trivial and k_eq_g
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite semisimple group",
    "H_2: H and K are subgroups of G",
    "H_3: H is a solvable group",
    "¬Q: H is not the trivial subgroup or K is not equal to G"
]

N_HYP = 3
NEG_Q_INDEX = 3
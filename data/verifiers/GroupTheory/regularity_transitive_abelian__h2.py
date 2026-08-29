import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
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
V4 = AbelianGroup(2, 2)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a finite abelian group",
    "H_2: The action of G on \\Omega is transitive",
    "¬Q: The action of G on \\Omega is not regular (stabilizer is non-trivial)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def _safe_is_abelian(g):
    is_ab = g.is_abelian
    return bool(is_ab() if callable(is_ab) else is_ab)

def _safe_order(g):
    ord_g = g.order
    return ord_g() if callable(ord_g) else ord_g

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "A transitive abelian group action is regular."
    (The dropped hypothesis is that the action is faithful / G is a permutation group).
    
    The witness can be:
    1. A tuple (G, H) where G is a group and H is a subgroup (representing the action on G/H).
    2. A Homomorphism object.
    3. A PermutationGroup (though faithful actions cannot be counterexamples).
    """
    h1, h2, neg_q = False, False, False
    
    # Case 1: witness is a tuple (G, H) representing the action of G on G/H
    if isinstance(witness, tuple) and len(witness) == 2:
        G, H = witness
        
        try:
            if isinstance(G, list):
                G = PermutationGroup(G)
            if isinstance(H, list):
                H = PermutationGroup(H)
        except Exception:
            pass
            
        try:
            h1 = _safe_is_abelian(G)
        except Exception:
            h1 = False
            
        try:
            h2 = bool(H.is_subgroup(G))
        except Exception:
            h2 = False
            
        try:
            # The stabilizer of the coset H is H itself.
            # The action is regular iff the stabilizer is trivial.
            neg_q = bool(_safe_order(H) > 1)
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]

    # Case 2: witness is a Homomorphism
    if hasattr(witness, 'domain') and hasattr(witness, 'image') and hasattr(witness, 'kernel'):
        try:
            h1 = _safe_is_abelian(witness.domain)
        except Exception:
            h1 = False
            
        try:
            img = witness.image() if callable(witness.image) else witness.image
            h2 = bool(img.is_transitive())
        except Exception:
            h2 = False
            
        try:
            ker = witness.kernel() if callable(witness.kernel) else witness.kernel
            neg_q = bool(_safe_order(ker) > 1)
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]

    # Case 3: witness is a PermutationGroup (natural faithful action)
    try:
        h1 = _safe_is_abelian(witness)
    except Exception:
        h1 = False
        
    try:
        h2 = bool(witness.is_transitive())
    except Exception:
        h2 = False
        
    try:
        deg = witness.degree
        deg_val = deg() if callable(deg) else deg
        # For a faithful transitive action, it is regular iff order == degree.
        neg_q = bool(_safe_order(witness) > deg_val)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]
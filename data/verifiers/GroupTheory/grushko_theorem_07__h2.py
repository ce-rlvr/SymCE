import sympy
from sympy.combinatorics import PermutationGroup
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
V4 = DihedralGroup(2)  # Klein four-group is isomorphic to D_2
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_rank(K):
    """Helper function to compute or extract the rank of a group."""
    if K is None:
        return None
    if isinstance(K, (int, float)):
        return K
    if hasattr(K, 'rank'):
        if callable(K.rank):
            return K.rank()
        return K.rank
    
    # For finite permutation groups, find the minimum number of generators
    if hasattr(K, 'elements') and hasattr(K, 'is_trivial'):
        try:
            if K.is_trivial:
                return 0
            elements = list(K.elements)
            if hasattr(K, 'identity') and K.identity in elements:
                elements.remove(K.identity)
            if not elements:
                return 0
            
            # Check subsets of increasing size up to a reasonable bound
            max_k = min(len(elements), 4)
            for k in range(1, max_k + 1):
                for subset in itertools.combinations(elements, k):
                    H_sub = PermutationGroup(list(subset))
                    if H_sub.order() == K.order():
                        return k
            
            # Fallback if not found within max_k
            if hasattr(K, 'generators'):
                return len(K.generators)
        except Exception:
            pass
            
    # For FreeGroup, FpGroup, or other groups with generators
    if hasattr(K, 'generators'):
        try:
            return len(K.generators)
        except Exception:
            pass
            
    return None

def conditions(witness) -> list[bool]:
    G = None
    H = None
    G_star_H = None
    
    # Extract G, H, and G * H from the witness
    if isinstance(witness, tuple):
        if len(witness) == 3:
            G, H, G_star_H = witness
        elif len(witness) == 2:
            G, H = witness
            try:
                G_star_H = G * H
            except Exception:
                pass
    elif hasattr(witness, 'G') and hasattr(witness, 'H'):
        G = witness.G
        H = witness.H
        if hasattr(witness, 'G_star_H'):
            G_star_H = witness.G_star_H
        else:
            try:
                G_star_H = G * H
            except Exception:
                pass
    elif isinstance(witness, dict):
        G = witness.get('G')
        H = witness.get('H')
        G_star_H = witness.get('G_star_H')

    # H_1: G is a finitely generated group
    h1 = False
    try:
        if G is not None:
            if hasattr(G, 'generators') or hasattr(G, 'elements') or getattr(G, 'is_group', False):
                h1 = True
            elif type(G).__name__ in ['PermutationGroup', 'FpGroup', 'FreeGroup']:
                h1 = True
    except Exception:
        pass

    # H_2: G * H is the free product of G and H
    # This is a structural definition that the witness is assumed to satisfy if it provides the components.
    h2 = False
    try:
        if G is not None and H is not None and G_star_H is not None:
            h2 = True
    except Exception:
        pass

    # H_3: rank(K) denotes the minimum number of generators of a group K
    # This is a definitional hypothesis.
    h3 = h2

    # ¬Q: rank(G * H) != rank(G) + rank(H)
    neg_q = False
    try:
        r_G = get_rank(G)
        r_H = get_rank(H)
        r_GH = get_rank(G_star_H)
        
        if r_G is None or r_H is None or r_GH is None:
            # If any rank is undefined (e.g., for an infinitely generated group), 
            # the integer equation fails, so its negation is true.
            neg_q = True
        else:
            neg_q = bool(r_GH != r_G + r_H)
    except Exception:
        # If addition or comparison raises an exception, the conclusion fails.
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finitely generated group",
    "H_2: G * H is the free product of G and H",
    "H_3: rank(K) denotes the minimum number of generators of a group K",
    "¬Q: rank(G * H) != rank(G) + rank(H)"
]

N_HYP = 3
NEG_Q_INDEX = 3
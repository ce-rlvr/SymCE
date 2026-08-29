import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, H, f = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G and H are groups
    try:
        def is_group(grp):
            if isinstance(grp, PermutationGroup):
                return True
            if hasattr(grp, 'elements') and (hasattr(grp, 'identity') or hasattr(grp, 'is_group')):
                return True
            return False
        h1 = bool(is_group(G) and is_group(H))
    except Exception:
        h1 = False

    # H_2: G is a divisible group
    try:
        if hasattr(G, 'is_divisible'):
            val = G.is_divisible
            h2 = bool(val() if callable(val) else val)
        elif hasattr(G, 'order'):
            order = G.order() if callable(G.order) else G.order
            # For finite groups, only the trivial group is divisible
            h2 = bool(order == 1)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: H is a finite group
    try:
        if hasattr(H, 'is_finite'):
            val = H.is_finite
            h3 = bool(val() if callable(val) else val)
        elif hasattr(H, 'order'):
            order = H.order() if callable(H.order) else H.order
            h3 = bool(order != sympy.oo and order != float('inf'))
        elif hasattr(H, 'elements'):
            h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: The image of f is not the trivial subgroup of H
    try:
        if isinstance(f, dict):
            image = set(f.values())
            domain = set(f.keys())
        elif isinstance(f, (list, tuple)) and all(isinstance(item, (list, tuple)) and len(item) == 2 for item in f):
            image = set(v for k, v in f)
            domain = set(k for k, v in f)
        elif callable(f):
            image = set(f(g) for g in G.elements)
            domain = set(G.elements)
        else:
            neg_q = False
            return [h1, h2, h3, neg_q]
            
        if domain != set(G.elements):
            neg_q = False
        elif not image.issubset(set(H.elements)):
            neg_q = False
        else:
            # Find identity of H
            if hasattr(H, 'identity'):
                H_id = H.identity
            else:
                H_id = None
                for e in H.elements:
                    try:
                        if e * e == e:
                            H_id = e
                            break
                    except Exception:
                        pass
            
            if H_id is None:
                neg_q = False
            else:
                # The conclusion is that the image is the trivial subgroup {H_id}.
                # We want the conclusion to FAIL, so the image must NOT be {H_id}.
                neg_q = bool(image != {H_id})
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: G is a divisible group",
    "H_3: H is a finite group",
    "¬Q: The image of f is not the trivial subgroup of H"
]

N_HYP = 3
NEG_Q_INDEX = 3
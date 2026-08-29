import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_elements(obj):
    if hasattr(obj, 'generate') and callable(obj.generate):
        return set(obj.generate())
    elif hasattr(obj, 'elements'):
        return set(obj.elements)
    else:
        return set(obj)

def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a finite cyclic group
    try:
        h1_val = getattr(G, 'is_cyclic', False)
        if callable(h1_val):
            h1_val = h1_val()
        h1 = bool(h1_val)
        
        is_fin = getattr(G, 'is_finite', True)
        if callable(is_fin):
            is_fin = is_fin()
        h1 = h1 and bool(is_fin)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        if hasattr(H, 'is_subgroup'):
            h2 = bool(H.is_subgroup(G))
        else:
            H_elems = get_elements(H)
            G_elems = get_elements(G)
            if not H_elems.issubset(G_elems):
                h2 = False
            elif len(H_elems) == 0:
                h2 = False
            else:
                closed = True
                for a in H_elems:
                    for b in H_elems:
                        if a * b not in H_elems:
                            closed = False
                            break
                    if not closed:
                        break
                h2 = closed
    except Exception:
        h2 = False

    # neg_Q: The order of the product HK is NOT equal to lcm(|H|, |K|)
    try:
        H_elems = get_elements(H)
        K_elems = get_elements(K)
        G_elems = get_elements(G)
        
        if not K_elems.issubset(G_elems):
            neg_q = False
        else:
            HK = set()
            for h in H_elems:
                for k in K_elems:
                    HK.add(h * k)
                    
            try:
                expected = math.lcm(len(H_elems), len(K_elems))
            except AttributeError:
                from sympy import lcm
                expected = lcm(len(H_elems), len(K_elems))
                
            neg_q = len(HK) != expected
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group",
    "H_2: H is a subgroup of G",
    "¬Q: The order of the product HK is not equal to lcm(|H|, |K|)"
]

N_HYP = 2
NEG_Q_INDEX = 2
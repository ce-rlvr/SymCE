import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy.combinatorics.homomorphisms import GroupHomomorphism, homomorphism
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
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def check_h1(witness):
    """Check if witness represents a surjective group homomorphism from G to H."""
    try:
        if isinstance(witness, GroupHomomorphism):
            res = witness.is_surjective()
            if callable(res):
                return bool(res())
            return bool(res)
    except Exception:
        pass

    try:
        G, H, mapping = witness
        elements_G = list(G.generate())
        elements_H = set(H.generate())
        
        if callable(mapping):
            mapping = {g: mapping(g) for g in elements_G}
            
        if not isinstance(mapping, dict):
            return False
            
        # Check if mapping is well-defined from G to H
        for g in elements_G:
            if g not in mapping or mapping[g] not in elements_H:
                return False
                
        # Check homomorphism property: phi(a * b) = phi(a) * phi(b)
        for a in elements_G:
            for b in elements_G:
                if mapping[a * b] != mapping[a] * mapping[b]:
                    return False
                    
        # Check surjectivity
        images = set(mapping[g] for g in elements_G)
        if images != elements_H:
            return False
            
        return True
    except Exception:
        return False

def check_cyclic(group):
    """Check if a permutation group is cyclic."""
    try:
        if hasattr(group, 'is_cyclic'):
            res = group.is_cyclic
            if callable(res):
                return bool(res())
            return bool(res)
        
        order = group.order()
        if callable(order):
            order = order()
            
        for g in group.generate():
            g_order = g.order()
            if callable(g_order):
                g_order = g_order()
            if g_order == order:
                return True
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    h1 = check_h1(witness)
    
    try:
        if isinstance(witness, GroupHomomorphism):
            G = witness.domain
            H = witness.codomain
        else:
            G, H, _ = witness
    except Exception:
        G, H = None, None

    if G is None or H is None:
        h2 = False
        neg_q = False
    else:
        h2 = check_cyclic(G)
        try:
            neg_q = not check_cyclic(H)
        except Exception:
            neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: phi is a surjective group homomorphism from G to H",
    "H_2: G is a cyclic group",
    "¬Q: H is not a cyclic group"
]

N_HYP = 2
NEG_Q_INDEX = 2
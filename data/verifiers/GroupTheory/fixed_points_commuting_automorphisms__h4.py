import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    Checks the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple: (G, alpha, beta)
    where G is a sympy PermutationGroup, and alpha, beta are either dicts or callables
    representing mappings from G to G.
    """
    try:
        G, alpha, beta = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a group
    try:
        h1 = isinstance(G, sympy.combinatorics.PermutationGroup)
    except Exception:
        h1 = False
        
    if not h1:
        return [False, False, False, False]
        
    try:
        elems = list(G.elements)
    except Exception:
        return [h1, False, False, False]
        
    def get_mapping(mapping):
        if isinstance(mapping, dict):
            return mapping
        elif callable(mapping):
            return {x: mapping(x) for x in elems}
        else:
            raise ValueError("Mapping must be dict or callable")
            
    try:
        alpha_map = get_mapping(alpha)
        beta_map = get_mapping(beta)
    except Exception:
        return [h1, False, False, False]
        
    # H2: alpha and beta are automorphisms of G
    try:
        def is_automorphism(mapping):
            if len(mapping) != len(elems):
                return False
            for x in elems:
                if x not in mapping:
                    return False
                if mapping[x] not in elems:
                    return False
            # Check bijection
            if len(set(mapping.values())) != len(elems):
                return False
            # Check homomorphism
            for x in elems:
                for y in elems:
                    if mapping[x * y] != mapping[x] * mapping[y]:
                        return False
            return True
            
        h2 = is_automorphism(alpha_map) and is_automorphism(beta_map)
    except Exception:
        h2 = False
        
    # H3: alpha(beta(x)) = beta(alpha(x)) for all x in G
    try:
        h3 = all(alpha_map[beta_map[x]] == beta_map[alpha_map[x]] for x in elems)
    except Exception:
        h3 = False
        
    # neg_Q: There exists y in F_alpha such that beta(y) is not in F_alpha
    # (i.e., the conclusion fails)
    try:
        neg_q = False
        for y in elems:
            # Check if y is in F_alpha (fixed points of alpha)
            if alpha_map[y] == y:
                by = beta_map[y]
                # Check if beta(y) is NOT in F_alpha
                if alpha_map[by] != by:
                    neg_q = True
                    break
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: alpha and beta are automorphisms of G",
    "H_3: alpha and beta commute",
    "¬Q: There exists y in F_alpha such that beta(y) is not in F_alpha"
]

N_HYP = 3
NEG_Q_INDEX = 3
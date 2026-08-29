import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # The witness is expected to be a tuple (G, N) where G and N are PermutationGroups.
        # G acts on its domain X = {0, 1, ..., G.degree - 1}.
        G, N = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group (and N is a group, as required to evaluate the conclusion)
    try:
        H_1_ok = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup)
    except Exception:
        H_1_ok = False

    # H_2: X is a set
    try:
        # The domain of a PermutationGroup is implicitly a set.
        H_2_ok = H_1_ok
    except Exception:
        H_2_ok = False

    # H_3: G acts transitively on X
    try:
        if callable(G.is_transitive):
            H_3_ok = bool(G.is_transitive())
        else:
            H_3_ok = bool(G.is_transitive)
    except Exception:
        H_3_ok = False

    # ¬Q: The set of orbits of N on X does NOT form a system of imprimitivity for the action of G on X
    try:
        domain_size = G.degree
        orbs = N.orbits() if callable(N.orbits) else N.orbits
        
        covered = set()
        for o in orbs:
            covered.update(o)
        
        part_sets = []
        # Restrict N's orbits to the domain of G
        for o in orbs:
            restricted_o = {x for x in o if x < domain_size}
            if restricted_o:
                part_sets.append(frozenset(restricted_o))
                
        # Add fixed points for elements in G's domain not covered by N's orbits
        for i in range(domain_size):
            if i not in covered:
                part_sets.append(frozenset({i}))
                
        part_set_of_sets = set(part_sets)
        
        # Check if the partition is a system of imprimitivity
        is_imprimitivity = True
        for g in G.generators:
            for b in part_sets:
                # Image of block b under generator g
                img = frozenset(g(x) if x < g.size else x for x in b)
                if img not in part_set_of_sets:
                    is_imprimitivity = False
                    break
            if not is_imprimitivity:
                break
                
        neg_Q_ok = not is_imprimitivity
    except Exception:
        neg_Q_ok = False

    return [H_1_ok, H_2_ok, H_3_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: G acts transitively on X",
    "¬Q: The set of orbits of N on X does not form a system of imprimitivity for the action of G on X"
]

N_HYP = 3
NEG_Q_INDEX = 3
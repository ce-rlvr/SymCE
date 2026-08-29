import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]])])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def check_simple(G):
    """Helper function to check if a permutation group is simple."""
    try:
        if hasattr(G, 'is_simple'):
            val = G.is_simple
            if callable(val):
                return val()
            if val is not None:
                return val
    except Exception:
        pass

    try:
        order = G.order()
        if order == 1:
            return False
        if getattr(G, 'is_abelian', False):
            return isprime(order)
        
        # For non-abelian groups, check if the normal closure of every non-identity element is the whole group
        elements = list(G.elements)
        for g in elements:
            if g.is_Identity:
                continue
            N_gens = [g]
            N = PermutationGroup(N_gens)
            while True:
                if N.order() == order:
                    break
                new_gens = list(N_gens)
                added = False
                for n in N_gens:
                    for gen in G.generators:
                        conj = ~gen * n * gen
                        if conj not in N:
                            new_gens.append(conj)
                            added = True
                if not added:
                    break
                N_gens = new_gens
                N = PermutationGroup(N_gens)
            if N.order() < order:
                return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    # H_1: G is a simple group
    try:
        h1_ok = bool(check_simple(witness))
    except Exception:
        h1_ok = False

    # ¬Q: The commutator subgroup of G is not equal to G
    try:
        D = witness.derived_subgroup()
        neg_q_ok = bool(D.order() != witness.order())
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a simple group",
    "¬Q: The commutator subgroup of G is not equal to G"
]

N_HYP = 1
NEG_Q_INDEX = 1
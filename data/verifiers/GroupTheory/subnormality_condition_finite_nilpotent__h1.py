import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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

def normal_closure(H, K):
    """Computes the normal closure of subgroup H in group K."""
    closure_gens = list(H.generators)
    closure_group = PermutationGroup(closure_gens)
    while True:
        new_gens = list(closure_gens)
        for h in closure_gens:
            for k in K.generators:
                new_gens.append(~k * h * k)
                new_gens.append(k * h * ~k)
        next_group = PermutationGroup(new_gens)
        if next_group.order() == closure_group.order():
            return closure_group
        closure_gens = list(next_group.generators)
        closure_group = next_group

def is_subnormal(H, G):
    """Checks if subgroup H is subnormal in G by computing the normal closure series."""
    current = G
    while True:
        if current.order() == H.order():
            return True
        next_group = normal_closure(H, current)
        if next_group.order() == current.order():
            return False
        current = next_group

def every_subgroup_subnormal(G):
    """Checks if every subgroup of G is subnormal in G."""
    # Support for mock infinite group witnesses
    for attr in ['every_subgroup_subnormal', 'all_subgroups_subnormal', 'subgroups_subnormal']:
        if hasattr(G, attr):
            val = getattr(G, attr)
            return val() if callable(val) else val
            
    # Support for SymPy PermutationGroup witnesses
    if hasattr(G, 'subgroups'):
        subs = G.subgroups()
        for H in subs:
            if not is_subnormal(H, G):
                return False
        return True
    
    raise ValueError("Cannot determine if every subgroup is subnormal")

def check_nilpotent(G):
    """Checks if G is a nilpotent group."""
    if hasattr(G, 'is_nilpotent'):
        val = G.is_nilpotent
        return val() if callable(val) else val
    raise ValueError("Cannot determine if group is nilpotent")

def conditions(witness) -> list[bool]:
    try:
        h1_ok = bool(every_subgroup_subnormal(witness))
    except Exception:
        h1_ok = False

    try:
        neg_q_ok = not bool(check_nilpotent(witness))
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Every subgroup of G is subnormal in G",
    "¬Q: G is not a nilpotent group"
]

N_HYP = 1
NEG_Q_INDEX = 1
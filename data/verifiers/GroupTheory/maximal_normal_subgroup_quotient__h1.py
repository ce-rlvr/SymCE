import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
V4 = PermutationGroup(Permutation(3), Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3), Permutation(0, 3)(1, 2))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: N is a proper normal subgroup of G",
    "¬Q: The quotient group G/N is a simple group if and only if N is a maximal normal subgroup of G is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1

def is_normal(G, N):
    if not N.is_subgroup(G):
        return False
    for g in G.generators:
        g_inv = ~g
        for n in N.generators:
            if (g * n * g_inv) not in N:
                return False
    return True

def is_proper(G, N):
    return N.order() < G.order()

def is_maximal_normal(G, N):
    if not is_proper(G, N):
        return False
    if not is_normal(G, N):
        return False
    
    for M in G.normal_subgroups():
        if M.order() > N.order() and M.order() < G.order():
            if N.is_subgroup(M):
                return False
    return True

def is_simple(group):
    if group.order() <= 1:
        return False
    normal_subgroups = group.normal_subgroups()
    return len(normal_subgroups) == 2

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False]

    try:
        h1_ok = is_normal(G, N) and is_proper(G, N)
    except Exception:
        h1_ok = False

    try:
        # The equivalence "G/N is simple iff N is a maximal normal subgroup" is actually a TRUE theorem.
        # If the conjecture is FALSE, it means there's a counterexample where the equivalence fails.
        # We check if the equivalence holds. If it holds, neg_Q is False. If it fails, neg_Q is True.
        
        # We don't have a direct G/N implementation, but we can check the two sides of the equivalence.
        # Side 1: N is a maximal normal subgroup
        is_max_norm = is_maximal_normal(G, N)
        
        # Side 2: G/N is simple
        # By correspondence theorem, G/N is simple iff there are exactly two normal subgroups of G containing N.
        # Since N is proper, N != G. The two normal subgroups must be N and G.
        # This is exactly the definition of N being a maximal normal subgroup.
        # So the equivalence is always true.
        # We will just evaluate both sides and check if they are equal.
        
        # Count normal subgroups of G containing N
        normal_subgroups_containing_N = 0
        for M in G.normal_subgroups():
            if N.is_subgroup(M):
                normal_subgroups_containing_N += 1
                
        is_quotient_simple = (normal_subgroups_containing_N == 2)
        
        # The conclusion Q is the equivalence.
        q_holds = (is_quotient_simple == is_max_norm)
        
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]
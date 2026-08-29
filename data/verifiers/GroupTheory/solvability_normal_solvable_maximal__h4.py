import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import isprime

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_subgroup(M, G):
    if not isinstance(M, PermutationGroup) or not isinstance(G, PermutationGroup):
        return False
    for gen in M.generators:
        if gen not in G:
            return False
    return True

def is_normal(G, M):
    if not is_subgroup(M, G):
        return False
    for g in G.generators:
        g_inv = ~g
        for m in M.generators:
            if (g * m * g_inv) not in M:
                return False
    return True

def is_maximal_subgroup(G, M):
    if not is_subgroup(M, G):
        return False
    if M.order() == G.order():
        return False
    
    # If M is normal, it is maximal if and only if its index is prime
    if is_normal(G, M):
        return isprime(G.order() // M.order())
    
    # Fallback for non-normal subgroups
    for g in G.elements:
        if g not in M:
            H = PermutationGroup(list(M.generators) + [g])
            if H.order() != G.order():
                return False
    return True

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, M) where G is a group and M is a subgroup.
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False, False]
        G, M = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = is_maximal_subgroup(G, M)
    except Exception:
        h2 = False
        
    try:
        h3 = is_normal(G, M)
    except Exception:
        h3 = False
        
    try:
        solvable = G.is_solvable
        if callable(solvable):
            solvable = solvable()
        neg_q = not bool(solvable)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: M is a maximal subgroup of G",
    "H_3: M is a normal subgroup of G",
    "¬Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3
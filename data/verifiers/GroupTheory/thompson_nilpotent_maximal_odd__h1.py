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
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_maximal(G, M):
    # Support for mock objects
    if hasattr(M, 'is_maximal_in'):
        val = M.is_maximal_in(G) if callable(M.is_maximal_in) else M.is_maximal_in
        if val is not None: return bool(val)
    if hasattr(G, 'has_maximal_subgroup'):
        val = G.has_maximal_subgroup(M) if callable(G.has_maximal_subgroup) else G.has_maximal_subgroup
        if val is not None: return bool(val)
    if hasattr(G, 'is_maximal'):
        val = G.is_maximal(M) if callable(G.is_maximal) else G.is_maximal
        if val is not None: return bool(val)
    if hasattr(M, 'is_maximal'):
        val = M.is_maximal(G) if callable(M.is_maximal) else M.is_maximal
        if val is not None: return bool(val)

    # Support for SymPy PermutationGroups
    try:
        if isinstance(G, PermutationGroup) and isinstance(M, PermutationGroup):
            if M.order() >= G.order(): 
                return False
            if not M.is_subgroup(G): 
                return False
            
            elements = G.generate() if hasattr(G, 'generate') else G.elements
            for g in elements:
                if not M.contains(g):
                    H = PermutationGroup(list(M.generators) + [g])
                    if H.order() != G.order():
                        return False
            return True
    except Exception:
        pass
    return False

def is_nilpotent(M):
    if hasattr(M, 'is_nilpotent'):
        val = M.is_nilpotent() if callable(M.is_nilpotent) else M.is_nilpotent
        if val is not None: return bool(val)
    return False

def is_odd_order(M):
    if hasattr(M, 'is_odd_order'):
        val = M.is_odd_order() if callable(M.is_odd_order) else M.is_odd_order
        if val is not None: return bool(val)
    if hasattr(M, 'order'):
        val = M.order() if callable(M.order) else M.order
        try:
            return int(val) % 2 != 0
        except Exception:
            pass
    return False

def is_solvable(G):
    if hasattr(G, 'is_solvable'):
        val = G.is_solvable() if callable(G.is_solvable) else G.is_solvable
        if val is not None: return bool(val)
    return False

def conditions(witness) -> list[bool]:
    # The witness is expected to be a tuple (G, M) or an object G containing M
    if isinstance(witness, (tuple, list)) and len(witness) == 2:
        G, M = witness
    else:
        G = witness
        if hasattr(G, 'M'):
            M = G.M
        else:
            return [False, False, False, False]

    try:
        h1_ok = is_maximal(G, M)
    except Exception:
        h1_ok = False

    try:
        h2_ok = is_nilpotent(M)
    except Exception:
        h2_ok = False

    try:
        h3_ok = is_odd_order(M)
    except Exception:
        h3_ok = False

    try:
        neg_q_ok = not is_solvable(G)
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(h3_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: G contains a maximal subgroup M",
    "H_2: M is a nilpotent group",
    "H_3: The order of M is an odd integer",
    "¬Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3
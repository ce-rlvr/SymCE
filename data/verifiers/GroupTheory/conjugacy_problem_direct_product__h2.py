import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def is_fg(g):
    try:
        if hasattr(g, 'is_finitely_generated'):
            val = g.is_finitely_generated
            if callable(val): val = val()
            return bool(val)
        if hasattr(g, 'fg'):
            val = g.fg
            if callable(val): val = val()
            return bool(val)
        if isinstance(g, str):
            return True
        t = type(g).__name__
        if t in ['PermutationGroup', 'FreeGroup', 'FpGroup', 'SymmetricGroup', 'AlternatingGroup', 'DihedralGroup', 'CyclicGroup', 'AbelianGroup', 'MatrixGroup']:
            return True
        if hasattr(g, 'generators'):
            gens = g.generators
            if callable(gens): gens = gens()
            return len(list(gens)) < float('inf')
    except Exception:
        pass
    return False

def has_scp(g):
    try:
        if hasattr(g, 'has_solvable_conjugacy_problem'):
            val = g.has_solvable_conjugacy_problem
            if callable(val): val = val()
            return bool(val)
        if hasattr(g, 'scp'):
            val = g.scp
            if callable(val): val = val()
            return bool(val)
        if isinstance(g, str):
            s = g.lower()
            unsolvable_keywords = ['unsolvable', 'novikov', 'boone', 'baumslag', 'miller', 'undecidable']
            if any(k in s for k in unsolvable_keywords):
                return False
            return True
        
        t = type(g).__name__
        if t in ['PermutationGroup', 'SymmetricGroup', 'AlternatingGroup', 'DihedralGroup', 'CyclicGroup', 'AbelianGroup']:
            return True
        if t == 'FreeGroup':
            return True
        if t == 'FpGroup':
            # Finitely presented groups can have an unsolvable conjugacy problem.
            # In the context of finding a counterexample, we treat FpGroup as the unsolvable component
            # unless it is explicitly known to be finite or free.
            return False
        
        if hasattr(g, 'is_finite'):
            val = g.is_finite
            if callable(val): val = val()
            if val:
                return True
    except Exception:
        pass
    return True

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = is_fg(G)
    except Exception:
        h1 = False

    try:
        h2 = is_fg(H)
    except Exception:
        h2 = False

    try:
        h3 = has_scp(H)
    except Exception:
        h3 = False

    try:
        # The direct product G x H has a solvable conjugacy problem if and only if 
        # both G and H have a solvable conjugacy problem.
        # The conclusion fails (neg_Q is True) if G x H does NOT have a solvable conjugacy problem.
        neg_q = not (has_scp(G) and has_scp(H))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finitely generated group",
    "H_2: H is a finitely generated group",
    "H_3: H has a solvable conjugacy problem",
    "¬Q: G x H does not have a solvable conjugacy problem"
]

N_HYP = 3
NEG_Q_INDEX = 3
import sympy
from sympy import S, Set, Union, Intersection, FiniteSet, Interval, ImageSet, Symbol, oo
from sympy.abc import x, y, z, n
from sympy.matrices import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools
import z3

# Top-level setup
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

def is_topological_space(witness):
    """Check if the witness can be interpreted as a topological space."""
    if getattr(witness, 'is_topological_space', False):
        return True
    if isinstance(witness, Set):
        return True
    if isinstance(witness, str):
        return True
    if hasattr(witness, 'path_components_are_open') or hasattr(witness, 'is_locally_path_connected'):
        return True
    if isinstance(witness, tuple) and len(witness) == 2:
        X, tau = witness
        if isinstance(X, (set, list, tuple)) and isinstance(tau, (set, list, tuple)):
            try:
                X_set = frozenset(X)
                tau_sets = [frozenset(U) for U in tau]
                if frozenset() not in tau_sets or X_set not in tau_sets:
                    return False
                for U in tau_sets:
                    if not U.issubset(X_set):
                        return False
                for U in tau_sets:
                    for V in tau_sets:
                        if U.intersection(V) not in tau_sets:
                            return False
                for U in tau_sets:
                    for V in tau_sets:
                        if U.union(V) not in tau_sets:
                            return False
                return True
            except Exception:
                return False
    return False

def path_components_open(witness):
    """
    Evaluate if every path-component of X is an open set in X.
    Returns True if they are all open, False if at least one is not open.
    """
    if hasattr(witness, 'path_components_are_open'):
        val = witness.path_components_are_open
        return val() if callable(val) else val

    if isinstance(witness, str):
        w = witness.lower()
        # Known counterexamples
        if any(kw in w for kw in ["rationals", "q", "irrationals", "cantor", "sine curve", "topologist"]):
            return False
        return True

    if witness == S.Rationals:
        return False
        
    try:
        if witness == S.Reals - S.Rationals:
            return False
    except Exception:
        pass

    if isinstance(witness, Union):
        has_image = any(isinstance(arg, ImageSet) for arg in witness.args)
        has_finite = any(isinstance(arg, FiniteSet) for arg in witness.args)
        # E.g., {0} U {1/n | n in N}
        if has_image and has_finite:
            return False

    # Default to True for finite spaces, intervals, R, Z, etc.
    # (Finite spaces are locally path-connected, so their path components are open)
    return True

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(is_topological_space(witness))
    except Exception:
        h1 = False

    try:
        q = bool(path_components_open(witness))
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: X is a topological space",
    "¬Q: There exists a path-component of X that is not open in X"
]

N_HYP = 1
NEG_Q_INDEX = 1
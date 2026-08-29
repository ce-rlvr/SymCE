import sympy
from sympy import S, Interval, FiniteSet, Union, Intersection, ProductSet, ImageSet, Complement
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def is_totally_disconnected(s):
    """
    Heuristic to check if a SymPy set or object represents a totally disconnected space.
    """
    try:
        if hasattr(s, 'is_totally_disconnected'):
            val = s.is_totally_disconnected
            return val() if callable(val) else val
            
        if s == S.EmptySet:
            return True
        if isinstance(s, FiniteSet):
            return True
        if s in (S.Integers, S.Naturals, S.Naturals0, S.Rationals):
            return True
        if isinstance(s, Interval):
            return s.start == s.end
        if isinstance(s, Union):
            return all(is_totally_disconnected(arg) for arg in s.args)
        if isinstance(s, Intersection):
            return any(is_totally_disconnected(arg) for arg in s.args)
        if isinstance(s, ProductSet):
            return all(is_totally_disconnected(arg) for arg in s.args)
        if isinstance(s, ImageSet):
            return is_totally_disconnected(s.base_set)
        if isinstance(s, Complement):
            if is_totally_disconnected(s.args[0]):
                return True
            return False
            
        if type(s).__name__ in ('Point', 'Point2D', 'Point3D'):
            return True
            
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        X_i = None
        X = None
        
        # Extract the family of spaces {X_i} and the space X from the witness
        if isinstance(witness, dict):
            if 'X_i' in witness and 'X' in witness:
                X_i = witness['X_i']
                X = witness['X']
            elif 'family' in witness and 'space' in witness:
                X_i = witness['family']
                X = witness['space']
        elif hasattr(witness, 'X_i') and hasattr(witness, 'X'):
            X_i = witness.X_i() if callable(witness.X_i) else witness.X_i
            X = witness.X() if callable(witness.X) else witness.X
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            X_i, X = witness
            
        if X_i is None or X is None:
            return [False, False]
            
        # Normalize X_i to an iterable of spaces
        if isinstance(X_i, dict):
            spaces = list(X_i.values())
        elif isinstance(X_i, (list, tuple, set)):
            spaces = list(X_i)
        else:
            spaces = [X_i]
            
        # H_1: {X_i} is a family of totally disconnected topological spaces
        H1 = all(is_totally_disconnected(s) for s in spaces)
        
        # ¬Q: X is NOT a totally disconnected space
        neg_Q = not is_totally_disconnected(X)
        
        return [bool(H1), bool(neg_Q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: {X_i} is a family of totally disconnected topological spaces indexed by a set I",
    "¬Q: X is not a totally disconnected space"
]

N_HYP = 1
NEG_Q_INDEX = 1
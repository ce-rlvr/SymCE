import sympy
from sympy import eye, zeros, Rational, Float
from sympy.abc import x, y, z
from sympy.combinatorics import Permutation

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_identity(u):
    """Attempt to determine the multiplicative identity 1_R for the ring of u."""
    if hasattr(u, 'ring') and hasattr(u.ring, 'one'):
        return u.ring.one
    if hasattr(u, 'parent'):
        parent = u.parent
        if callable(parent):
            try:
                parent = parent()
            except Exception:
                pass
        if hasattr(parent, 'one'):
            return parent.one
    if getattr(u, 'is_Matrix', False):
        return eye(u.shape[0])
    if isinstance(u, Permutation):
        return Permutation()
    return 1

def check_H1(u):
    """Check if u is a unit in R."""
    try:
        # Check for explicit is_unit property/method
        if hasattr(u, 'is_unit'):
            val = u.is_unit
            if callable(val):
                return bool(val())
            return bool(val)
            
        # Matrix handling
        if getattr(u, 'is_Matrix', False):
            # If all elements are integers, it's a matrix over Z.
            # A matrix over Z is a unit iff its determinant is 1 or -1.
            is_int = True
            for val in u:
                if not (isinstance(val, int) or getattr(val, 'is_integer', False)):
                    is_int = False
                    break
            if is_int:
                det_val = u.det()
                return det_val == 1 or det_val == -1
            else:
                # Over fields or other rings, try to invert it
                u.inv()
                return True
                
        # Scalar handling
        if isinstance(u, int):
            return u in [1, -1]
            
        if isinstance(u, float):
            return u != 0.0
            
        if hasattr(u, 'is_integer') and u.is_integer:
            return u in [1, -1]
            
        # Domain elements or polynomials
        if hasattr(u, 'parent') or hasattr(u, 'ring'):
            try:
                inv = u**-1
                return True
            except Exception:
                pass
                
        # Sympy Rationals and Floats
        if isinstance(u, (Rational, Float)):
            return u != 0
            
        # General inversion fallback
        if hasattr(u, 'inv'):
            u.inv()
            return True
            
        return False
    except Exception:
        return False

def check_H2(u):
    """Check if u is an idempotent element (u^2 = u)."""
    try:
        res = (u * u == u)
        if isinstance(res, bool):
            return res
        return bool(res)
    except Exception:
        pass
    try:
        res = (u ** 2 == u)
        if isinstance(res, bool):
            return res
        return bool(res)
    except Exception:
        return False

def check_neg_Q(u):
    """Check if the conclusion fails (u != 1_R)."""
    try:
        identity = get_identity(u)
        res = (u != identity)
        if isinstance(res, bool):
            return res
        return bool(res)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    return [
        check_H1(witness),
        check_H2(witness),
        check_neg_Q(witness)
    ]

CONDITION_LABELS = [
    "H_1: u is a unit in R",
    "H_2: u is an idempotent element, meaning u^2 = u",
    "¬Q: u != 1_R"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential matrix witnesses
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def evaluate_f(witness, n):
    """
    Evaluates the arithmetic function witness at n.
    The witness can be a callable, a dictionary, a list/tuple of values,
    or just a single value representing f(1).
    """
    if callable(witness):
        return witness(n)
    elif isinstance(witness, dict):
        return witness.get(n, 0)
    elif isinstance(witness, (list, tuple)):
        if n - 1 < len(witness):
            return witness[n - 1]
        else:
            return 0
    else:
        if n == 1:
            return witness
        return 0

def is_unit(v):
    """
    Determines if a value is a unit in its respective ring.
    Defaults to assuming the ring is Z if the value is an integer.
    """
    if hasattr(v, 'det'):
        try:
            return is_unit(v.det())
        except Exception:
            return False
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, sympy.Integer)):
        return abs(v) == 1
    if isinstance(v, sympy.Rational):
        return v != 0
    if isinstance(v, float):
        return v != 0
    try:
        return abs(int(v)) == 1
    except Exception:
        pass
    try:
        return bool(v != 0)
    except Exception:
        return False

def is_nonzero(v):
    """
    Safely checks if a value is non-zero.
    """
    if hasattr(v, 'is_zero') and v.is_zero is not None:
        return not v.is_zero
    if hasattr(v, 'is_zero_matrix') and v.is_zero_matrix is not None:
        return not v.is_zero_matrix
    try:
        return bool(v != 0)
    except Exception:
        pass
    try:
        return bool(v.norm() != 0)
    except Exception:
        pass
    return True

def conditions(witness) -> list[bool]:
    try:
        v1 = evaluate_f(witness, 1)
        
        # H_1: A is the ring of arithmetic functions from the positive integers to K
        # H_2: f \in A
        # Any valid function/sequence provided as a witness trivially satisfies being in A.
        # We just verify that f(1) can be evaluated.
        h1 = True
        h2 = True
        
        # Check if f is a unit in A.
        # An arithmetic function f is a unit under Dirichlet convolution iff f(1) is a unit in K.
        f_is_unit = is_unit(v1)
        
        # Check if f(1) != 0
        f1_neq_0 = is_nonzero(v1)
        
        # Conclusion Q: f is a unit in A if and only if f(1) != 0
        q = (f_is_unit == f1_neq_0)
        
        # The conjecture is false, so we want the conclusion to fail (neg_Q = True)
        neg_q = not q
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: A is the ring of arithmetic functions from the positive integers to K",
    "H_2: f in A",
    "¬Q: f is a unit in A iff f(1) != 0 fails"
]

N_HYP = 2
NEG_Q_INDEX = 2
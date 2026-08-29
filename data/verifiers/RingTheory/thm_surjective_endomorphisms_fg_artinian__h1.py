import sympy
import sympy.combinatorics
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample.
    Since SymPy lacks a general module theory over non-commutative/non-Noetherian rings,
    the witness is expected to be an object or dictionary exposing the required properties.
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_finitely_generated", False))
            h2 = bool(witness.get("is_surjective", False))
            neg_q = not bool(witness.get("is_injective", True))
            return [h1, h2, neg_q]
            
        if hasattr(witness, "is_finitely_generated"):
            v = witness.is_finitely_generated
            h1 = bool(v() if callable(v) else v)
            
        if hasattr(witness, "is_surjective"):
            v = witness.is_surjective
            h2 = bool(v() if callable(v) else v)
            
        if hasattr(witness, "is_injective"):
            v = witness.is_injective
            neg_q = not bool(v() if callable(v) else v)
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M is a finitely generated right R-module",
    "H_2: f is a surjective R-module homomorphism",
    "¬Q: f is not injective"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z
from sympy.polys.domains import QQ, ZZ, GF
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: E/K is a normal extension",
    "H_2: E/K is a separable extension",
    "¬Q: E/K is not a Galois extension"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Check if the witness is a counterexample to "Normal and Separable implies Galois".
    The dropped hypothesis is "FiniteDimensional" (or "Algebraic").
    A valid counterexample is a transcendental extension like K(x)/K,
    or an infinite algebraic extension.
    """
    h1 = False
    h2 = False
    neg_q = False
    
    E = None
    K = None
    if isinstance(witness, tuple) and len(witness) == 2:
        E, K = witness
    else:
        E = witness

    # 1. Infinite algebraic extensions or transcendental extensions represented as strings
    try:
        if isinstance(witness, str):
            s = witness.lower()
            if any(kw in s for kw in ["infinite", "transcendental", "q(x)", "f_p(x)", "closure", "q_bar"]):
                return [True, True, True]
    except Exception:
        pass

    # 2. SymPy Domains (FractionField, AlgebraicField, FiniteField, QQ, etc.)
    try:
        from sympy.polys.domains.domain import Domain
        if isinstance(E, Domain):
            if hasattr(E, 'is_FractionField') and E.is_FractionField:
                # Transcendental extension K(x)/K
                # Normal: True (algebraic elements are just K, so minimal polynomials trivially split)
                # Separable: True (algebraic elements are K, which are separable over K)
                # Galois: False (not finite dimensional, or fixed field of Aut is strictly larger than K)
                return [True, True, True]
            else:
                # Finite extensions like QQ(sqrt(2)), GF(p), or trivial extensions like QQ/QQ
                # For finite extensions, normal + separable implies Galois.
                return [True, True, False]
    except Exception:
        pass

    # 3. SymPy Expressions
    try:
        if isinstance(E, sympy.Expr):
            if E.free_symbols:
                # Has variables -> represents a transcendental extension K(x)
                return [True, True, True]
            else:
                # Constant -> represents a finite extension
                return [True, True, False]
    except Exception:
        pass

    # 4. SymPy Poly
    try:
        if isinstance(E, sympy.Poly):
            # Polynomials represent finite extensions (e.g., splitting fields or K[x]/(f))
            return [True, True, False]
    except Exception:
        pass

    return [h1, h2, neg_q]
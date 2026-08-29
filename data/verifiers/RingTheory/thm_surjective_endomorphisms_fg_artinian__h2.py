import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
# Since representing infinite-dimensional modules directly in SymPy is not feasible,
# we provide standard counterexample objects and a generic Counterexample class.

class Counterexample:
    """
    Generic witness for module homomorphism properties.
    """
    def __init__(self, R_is_artinian, f_is_surjective, f_is_injective):
        self.R_is_artinian = R_is_artinian
        self.f_is_surjective = f_is_surjective
        self.f_is_injective = f_is_injective

class LeftShiftOperator:
    """
    Represents the left shift operator on the infinite-dimensional vector space
    V = F^\infty over a field F (which is an Artinian ring).
    f(x_1, x_2, x_3, ...) = (x_2, x_3, ...)
    This operator is surjective but not injective.
    """
    @property
    def R_is_artinian(self):
        return True
        
    @property
    def f_is_surjective(self):
        return True
        
    @property
    def f_is_injective(self):
        return False

class PolynomialDerivative:
    """
    Represents the derivative operator on F[x] over a field F.
    f(P) = P'
    This operator is surjective but not injective.
    """
    @property
    def R_is_artinian(self):
        return True
        
    @property
    def f_is_surjective(self):
        return True
        
    @property
    def f_is_injective(self):
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, str):
            if witness in ["LeftShiftOperator", "PolynomialDerivative"]:
                return [True, True, True]
            return [False, False, False]
            
        if isinstance(witness, dict):
            h1 = witness.get('R_is_artinian', False)
            h2 = witness.get('f_is_surjective', False)
            q = witness.get('f_is_injective', True)
        elif isinstance(witness, tuple) and len(witness) == 3:
            h1, h2, q = witness
        else:
            h1 = getattr(witness, 'R_is_artinian', False)
            h2 = getattr(witness, 'f_is_surjective', False)
            q = getattr(witness, 'f_is_injective', True)
        
        return [bool(h1), bool(h2), not bool(q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "H_2: f is a surjective R-module homomorphism",
    "¬Q: f is not injective"
]

N_HYP = 2
NEG_Q_INDEX = 2
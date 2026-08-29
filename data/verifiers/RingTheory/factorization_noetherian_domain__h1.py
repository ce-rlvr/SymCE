import sympy
from sympy import Rational
import math
import itertools
import functools

# Top-level setup
class PuiseuxMonomial:
    """
    Represents an element c * x^q in the ring F[x^{Q_{>=0}}].
    This ring is a non-Noetherian domain where no element with q > 0
    can be factored into a finite product of irreducibles.
    """
    def __init__(self, c, q):
        self.c = c
        self.q = Rational(q)
        
    def is_zero(self):
        return self.c == 0
        
    def is_unit(self):
        return self.c != 0 and self.q == 0
        
    def has_finite_irreducible_factorization(self):
        if self.is_zero() or self.is_unit():
            return True
        return False

class RingElement:
    """
    A generic mock object for the caller's convenience to represent
    an element in an arbitrary ring.
    """
    def __init__(self, zero=False, unit=False, finite_factors=True):
        self._zero = zero
        self._unit = unit
        self._finite_factors = finite_factors
        
    def is_zero(self): return self._zero
    def is_unit(self): return self._unit
    def has_finite_irreducible_factorization(self): return self._finite_factors


def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            is_z = witness.get('is_zero', False)
            is_u = witness.get('is_unit', False)
            h1 = bool(not is_z and not is_u)
            
            fin_fact = True
            for key in ['has_finite_irreducible_factorization', 
                        'is_finite_product_of_irreducibles',
                        'factors_into_irreducibles',
                        'finite_factorization']:
                if key in witness:
                    fin_fact = bool(witness[key])
                    break
            neg_q = not fin_fact
            return [h1, neg_q]
            
        # Object with methods/attributes
        if hasattr(witness, 'is_zero'):
            is_z = witness.is_zero() if callable(witness.is_zero) else witness.is_zero
        else:
            is_z = (witness == 0)
            
        if hasattr(witness, 'is_unit'):
            is_u = witness.is_unit() if callable(witness.is_unit) else witness.is_unit
        else:
            try:
                is_u = (abs(witness) == 1)
            except Exception:
                is_u = False
                
        h1 = bool(not is_z and not is_u)
    except Exception:
        h1 = False

    try:
        fin_fact = True
        found_attr = False
        for attr in ['has_finite_irreducible_factorization', 
                     'is_finite_product_of_irreducibles',
                     'factors_into_irreducibles',
                     'finite_factorization']:
            if hasattr(witness, attr):
                val = getattr(witness, attr)
                fin_fact = val() if callable(val) else val
                found_attr = True
                break
        
        if not found_attr:
            # Fallback for standard types (int, sympy Expr) which are in UFDs
            fin_fact = True
            
        neg_q = not fin_fact
    except Exception:
        neg_q = False

    return [h1, neg_q]


CONDITION_LABELS = [
    "H_1: a is a non-zero non-unit element in R",
    "¬Q: a cannot be written as a finite product of irreducible elements"
]

N_HYP = 1
NEG_Q_INDEX = 1
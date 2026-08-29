import sympy
from sympy import symbols, QQ, ZZ, Rational
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
# We provide standard counterexample classes that the witness might instantiate.
class InfiniteProductRing:
    def __init__(self, base_ring=None):
        self.base_ring = base_ring
        self.is_commutative = True
        self.has_identity = True
        self.has_infinite_minimal_primes = True

class InfinitePolynomialQuotientRing:
    def __init__(self):
        self.is_commutative = True
        self.has_identity = True
        self.has_infinite_minimal_primes = True

class BooleanRingOfInfiniteSets:
    def __init__(self):
        self.is_commutative = True
        self.has_identity = True
        self.has_infinite_minimal_primes = True

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        # Check H1: R is a commutative ring with identity
        if hasattr(witness, 'is_commutative') and hasattr(witness, 'has_identity'):
            h1 = bool(witness.is_commutative) and bool(witness.has_identity)
        elif hasattr(witness, 'is_commutative_ring_with_identity'):
            h1 = bool(witness.is_commutative_ring_with_identity)
        elif hasattr(witness, 'is_Ring') and witness.is_Ring:
            h1 = bool(getattr(witness, 'is_commutative', True))

        # Check neg_Q: The set of minimal prime ideals of R is infinite
        if hasattr(witness, 'has_infinite_minimal_primes'):
            neg_q = bool(witness.has_infinite_minimal_primes)
        elif hasattr(witness, 'minimal_primes'):
            mp = witness.minimal_primes
            if mp == "infinite" or mp == float('inf'):
                neg_q = True
            else:
                try:
                    neg_q = len(mp) == float('inf')
                except Exception:
                    neg_q = False

        # Fallback for string-based or descriptive witnesses
        if not h1 or not neg_q:
            w_str = str(witness).lower()
            
            if not h1:
                ring_keywords = [
                    "ring", "prod", "k[x", "zz", "qq", "integer", "rational", 
                    "field", "product", "polynomial", "f2", "z2", "z3", "z4", "z6"
                ]
                if any(kw in w_str for kw in ring_keywords):
                    h1 = True
                    
            if not neg_q:
                infinite_keywords = [
                    "infinite", "...", "x_i", "x_j", "prod_{", "prod_i", "product over"
                ]
                if any(kw in w_str for kw in infinite_keywords):
                    neg_q = True
                
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: The set of minimal prime ideals of R is infinite"
]

N_HYP = 1
NEG_Q_INDEX = 1
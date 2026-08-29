import sympy
from sympy import QQ, ZZ, Rational, Integer
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup: Mock classes for non-Noetherian rings and ideals
# Since finite rings and finitely generated algebras over fields/Z are Noetherian,
# and in Noetherian rings every ideal is decomposable (thus having minimal associated primes),
# any valid counterexample must be an infinite, non-Noetherian ring.
# SymPy does not natively support infinite polynomial rings or general non-Noetherian rings,
# so we provide a mock framework for the witness to express the counterexample's properties.

class Ring:
    """
    Mock class for a commutative ring.
    """
    def __init__(self, commutative=True, identity=True):
        self.is_commutative = commutative
        self.has_identity = identity

class Ideal:
    """
    Mock class for an ideal in a ring.
    """
    def __init__(self, is_prime=False, minimal_associated_primes=None, contains=None):
        self.is_prime = is_prime
        self._min_assoc = minimal_associated_primes if minimal_associated_primes is not None else []
        self._contains = contains if contains is not None else []

    def is_subset(self, other):
        if self is other:
            return True
        if hasattr(other, '_contains') and self in other._contains:
            return True
        if hasattr(other, 'contains') and self in other.contains:
            return True
        return False

    def minimal_associated_primes(self):
        return self._min_assoc


def conditions(witness) -> list[bool]:
    try:
        # The witness is expected to be a tuple: (Ring, Ideal_I, Ideal_P)
        R, I, P = witness
        
        # H_1: R is a commutative ring with identity
        is_comm = R.is_commutative() if callable(getattr(R, 'is_commutative', None)) else getattr(R, 'is_commutative', False)
        has_id = R.has_identity() if callable(getattr(R, 'has_identity', None)) else getattr(R, 'has_identity', False)
        H1 = bool(is_comm and has_id)
        
        # H_2: P is a prime ideal of R containing I
        is_prime = P.is_prime() if callable(getattr(P, 'is_prime', None)) else getattr(P, 'is_prime', False)
        
        if hasattr(I, 'is_subset'):
            i_sub_p = I.is_subset(P)
        elif hasattr(P, 'contains'):
            i_sub_p = P.contains(I) if callable(P.contains) else I in P.contains
        elif hasattr(P, '_contains'):
            i_sub_p = I in P._contains
        else:
            i_sub_p = False
            
        H2 = bool(is_prime and i_sub_p)
        
        # ¬Q: P does NOT contain any minimal associated prime ideal of I
        if hasattr(I, 'minimal_associated_primes'):
            min_assoc = I.minimal_associated_primes() if callable(I.minimal_associated_primes) else I.minimal_associated_primes
        else:
            # If we cannot determine the minimal associated primes, we cannot verify the counterexample.
            raise ValueError("minimal_associated_primes not found on ideal I")
            
        neg_Q = True
        for p in min_assoc:
            if hasattr(p, 'is_subset'):
                p_sub_P = p.is_subset(P)
            elif hasattr(P, 'contains'):
                p_sub_P = P.contains(p) if callable(P.contains) else p in P.contains
            elif hasattr(P, '_contains'):
                p_sub_P = p in P._contains
            else:
                p_sub_P = False
                
            if p_sub_P:
                neg_Q = False
                break
                
    except Exception:
        return [False, False, False]
        
    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: P is a prime ideal of R containing I",
    "¬Q: P does not contain any minimal associated prime ideal of I"
]

N_HYP = 2
NEG_Q_INDEX = 2
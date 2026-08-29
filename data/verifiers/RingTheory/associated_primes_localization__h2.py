import sympy
from sympy import symbols, QQ, ZZ
import math
import itertools
import functools

# Top-level setup
x, y, z = symbols('x y z')

class NonNoetherianWitness:
    """
    A witness class for non-Noetherian ring counterexamples.
    Since SymPy only supports Noetherian rings (e.g. polynomial rings in finitely many variables),
    this class allows representing a counterexample symbolically.
    """
    def __init__(self, is_commutative_ring_with_identity=True, is_module=True, 
                 is_multiplicatively_closed=True, associated_primes_bijection=False):
        self.is_commutative_ring_with_identity = is_commutative_ring_with_identity
        self.is_module = is_module
        self.is_multiplicatively_closed = is_multiplicatively_closed
        self.associated_primes_bijection = associated_primes_bijection

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_commutative_ring_with_identity", False))
            h2 = bool(witness.get("is_module", False))
            h3 = bool(witness.get("is_multiplicatively_closed", False))
            neg_q = not bool(witness.get("associated_primes_bijection", True))
        else:
            h1 = bool(witness.is_commutative_ring_with_identity)
            h2 = bool(witness.is_module)
            h3 = bool(witness.is_multiplicatively_closed)
            neg_q = not bool(witness.associated_primes_bijection)
    except Exception:
        return [False, False, False, False]
    
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: M is an R-module",
    "H_3: S is a multiplicatively closed subset of R",
    "¬Q: The set of associated primes of S^{-1}M does not correspond bijectively to the set of associated primes of M disjoint from S"
]

N_HYP = 3
NEG_Q_INDEX = 3
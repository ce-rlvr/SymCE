import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.polys.domains import ZZ, QQ, EX
from sympy.abc import x, y, z
import sympy.ntheory
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
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

def is_krull_domain(R):
    """
    Evaluates whether the given ring R is a Krull domain.
    Returns False if it can be determined that R is NOT a Krull domain.
    Returns True otherwise (as a safe fallback so we only accept definitive counterexamples).
    """
    if hasattr(R, 'is_Krull'):
        return R.is_Krull
    
    if getattr(R, 'is_Matrix', False):
        return False
        
    if getattr(R, 'is_IntegralDomain', None) is False:
        return False
        
    if hasattr(R, 'base_ideal'):
        try:
            if not R.base_ideal.is_prime():
                return False
            # Check for specific known non-integrally closed domains (e.g. cuspidal cubic)
            gens = R.base_ideal.gens
            if len(gens) == 1:
                f = gens[0].as_expr()
                s = str(f).replace(" ", "")
                if "x**3-y**2" in s or "y**2-x**3" in s or "x**2-y**3" in s or "y**3-x**2" in s:
                    return False
        except Exception:
            pass
            
    # If the witness is provided as a cyclic group Z_n acting as the ring Z/nZ
    if hasattr(R, 'order'):
        try:
            n = R.order()
            if not sympy.ntheory.isprime(n):
                return False
        except Exception:
            pass
            
    if getattr(R, 'is_Field', False):
        return True
        
    if getattr(R, 'is_UFD', False):
        return True
        
    return True

def conditions(witness) -> list[bool]:
    try:
        # The conjecture is "R is a Krull domain".
        # We want neg_q to be True when the conjecture FAILS (i.e., R is NOT a Krull domain).
        neg_q = not is_krull_domain(witness)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R is not a Krull domain"
]

N_HYP = 0
NEG_Q_INDEX = 0
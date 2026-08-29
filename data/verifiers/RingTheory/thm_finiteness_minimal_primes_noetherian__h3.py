import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard algebra objects
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Witness could be a tuple (R, I) or just a ring R
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        else:
            R = witness
            I = None
            
        if isinstance(R, dict):
            h1 = bool(R.get('is_commutative_ring_with_identity', 
                      R.get('is_commutative', False) and R.get('has_identity', False)))
            h2 = bool(R.get('is_Noetherian', False))
            neg_q = bool(R.get('has_infinitely_many_minimal_primes_over_I', 
                         R.get('has_infinitely_many_minimal_primes', False)))
        else:
            # H_1: R is a commutative ring with identity
            if hasattr(R, 'is_commutative_ring_with_identity'):
                h1 = bool(R.is_commutative_ring_with_identity)
            else:
                h1 = bool(getattr(R, 'is_commutative', False) and getattr(R, 'has_identity', False))
                
            # H_2: R is a Noetherian ring
            h2 = bool(getattr(R, 'is_Noetherian', False))
                
            # ¬Q: There are infinitely many minimal prime ideals over I
            if hasattr(R, 'has_infinitely_many_minimal_primes_over_I'):
                neg_q = bool(R.has_infinitely_many_minimal_primes_over_I)
            elif hasattr(R, 'has_infinitely_many_minimal_primes'):
                neg_q = bool(R.has_infinitely_many_minimal_primes)
            elif hasattr(R, 'has_infinitely_many_minimal_primes_over'):
                neg_q = bool(R.has_infinitely_many_minimal_primes_over(I))
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R is a Noetherian ring",
    "¬Q: There are infinitely many minimal prime ideals over I"
]

N_HYP = 2
NEG_Q_INDEX = 2
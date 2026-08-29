import math
import sympy
from sympy import symbols
import sympy.combinatorics
import sympy.matrices

# Top-level setup
class InfiniteProductRing:
    """
    A mock commutative ring with identity that has infinitely many minimal prime ideals
    over the zero ideal. Represents an infinite direct product of fields.
    """
    is_commutative = True
    has_identity = True
    
    class ideal:
        is_proper = True
        
    minimal_prime_ideals_count = math.inf

# Standard algebra objects
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

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        else:
            R = witness
            I = getattr(witness, 'ideal', None) or getattr(witness, 'I', None)
            
        # H1: R is a commutative ring with identity
        is_comm = getattr(R, 'is_commutative', False) or getattr(R, 'is_Commutative', False)
        has_id = getattr(R, 'has_identity', False) or getattr(R, 'has_Identity', False)
        if is_comm and has_id:
            h1 = True
            
        # H2: I is a proper ideal of R
        if I is not None:
            if hasattr(I, 'is_proper'):
                h2 = bool(getattr(I, 'is_proper'))
            else:
                h2 = True
        elif hasattr(R, 'is_proper'):
            h2 = bool(getattr(R, 'is_proper'))
        elif R is InfiniteProductRing or isinstance(R, InfiniteProductRing):
            h2 = True
            
        # neg_Q: infinitely many minimal prime ideals over I
        if hasattr(R, 'minimal_prime_ideals_count'):
            val = R.minimal_prime_ideals_count
            if callable(val):
                try:
                    val = val(I)
                except Exception:
                    val = val()
            if val == math.inf or val == float('inf'):
                neg_q = True
        elif hasattr(R, 'has_infinite_minimal_primes'):
            neg_q = bool(getattr(R, 'has_infinite_minimal_primes'))
        elif R is InfiniteProductRing or isinstance(R, InfiniteProductRing):
            neg_q = True
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I is a proper ideal of R",
    "¬Q: There are infinitely many minimal prime ideals over I"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
class MatrixRing:
    """Represents the ring of n x n matrices over a base ring."""
    def __init__(self, base_ring, n):
        self.base_ring = base_ring
        self.n = n

class UpperTriangularMatrixRing:
    """Represents the ring of n x n upper triangular matrices over a base ring."""
    def __init__(self, base_ring, n):
        self.base_ring = base_ring
        self.n = n

class QuaternionRing:
    """Represents a quaternion ring over a base ring."""
    def __init__(self, base_ring):
        self.base_ring = base_ring

def conditions(witness) -> list[bool]:
    try:
        h1_ok = False
        neg_q = False
        
        # H_1: Let F be the family of all surjective ring homomorphisms from R to fields.
        # This is a definitional hypothesis, so it holds as long as the witness is a valid ring.
        if isinstance(witness, (MatrixRing, UpperTriangularMatrixRing, QuaternionRing)):
            h1_ok = True
        elif isinstance(witness, str):
            h1_ok = True
        elif hasattr(witness, 'is_Ring') and witness.is_Ring:
            h1_ok = True
        elif witness in [sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes]:
            h1_ok = True
        elif hasattr(witness, 'get_ring') or hasattr(witness, 'domain'):
            h1_ok = True
            
        if not h1_ok:
            return [False, False]
            
        # ¬Q: The intersection of the kernels of all homomorphisms in F is NOT the Jacobson radical of R.
        # For commutative rings, the intersection of kernels to fields is exactly the intersection 
        # of all maximal ideals, which IS the Jacobson radical. Thus, the conjecture holds (neg_Q = False).
        # For non-commutative simple rings (like M_n(K) for n >= 2, or Quaternions), the Jacobson radical is {0}.
        # However, there are no surjective homomorphisms to commutative fields, so F is empty.
        # The intersection of an empty family of ideals is the whole ring R != {0}. Thus, the conjecture fails (neg_Q = True).
        if isinstance(witness, MatrixRing):
            if witness.n >= 2:
                neg_q = True
            else:
                neg_q = False
        elif isinstance(witness, UpperTriangularMatrixRing):
            # R/J(R) is commutative, so the intersection of kernels equals J(R).
            neg_q = False
        elif isinstance(witness, QuaternionRing):
            neg_q = True
        elif isinstance(witness, str):
            w = witness.lower()
            if 'upper' in w and 'triangular' in w:
                neg_q = False
            elif 'matrix' in w or 'm2' in w or 'm_2' in w or 'm3' in w or 'm_3' in w or 'm_n' in w:
                neg_q = True
            elif 'quaternion' in w or w == 'h':
                neg_q = True
            elif 'weyl' in w or 'free' in w:
                neg_q = True
            else:
                neg_q = False
        else:
            # Default to commutative behavior for standard SymPy domains (ZZ, QQ, etc.)
            neg_q = False
            
    except Exception:
        h1_ok = False
        neg_q = False
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: F is the family of all surjective ring homomorphisms from R to fields",
    "¬Q: The intersection of the kernels of all homomorphisms in F is not the Jacobson radical of R"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
from sympy import Matrix, eye, zeros

class MatrixRingOverField:
    """
    Represents the ring of n x n matrices over a field (e.g., QQ or RR).
    In this non-commutative ring, the only two-sided ideals are {0} and the whole ring.
    Thus, the unique maximal ideal is the zero ideal.
    """
    def __init__(self, n):
        self.n = n
        
    def __contains__(self, a):
        try:
            return hasattr(a, 'is_Matrix') and a.is_Matrix and a.shape == (self.n, self.n)
        except Exception:
            return False
            
    def is_unit(self, a):
        return a.det() != 0
        
    def in_maximal_ideal(self, a):
        return a.is_zero_matrix

class MultipleIntegersRing:
    """
    Represents the commutative ring without identity nZ.
    The maximal ideals are of the form p*nZ for prime p.
    An element a in nZ is in a maximal ideal iff a/n has a prime factor.
    """
    def __init__(self, n):
        self.n = abs(int(n))
        
    def __contains__(self, a):
        try:
            return int(a) % self.n == 0
        except Exception:
            return False
            
    def is_unit(self, a):
        # A ring without identity has no units
        return False
        
    def in_maximal_ideal(self, a):
        if a == 0:
            return True
        # a is in p*nZ iff a/n is divisible by p.
        # So a is in some maximal ideal iff a/n is not 1 or -1.
        return abs(int(a) // self.n) > 1

# Top-level setup: named object bindings that the witness expression may reference.
M2_QQ = MatrixRingOverField(2)
M3_QQ = MatrixRingOverField(3)
Z_even = MultipleIntegersRing(2)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion at the witness.
    The witness can be a tuple (R, a) or just the element a (from which R is inferred).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, a = witness
        else:
            a = witness
            # Infer the ring if only the element is provided
            if hasattr(a, 'is_Matrix') and a.is_Matrix and a.shape[0] == a.shape[1]:
                R = MatrixRingOverField(a.shape[0])
            else:
                try:
                    val = int(a)
                    # For integers 0, 1, -1, the theorem holds in their respective generated rings.
                    if val == 0 or abs(val) == 1:
                        return [False, False]
                    R = MultipleIntegersRing(abs(val))
                except Exception:
                    return [False, False]
                    
        # H_1: a is an element of R
        h1 = (a in R)
        
        # Evaluate properties
        is_unit = R.is_unit(a)
        in_max_ideal = R.in_maximal_ideal(a)
        
        # Conclusion Q: a is a unit iff a is not contained in any maximal ideal.
        # Negated conclusion ¬Q: (a is a unit) is equivalent to (a is contained in a maximal ideal).
        neg_q = (bool(is_unit) == bool(in_max_ideal))
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: a is an element of R",
    "¬Q: The equivalence between being a unit and not being in any maximal ideal fails"
]

N_HYP = 1
NEG_Q_INDEX = 1
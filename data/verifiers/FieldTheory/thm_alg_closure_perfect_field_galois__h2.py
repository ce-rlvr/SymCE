import sympy
import sympy.combinatorics
import sympy.matrices
from sympy.polys.domains import QQ, ZZ, RR, CC, FF
from sympy.abc import x, y, z, t

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

# Alias for finite fields
GF = FF

def is_perfect_field(F):
    """
    Checks if a given SymPy domain represents a perfect field.
    """
    try:
        if not getattr(F, 'is_Field', False):
            return False
        
        char = F.characteristic()
        if char == 0:
            return True
            
        cls_name = F.__class__.__name__
        if 'FiniteField' in cls_name or 'GaloisField' in cls_name:
            return True
            
        if 'FractionField' in cls_name or getattr(F, 'is_FractionField', False):
            # A fraction field over a field of characteristic p > 0 is not perfect
            return False
            
        if 'AlgebraicField' in cls_name or getattr(F, 'is_AlgebraicField', False):
            return is_perfect_field(F.domain)
            
        return False
    except Exception:
        return False

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    """
    try:
        h1 = is_perfect_field(witness)
    except Exception:
        h1 = False
        
    try:
        # The algebraic closure of a field F is a Galois extension of F
        # if and only if F is a perfect field.
        if not getattr(witness, 'is_Field', False):
            q = False
        else:
            q = is_perfect_field(witness)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a perfect field",
    "¬Q: The field extension \\overline{F}/F is not a Galois extension"
]

N_HYP = 1
NEG_Q_INDEX = 1
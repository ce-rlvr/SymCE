import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
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

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "In a finite-dimensional algebra A over k, every non-unit is a zero divisor."
    
    The dropped hypothesis is that k is a field. If k is just a commutative ring 
    (like Z), the theorem fails. For example, A = Z is a finite-dimensional 
    algebra over k = Z, and x = 2 is neither a unit nor a zero divisor.
    """
    try:
        if isinstance(witness, bool):
            return [False, False, False]
            
        # Case 1: Witness is an element of A = Z (finite-dimensional algebra over k = Z)
        if isinstance(witness, (int, sympy.Integer)):
            h1 = True
            h2 = abs(witness) != 1
            is_zd = (witness == 0)
            neg_q = not is_zd
            return [h1, h2, neg_q]
            
        # Case 2: Witness is an element of A = M_n(Z) or M_n(k)
        elif isinstance(witness, sympy.Matrix):
            if witness.rows != witness.cols:
                return [False, False, False]
            h1 = True
            
            is_integer_matrix = all(isinstance(val, (int, sympy.Integer)) for val in witness)
            d = witness.det()
            
            if is_integer_matrix:
                # In M_n(Z), a matrix is a unit iff its determinant is 1 or -1
                is_unit = (abs(d) == 1)
            else:
                # If over a field, it's a unit iff determinant is non-zero
                is_unit = (d != 0)
                
            h2 = not is_unit
            
            # Over an integral domain, a matrix is a zero divisor iff its determinant is 0
            is_zd = (d == 0)
            neg_q = not is_zd
            
            return [h1, h2, neg_q]
            
        # Case 3: Witness is an element of A = Z^n (product ring)
        elif isinstance(witness, (tuple, list)) and len(witness) > 0 and all(isinstance(v, (int, sympy.Integer)) for v in witness):
            h1 = True
            is_unit = all(abs(v) == 1 for v in witness)
            h2 = not is_unit
            is_zd = any(v == 0 for v in witness)
            neg_q = not is_zd
            return [h1, h2, neg_q]
            
        else:
            return [False, False, False]
            
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: A is a finite-dimensional algebra over k",
    "H_2: x is not a unit in A",
    "¬Q: x is neither a left nor a right zero divisor in A"
]

N_HYP = 2
NEG_Q_INDEX = 2
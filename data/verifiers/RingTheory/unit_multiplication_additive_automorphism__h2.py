import math
from sympy import Integer, Rational, Float, Matrix, eye, zeros
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

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample.
    The witness is expected to represent an element u in a ring R.
    Supported witness formats:
      - int or sympy.Integer: represents u in the ring of integers Z.
      - float, sympy.Rational, sympy.Float: represents u in the field of rationals Q.
      - tuple (n, u): represents u in the ring of integers modulo n (Z_n).
      - sympy.Matrix: represents u in a matrix ring.
    """
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, (int, Integer)) and not isinstance(witness, bool):
            h1 = True
            # In Z, L_u is an automorphism iff u is 1 or -1
            is_auto = (abs(int(witness)) == 1)
            neg_q = not is_auto
            
        elif isinstance(witness, (float, Rational, Float)) and not isinstance(witness, bool):
            h1 = True
            # In Q (or R), L_u is an automorphism iff u != 0
            is_auto = (witness != 0)
            neg_q = not is_auto
            
        elif isinstance(witness, tuple) and len(witness) == 2:
            n, u = witness
            if isinstance(n, (int, Integer)) and not isinstance(n, bool) and \
               isinstance(u, (int, Integer)) and not isinstance(u, bool) and n > 0:
                h1 = True
                # In Z_n, L_u is an automorphism iff gcd(u, n) == 1
                is_auto = (math.gcd(int(u) % int(n), int(n)) == 1)
                neg_q = not is_auto
                
        elif isinstance(witness, Matrix):
            if witness.is_square:
                h1 = True
                # Check if it's an integer matrix or rational/float matrix
                is_int_matrix = all(getattr(x, 'is_integer', False) or isinstance(x, (int, Integer)) for x in witness)
                det = witness.det()
                if is_int_matrix:
                    # In M_k(Z), L_u is an automorphism iff det(u) is 1 or -1
                    is_auto = (abs(det) == 1)
                else:
                    # In M_k(Q), L_u is an automorphism iff det(u) != 0
                    is_auto = (det != 0)
                neg_q = not is_auto
                
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring with identity",
    "¬Q: The left multiplication map L_u(x) = ux is not a group automorphism of (R, +)"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
    h1 = False
    neg_q = False
    
    try:
        # Case 1: Witness is a tuple (n, x) representing the ring Z/nZ and an element x
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            n, x = witness
            if isinstance(n, (int, sympy.Integer)) and n >= 2 and isinstance(x, (int, sympy.Integer)):
                h1 = True
                n = int(n)
                x = int(x) % n
                
                ann_x = set()
                for y in range(n):
                    if (x * y) % n == 0:
                        ann_x.add(y)
                        
                ideal_1_minus_x = set()
                for y in range(n):
                    ideal_1_minus_x.add((y * (1 - x)) % n)
                    
                neg_q = ann_x != ideal_1_minus_x
                return [h1, neg_q]
    except Exception:
        pass

    try:
        # Case 2: Witness is a Sympy Matrix (representing an element in a matrix ring)
        if hasattr(witness, 'is_zero_matrix'):
            h1 = True
            is_zero = witness.is_zero_matrix
            if witness.rows == witness.cols:
                is_one = (witness == sympy.eye(witness.rows))
            else:
                is_one = False
            
            # In a matrix ring, Ann(M) == <I - M> generally holds only for O and I
            neg_q = not (is_zero or is_one)
            return [h1, neg_q]
    except Exception:
        pass

    try:
        # Case 3: Witness is a general element (assuming an integral domain like Z, R, C, or polynomials)
        if isinstance(witness, (int, float, complex, sympy.Expr)):
            h1 = True
            
            if hasattr(witness, 'is_zero') and witness.is_zero is not None:
                is_zero = bool(witness.is_zero)
            else:
                is_zero = bool(witness == 0)
                
            if hasattr(witness, 'is_one') and witness.is_one is not None:
                is_one = bool(witness.is_one)
            else:
                is_one = bool(witness == 1)
                
            # In an integral domain, Ann(x) == <1 - x> iff x == 0 or x == 1
            neg_q = not (is_zero or is_one)
            return [h1, neg_q]
    except Exception:
        pass

    return [False, False]

CONDITION_LABELS = [
    "H_1: x is an element of R",
    "¬Q: Ann(x) != <1 - x>"
]

N_HYP = 1
NEG_Q_INDEX = 1
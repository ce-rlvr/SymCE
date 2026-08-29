import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
import math

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a ring with identity",
    "H_2: I is a nilpotent two-sided ideal of R",
    "H_3: x is an element of R",
    "¬Q: x is not a unit in R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        # Helper to check if the witness is a matrix (assuming R is a matrix ring and I is the zero ideal)
        def check_matrix(x_mat):
            if not x_mat.is_square:
                return [False, False, False, False]
            h1_ok = True  # Matrix ring over Z is a ring with identity
            h2_ok = True  # The zero ideal is a nilpotent two-sided ideal
            h3_ok = True  # x is an element of the matrix ring
            
            det = x_mat.det()
            if det == 0:
                neg_q_ok = True
            else:
                # Over Z, a matrix is a unit iff its determinant is 1 or -1
                if all(isinstance(val, int) or (hasattr(val, 'is_Integer') and val.is_Integer) for val in x_mat):
                    neg_q_ok = abs(det) != 1
                else:
                    neg_q_ok = False
            return [h1_ok, h2_ok, h3_ok, neg_q_ok]

        # 1. Check if witness is a matrix directly
        if hasattr(witness, 'is_Matrix') and witness.is_Matrix:
            return check_matrix(witness)
            
        # 2. Check if witness is a tuple containing a matrix
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3 and hasattr(witness[2], 'is_Matrix') and witness[2].is_Matrix:
                return check_matrix(witness[2])
            if len(witness) == 1 and hasattr(witness[0], 'is_Matrix') and witness[0].is_Matrix:
                return check_matrix(witness[0])

        # 3. Parse witness as integers representing R = Z/nZ, I = (a), x = x
        if isinstance(witness, dict):
            n = witness.get('n', witness.get('R', 0))
            a = witness.get('a', witness.get('I', 0))
            x = witness.get('x', witness.get('value', 0))
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                n, a, x = witness
            elif len(witness) == 1:
                n, a, x = 0, 0, witness[0]
            else:
                return [False, False, False, False]
        else:
            n, a, x = 0, 0, witness
            
        if n == sympy.S.Integers:
            n = 0
            
        n = int(n)
        a = int(a)
        x = int(x)
        
        # H_1: R is a ring with identity (Z if n=0, or Z/nZ if n>=2)
        h1_ok = (n == 0 or n >= 2)
        
        # H_2: I is a nilpotent two-sided ideal of R
        h2_ok = False
        if h1_ok:
            if n == 0:
                # In Z, the only nilpotent ideal is the zero ideal
                h2_ok = (a == 0)
            else:
                # In Z/nZ, ideal (a) is nilpotent iff every prime factor of n divides a
                factors = factorint(n)
                h2_ok = all(a % p == 0 for p in factors)
                
        # H_3: x is an element of R
        h3_ok = True
        
        # ¬Q: x is not a unit in R
        if n == 0:
            # In Z, units are 1 and -1
            neg_q_ok = abs(x) != 1
        else:
            # In Z/nZ, x is a unit iff gcd(x, n) == 1
            neg_q_ok = math.gcd(x, n) != 1
            
        return [h1_ok, h2_ok, h3_ok, neg_q_ok]
    except Exception:
        return [False, False, False, False]
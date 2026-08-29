import sympy
from sympy import symbols, Rational, Integer, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

# Group theory
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

# Linear algebra
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

# Ring/Field
x, y, z = symbols('x y z')

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The conclusion is mathematically always true for Noetherian commutative rings, 
    so neg_Q will evaluate to False for any valid witness.
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Case 1: witness is an integer n, representing R = ZZ, I = (n)
        if isinstance(witness, (int, Integer)):
            n = int(witness)
            h1 = True
            h2 = (abs(n) != 1)
            neg_q = False
            return [h1, h2, neg_q]
            
        # Case 2: witness is a SymPy Ideal object
        if hasattr(witness, 'ring') and hasattr(witness, 'gens'):
            R = witness.ring
            I = witness.gens
            if hasattr(R, 'is_commutative'):
                h1 = bool(R.is_commutative)
            else:
                h1 = True
            h2 = (1 not in I)
            neg_q = False
            return [h1, h2, neg_q]

        # Case 3: witness is a tuple (R, I)
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            
            # Subcase 3a: R and I are integers, representing R = Z/nZ, I = (d)
            if isinstance(R, (int, Integer)) and isinstance(I, (int, Integer)):
                n, d = int(R), int(I)
                if n > 1:
                    h1 = True
                    g = math.gcd(d, n)
                    h2 = (g != 1)
                    neg_q = False
                return [h1, h2, neg_q]
            
            # Subcase 3b: R is a SymPy ring, I is a list of generators or an element
            if hasattr(R, 'is_commutative'):
                h1 = bool(R.is_commutative)
            elif R == sympy.ZZ:
                h1 = True
                
            if isinstance(I, list):
                if R == sympy.ZZ:
                    try:
                        g = int(I[0])
                        for val in I[1:]:
                            g = math.gcd(g, int(val))
                        h2 = (abs(g) != 1)
                    except Exception:
                        h2 = (1 not in I)
                else:
                    h2 = (1 not in I)
            elif isinstance(I, (int, Integer)):
                h2 = (abs(int(I)) != 1)
            else:
                h2 = True
                
            neg_q = False
            return [h1, h2, neg_q]
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Noetherian commutative ring",
    "H_2: I is a proper ideal of R",
    "¬Q: There does not exist a positive integer m such that the product (P_1 P_2 \\cdots P_k)^m is contained in I"
]

N_HYP = 2
NEG_Q_INDEX = 2
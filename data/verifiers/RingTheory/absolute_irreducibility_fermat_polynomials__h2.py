import sympy
import sympy.combinatorics
import sympy.matrices

S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, K = witness
        else:
            return [False, False, False]
            
        if hasattr(K, 'characteristic'):
            char_K = K.characteristic()
        elif isinstance(K, int):
            char_K = K
        else:
            char_K = None
            
        h1 = isinstance(n, int) and n >= 3
        
        if char_K is None:
            h2 = False
        elif char_K == 0:
            h2 = True
        else:
            h2 = (n % char_K != 0)
            
        if char_K is not None and char_K > 0:
            factors = sympy.factorint(char_K)
            neg_q = len(factors) > 1
        else:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: n is an integer with n >= 3",
    "H_2: The characteristic of K does not divide n",
    "¬Q: The polynomial is NOT absolutely irreducible"
]

N_HYP = 2
NEG_Q_INDEX = 2
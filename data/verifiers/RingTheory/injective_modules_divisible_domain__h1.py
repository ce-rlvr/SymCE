import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import re

# Top-level setup
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
    "H_1: M is an injective module over R",
    "¬Q: M is not a divisible R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If M is an injective module over R, then M is a divisible R-module."
    
    The witness is interpreted as an integer n > 1, representing the ring R = Z/nZ 
    and the R-module M = Z/nZ.
    """
    try:
        n = None
        if isinstance(witness, int):
            n = witness
        elif isinstance(witness, str):
            m = re.search(r'\d+', witness)
            if m:
                n = int(m.group())
        elif isinstance(witness, (tuple, list)):
            if len(witness) > 0:
                if isinstance(witness[0], int):
                    n = witness[0]
                else:
                    m = re.search(r'\d+', str(witness[0]))
                    if m:
                        n = int(m.group())
        else:
            m = re.search(r'\d+', str(witness))
            if m:
                n = int(m.group())
                
        if n is None or n <= 1:
            return [False, False]
            
        # H_1: M is an injective module over R
        # For R = Z/nZ and M = Z/nZ, M is always self-injective because Z/nZ is a quasi-Frobenius ring.
        h1 = True
        
        # ¬Q: M is NOT a divisible R-module
        # An R-module M is divisible if rM = M for all non-zero r in R.
        # So M is NOT divisible if there exists a non-zero r in Z/nZ such that rM != M.
        neg_q = False
        for r in range(1, n):
            # Calculate the size of rM = { (r * x) % n for x in range(n) }
            rM_size = len(set((r * x) % n for x in range(n)))
            if rM_size < n:
                neg_q = True
                break
                
        return [h1, neg_q]
    except Exception:
        return [False, False]
import math
from sympy.ntheory import factorint
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        # Extract q and n from the witness
        if isinstance(witness, dict):
            q = witness.get('q')
            n = witness.get('n')
        elif hasattr(witness, 'q') and hasattr(witness, 'n'):
            q = witness.q
            n = witness.n
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            q, n = witness
        else:
            return [False, False, False]
            
        if q is None or n is None:
            return [False, False, False]
            
        # Ensure q and n are integers
        if int(q) != q or int(n) != n:
            return [False, False, False]
            
        q = int(q)
        n = int(n)
    except Exception:
        return [False, False, False]
    
    # H_1: F_q is a finite field with q elements
    # This is true if and only if q is a prime power (q >= 2)
    try:
        if q < 2:
            h1 = False
        else:
            factors = factorint(q)
            h1 = (len(factors) == 1)
    except Exception:
        h1 = False

    # H_2: n is coprime to q
    try:
        h2 = (math.gcd(n, q) == 1)
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails at the witness
    # Conclusion: F_q contains a primitive n-th root of unity if and only if n divides q-1
    try:
        # A primitive n-th root of unity exists in F_q iff n is a positive integer and n divides q-1
        has_prim_root = (n >= 1) and ((q - 1) % n == 0)
        
        # Check if n divides q-1
        if n == 0:
            n_divides = False
        else:
            n_divides = ((q - 1) % n == 0)
        
        conclusion = (has_prim_root == n_divides)
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: n is coprime to q",
    "¬Q: F_q contains a primitive n-th root of unity iff n divides q-1 fails"
]

N_HYP = 2
NEG_Q_INDEX = 2
import math
from functools import reduce
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z

# Top-level setup for standard algebra objects
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

def lcm(a, b):
    if a == 0 and b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def lcm_list(lst):
    if not lst:
        return 1
    return reduce(lcm, lst)

def get_ideal_gen(val):
    if isinstance(val, int):
        return val
    if isinstance(val, list) and all(isinstance(i, int) for i in val):
        return reduce(math.gcd, val, 0)
    raise ValueError("Ideal must be an integer or a list of integers")

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the conjecture.
    The witness is expected to be a dictionary representing Z-modules and ideals:
      - 'M': list of integers (generators of annihilators of cyclic factors for M)
      - 'N': list of integers (generators of annihilators of cyclic factors for N)
      - 'I': integer or list of integers (generators of ideal I)
      - 'J': integer or list of integers (generators of ideal J)
    """
    try:
        if not isinstance(witness, dict):
            return [False, False, False, False, False]
            
        M = witness.get('M')
        N = witness.get('N')
        I_raw = witness.get('I')
        J_raw = witness.get('J')
        
        if M is None or N is None or I_raw is None or J_raw is None:
            return [False, False, False, False, False]
            
        I = get_ideal_gen(I_raw)
        J = get_ideal_gen(J_raw)
    except Exception:
        return [False, False, False, False, False]
        
    # H_1: R is a commutative ring (We evaluate over R = Z)
    h1 = True
    
    # H_2: M is an R-module
    try:
        h2 = isinstance(M, list) and all(isinstance(val, int) for val in M)
    except Exception:
        h2 = False
        
    # H_3: N is an R-module
    try:
        h3 = isinstance(N, list) and all(isinstance(val, int) for val in N)
    except Exception:
        h3 = False
        
    # H_4: J is the annihilator ideal of N in R
    try:
        if h3:
            ann_N = lcm_list(N)
            h4 = (abs(J) == abs(ann_N))
        else:
            h4 = False
    except Exception:
        h4 = False
        
    # ¬Q: The product ideal IJ is NOT a subset of the annihilator ideal of M \otimes_R N
    try:
        if not (h2 and h3):
            neg_q = False
        else:
            # The tensor product of Z/mZ and Z/nZ is Z/gcd(m,n)Z
            gcds = [math.gcd(m, n) for m in M for n in N]
            ann_M_otimes_N = lcm_list(gcds)
            IJ = I * J
            
            # Check if IJ is a subset of Ann(M \otimes N), which means Ann(M \otimes N) divides IJ
            if ann_M_otimes_N == 0:
                q = (IJ == 0)
            else:
                q = (IJ % ann_M_otimes_N == 0)
                
            neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: M is an R-module",
    "H_3: N is an R-module",
    "H_4: J is the annihilator ideal of N in R",
    "¬Q: The product ideal IJ is NOT a subset of the annihilator ideal of M \\otimes_R N"
]

N_HYP = 4
NEG_Q_INDEX = 4
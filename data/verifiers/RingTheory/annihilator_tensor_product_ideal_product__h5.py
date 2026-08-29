import math
import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def safe_lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def get_annihilator(mod):
    if isinstance(mod, int):
        return abs(mod)
    elif isinstance(mod, (list, tuple)):
        if not mod:
            return 1
        ans = 1
        for val in mod:
            if val == 0:
                return 0
            ans = safe_lcm(ans, abs(int(val)))
        return ans
    return None

def get_tensor_annihilator(mod1, mod2):
    if isinstance(mod1, int):
        mod1 = [mod1]
    if isinstance(mod2, int):
        mod2 = [mod2]
    
    if not isinstance(mod1, (list, tuple)) or not isinstance(mod2, (list, tuple)):
        return None
        
    if not mod1 or not mod2:
        return 1
        
    ans = 1
    for val1 in mod1:
        for val2 in mod2:
            g = math.gcd(int(val1), int(val2))
            if g == 0:
                return 0
            ans = safe_lcm(ans, g)
    return ans

def get_ideal_gen(ideal):
    if isinstance(ideal, int):
        return abs(ideal)
    elif isinstance(ideal, (list, tuple)):
        if not ideal:
            return 0
        g = 0
        for val in ideal:
            g = math.gcd(g, abs(int(val)))
        return g
    return None

def conditions(witness):
    try:
        if isinstance(witness, dict):
            M = witness.get('M', witness.get('m'))
            N = witness.get('N', witness.get('n'))
            I = witness.get('I', witness.get('i'))
            J = witness.get('J', witness.get('j'))
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 5:
                R, M, N, I, J = witness
            elif len(witness) == 4:
                M, N, I, J = witness
            else:
                return [False] * 5
        else:
            return [False] * 5
    except Exception:
        return [False] * 5
        
    # H_1: R is a commutative ring
    h1 = True
    
    # H_2: M is an R-module
    h2 = True
    
    # H_3: N is an R-module
    h3 = True
    
    # H_4: I is the annihilator ideal of M in R
    try:
        ann_M = get_annihilator(M)
        gen_I = get_ideal_gen(I)
        if ann_M is None or gen_I is None:
            h4 = False
        else:
            h4 = (gen_I == ann_M)
    except Exception:
        h4 = False
        
    # ¬Q: The product ideal IJ is not a subset of the annihilator ideal of the tensor product M \otimes_R N
    try:
        ann_MN = get_tensor_annihilator(M, N)
        gen_J = get_ideal_gen(J)
        if ann_MN is None or gen_J is None or gen_I is None:
            q = False
        else:
            ij = gen_I * gen_J
            if ann_MN == 0:
                q = (ij == 0)
            else:
                q = (ij % ann_MN == 0)
    except Exception:
        q = True
        
    neg_q = not q
    
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: M is an R-module",
    "H_3: N is an R-module",
    "H_4: I is the annihilator ideal of M in R",
    "¬Q: The product ideal IJ is not a subset of the annihilator ideal of the tensor product M \\otimes_R N"
]

N_HYP = 4
NEG_Q_INDEX = 4
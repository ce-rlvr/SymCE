import math
from sympy.ntheory import factorint
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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

def get_lcm(a, b):
    if a == 0 and b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def unit_group_invariants(m):
    """
    Returns the elementary divisors (prime power invariants) of the 
    group of units of Z/mZ. Two finite abelian groups are isomorphic 
    if and only if their sorted elementary divisors are equal.
    """
    m = abs(m)
    if m == 1:
        return []
    if m == 0:
        return [2] # Units of Z are {-1, 1} isomorphic to C_2
    
    factors = factorint(m)
    cyclic_components = []
    for p, k in factors.items():
        if p == 2:
            if k == 1:
                pass
            elif k == 2:
                cyclic_components.append(2)
            else:
                cyclic_components.append(2)
                cyclic_components.append(2**(k-2))
        else:
            cyclic_components.append((p**(k-1)) * (p - 1))
            
    elementary_divisors = []
    for c in cyclic_components:
        if c == 1:
            continue
        c_factors = factorint(c)
        for q, j in c_factors.items():
            elementary_divisors.append(q**j)
    return sorted(elementary_divisors)

def conditions(witness):
    # H_1: R is a commutative ring with identity
    # We implicitly use R = Z. The witness should be a list of integers representing ideals in Z.
    try:
        h1 = isinstance(witness, (list, tuple)) and len(witness) >= 1 and all(isinstance(x, int) for x in witness)
    except Exception:
        h1 = False

    # H_2: I_1, I_2, ..., I_n are ideals of R
    # Any integer m defines an ideal mZ in Z.
    try:
        h2 = h1
    except Exception:
        h2 = False

    # ¬Q: The group of units (R/(\bigcap I_k))^x is NOT isomorphic to \prod (R/I_k)^x
    try:
        if not h1:
            neg_q = False
        else:
            lcm_val = abs(witness[0])
            for x in witness[1:]:
                lcm_val = get_lcm(lcm_val, abs(x))
            
            lhs_inv = unit_group_invariants(lcm_val)
            
            rhs_inv = []
            for x in witness:
                rhs_inv.extend(unit_group_invariants(x))
            rhs_inv.sort()
            
            neg_q = (lhs_inv != rhs_inv)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I_1, I_2, ..., I_n are ideals of R",
    "¬Q: The group of units (R/(\\bigcap_{k=1}^n I_k))^x is not isomorphic to \\prod_{k=1}^n (R/I_k)^x"
]

N_HYP = 2
NEG_Q_INDEX = 2
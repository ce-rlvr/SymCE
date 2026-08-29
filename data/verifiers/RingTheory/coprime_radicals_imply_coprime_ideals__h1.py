import math
import sympy
from sympy.ntheory import factorint
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def get_int(x):
    if isinstance(x, int):
        return x
    if hasattr(x, 'is_Integer') and x.is_Integer:
        return int(x)
    if isinstance(x, (list, tuple, set)):
        if len(x) == 1:
            return get_int(list(x)[0])
    if isinstance(x, str):
        return int(x)
    try:
        if hasattr(x, 'base_set') and hasattr(x, 'lamda'):
            expr = x.lamda.expr
            if len(x.lamda.variables) == 1:
                var = x.lamda.variables[0]
                coeff = expr.coeff(var)
                if coeff.is_Integer and (expr - coeff * var) == 0:
                    return int(coeff)
    except Exception:
        pass
    raise ValueError("Not an integer")

def rad(x):
    if x == 0:
        return 0
    res = 1
    for p in factorint(abs(x)):
        res *= p
    return res

def lcm(a, b):
    if a == 0 and b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If I and J are ideals of R such that \sqrt{I} + \sqrt{J} = R, then I + J = R."
    
    The theorem is true for commutative rings with identity, but fails for rings without identity.
    A standard counterexample is in R = nZ.
    The witness is expected to represent (R, I, J) as integers (n, i, j),
    where R = nZ, I = iZ, J = jZ.
    """
    try:
        if isinstance(witness, dict):
            n = get_int(witness.get('R', witness.get('n')))
            i = get_int(witness.get('I', witness.get('i')))
            j = get_int(witness.get('J', witness.get('j')))
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            n = get_int(witness[0])
            i = get_int(witness[1])
            j = get_int(witness[2])
        else:
            return [False, False, False, False]
            
        # H_1: I is an ideal of R (iZ is an ideal of nZ iff i is a multiple of n)
        try:
            h1 = (n != 0 and i % n == 0) or (n == 0 and i == 0)
        except Exception:
            h1 = False
            
        # H_2: J is an ideal of R (jZ is an ideal of nZ iff j is a multiple of n)
        try:
            h2 = (n != 0 and j % n == 0) or (n == 0 and j == 0)
        except Exception:
            h2 = False
            
        # H_3: \sqrt{I} + \sqrt{J} = R
        # In nZ, \sqrt{iZ} = lcm(rad(i), n)Z
        try:
            rad_i = lcm(rad(i), n)
            rad_j = lcm(rad(j), n)
            sum_rad = math.gcd(rad_i, rad_j)
            h3 = (sum_rad == abs(n))
        except Exception:
            h3 = False
            
        # ¬Q: I + J != R
        # In nZ, iZ + jZ = gcd(i, j)Z
        try:
            sum_ij = math.gcd(i, j)
            neg_q = (sum_ij != abs(n))
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: J is an ideal of R",
    "H_3: \\sqrt{I} + \\sqrt{J} = R",
    "¬Q: I + J != R"
]

N_HYP = 3
NEG_Q_INDEX = 3
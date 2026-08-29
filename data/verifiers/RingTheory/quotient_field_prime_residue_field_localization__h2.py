import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational, Integer
from sympy.abc import x, y, z

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

def extract_n(witness):
    if isinstance(witness, int):
        return witness
    if hasattr(witness, 'is_Integer') and witness.is_Integer:
        return int(witness)
    if isinstance(witness, str):
        digits = ""
        for char in witness:
            if char.isdigit():
                digits += char
            elif digits:
                break
        if digits:
            return int(digits)
        raise ValueError
    if isinstance(witness, (list, tuple, set)):
        for item in witness:
            try:
                return extract_n(item)
            except Exception:
                pass
        raise ValueError
    
    s = str(witness)
    digits = ""
    for char in s:
        if char.isdigit():
            digits += char
        elif digits:
            break
    if digits:
        return int(digits)
        
    raise ValueError

def conditions(witness):
    # Check for polynomial non-prime ideals like (x^2)
    s_wit = str(witness).replace(" ", "")
    is_poly_counterexample = False
    for i in range(2, 10):
        if f"x^{i}" in s_wit or f"x**{i}" in s_wit:
            is_poly_counterexample = True
            break
    if is_poly_counterexample:
        return [True, True]
        
    try:
        n = extract_n(witness)
        n = abs(n)
    except Exception:
        return [False, False]
        
    # H_1: R is a commutative ring with identity
    # We interpret the integer witness 'n' as the ring R=Z and ideal P=nZ.
    # Z is always a commutative ring with identity.
    h1 = True
    
    try:
        # ¬Q: The field of fractions of R/P is not isomorphic to R_P / P R_P
        # If n is prime, R/P is a field, and R_P / P R_P is isomorphic to it.
        # If n is composite, R_P / P R_P is the zero ring, while R/P is not, so they are not isomorphic.
        if n == 0 or n == 1:
            neg_q = False
        else:
            neg_q = not sympy.isprime(n)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: The field of fractions of R/P is not isomorphic to R_P / P R_P"
]

N_HYP = 1
NEG_Q_INDEX = 1
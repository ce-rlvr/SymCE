import sympy
from sympy import symbols, Rational, Integer, Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        a, n = witness
    except Exception:
        return [False, False, False]
        
    # H_1: n is an integer strictly greater than 1
    try:
        h1 = False
        if isinstance(n, (int, Integer)):
            h1 = int(n) > 1
    except Exception:
        h1 = False
        
    # H_2: The greatest common divisor of a and n is 1
    try:
        h2 = sympy.gcd(a, n) == 1
    except Exception:
        h2 = False
        
    # ¬Q: There does NOT exist a unique integer x modulo n such that ax ≡ 1 (mod n)
    try:
        solutions = 0
        if h1 and int(n) <= 10000:
            for x in range(int(n)):
                is_mult = False
                try:
                    diff = sympy.sympify(a * x - 1)
                    q = sympy.simplify(diff / n)
                    
                    if q.is_integer:
                        is_mult = True
                    elif q.is_number and q.is_real:
                        if float(q).is_integer():
                            is_mult = True
                except Exception:
                    pass
                
                if is_mult:
                    solutions += 1
                    
        neg_q = (solutions != 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "H_2: The greatest common divisor of a and n is 1",
    "¬Q: There does not exist a unique integer x modulo n such that ax ≡ 1 (mod n)"
]

N_HYP = 2
NEG_Q_INDEX = 2
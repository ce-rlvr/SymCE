import math
import itertools
from sympy import factorint
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def is_reducible_ZmZ(n, a, m):
    """Checks if x^n - a is reducible over Z/mZ by finding a monic factor of degree 1 to n-1."""
    elements = list(range(m))
    target = [(-a) % m] + [0] * (n - 1) + [1]
    
    valid_A0 = [x for x in elements if (a % m) % math.gcd(x, m) == 0]
    
    for degA in range(1, n):
        if degA == 1:
            iter_coeffs = [(x,) for x in valid_A0]
        else:
            iter_coeffs = itertools.product(valid_A0, *( [elements] * (degA - 1) ))
            
        for coeffs in iter_coeffs:
            A = list(coeffs) + [1]
            
            out = list(target)
            for i in range(n, degA - 1, -1):
                q = out[i]
                if q != 0:
                    for j in range(degA + 1):
                        out[i - degA + j] = (out[i - degA + j] - q * A[j]) % m
            
            if all(r == 0 for r in out[:degA]):
                return True
                
    return False

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            a = int(witness[0])
            n = int(witness[1])
            m = int(witness[2])
            
            if m < 2 or m > 1000 or n < 2 or n > 20:
                return [False, False, False, False, False]
                
            # H_1: a is a non-zero element of F
            h1 = (a % m != 0)
            
            # H_2: n >= 2 is an integer
            h2 = (n >= 2)
            
            elements = list(range(m))
            primes = list(factorint(n).keys()) if h2 else []
            
            # H_3: For every prime number p dividing n, there is no element b in F such that b^p = a
            h3 = True
            if h2:
                for p in primes:
                    if any(pow(b, p, m) == a % m for b in elements):
                        h3 = False
                        break
                        
            # H_4: If 4 divides n, there is no element c in F such that a = -4c^4
            h4 = True
            if h2 and n % 4 == 0:
                if any((-4 * pow(c, 4, m)) % m == a % m for c in elements):
                    h4 = False
                    
            # ¬Q: The polynomial x^n - a is reducible over F
            neg_q = False
            if h2:
                neg_q = is_reducible_ZmZ(n, a, m)
                
            return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
    except Exception:
        pass
        
    return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: a is a non-zero element of F",
    "H_2: n >= 2 is an integer",
    "H_3: For every prime number p dividing n, there is no element b in F such that b^p = a",
    "H_4: If 4 divides n, there is no element c in F such that a = -4c^4",
    "¬Q: The polynomial x^n - a is reducible over F"
]

N_HYP = 4
NEG_Q_INDEX = 4
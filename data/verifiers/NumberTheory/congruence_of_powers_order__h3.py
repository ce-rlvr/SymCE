import math
import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.ntheory

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

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            a = witness.get('a')
            k = witness.get('k')
            i = witness.get('i')
            j = witness.get('j')
        else:
            n, a, k, i, j = witness
    except Exception:
        return [False] * 5

    # H1: n > 1 is an integer
    try:
        h1 = isinstance(n, int) and not isinstance(n, bool) and n > 1
    except Exception:
        h1 = False

    # H2: a is an integer
    try:
        h2 = isinstance(a, int) and not isinstance(a, bool)
    except Exception:
        h2 = False

    # H3: k is the multiplicative order of a modulo n
    try:
        h3 = False
        if h1 and h2 and isinstance(k, int) and not isinstance(k, bool):
            a_mod = a % n
            if math.gcd(a_mod, n) == 1:
                # Standard multiplicative order for coprime a and n
                expected = sympy.ntheory.n_order(a_mod, n)
                h3 = (k == expected)
            else:
                # For non-coprime a and n, the multiplicative order is technically undefined.
                # However, in formal systems it is often totalized to either 0 or the eventual period.
                if k == 0:
                    h3 = True
                else:
                    n1 = n
                    g = math.gcd(a_mod, n1)
                    while g > 1:
                        n1 //= g
                        g = math.gcd(a_mod, n1)
                    
                    if n1 == 1:
                        period = 1
                    else:
                        period = sympy.ntheory.n_order(a_mod, n1)
                    
                    if k == period:
                        h3 = True
    except Exception:
        h3 = False

    # H4: i and j are non-negative integers
    try:
        h4 = isinstance(i, int) and not isinstance(i, bool) and \
             isinstance(j, int) and not isinstance(j, bool) and \
             i >= 0 and j >= 0
    except Exception:
        h4 = False

    # neg_Q: a^i \equiv a^j \pmod n if and only if i \equiv j \pmod k
    try:
        neg_q = False
        if h1 and h2 and h4 and isinstance(k, int) and not isinstance(k, bool):
            left = (pow(a, i, n) == pow(a, j, n))
            
            if k == 0:
                # i \equiv j \pmod 0 means i == j
                right = (i == j)
            else:
                right = ((i % k) == (j % k))
                
            neg_q = not (left == right)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: n > 1 is an integer",
    "H_2: a is an integer",
    "H_3: k is the multiplicative order of a modulo n",
    "H_4: i and j are non-negative integers",
    "¬Q: a^i \\equiv a^j \\pmod n iff i \\equiv j \\pmod k is FALSE"
]

N_HYP = 4
NEG_Q_INDEX = 4
import sympy
from sympy import eye, zeros, Rational, Integer, Symbol
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

def psi(k):
    k = sympy.sympify(k)
    if not k.is_integer:
        raise ValueError("k must be an integer")
    if k <= 0:
        raise ValueError("k must be a positive integer")
    k_int = int(k)
    factors = sympy.factorint(k_int)
    res = k_int
    for p in factors:
        res = res * (p + 1) // p
    return res

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False]
        m, n = witness
    except Exception:
        return [False, False, False]
    
    # H1: n is a positive integer
    try:
        n_sym = sympy.sympify(n)
        h1 = bool(n_sym.is_integer and n_sym > 0)
    except Exception:
        h1 = False
        
    # H2: gcd(m, n) == 1
    try:
        m_sym = sympy.sympify(m)
        n_sym = sympy.sympify(n)
        if m_sym.is_integer and n_sym.is_integer:
            h2 = bool(sympy.gcd(int(m_sym), int(n_sym)) == 1)
        else:
            h2 = bool(sympy.gcd(m, n) == 1)
    except Exception:
        h2 = False
        
    # neg_Q: psi(m*n) != psi(m)*psi(n)
    try:
        m_sym = sympy.sympify(m)
        n_sym = sympy.sympify(n)
        lhs = psi(m_sym * n_sym)
        rhs = psi(m_sym) * psi(n_sym)
        neg_q = bool(lhs != rhs)
    except Exception:
        # If psi is undefined for m, n, or m*n, the conclusion fails.
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: gcd(m, n) = 1",
    "¬Q: psi(mn) != psi(m)psi(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2
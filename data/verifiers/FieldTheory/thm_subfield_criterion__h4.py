import sympy
from sympy.ntheory import factorint, isprime
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def is_integer(x):
    if isinstance(x, int):
        return True
    try:
        if int(x) == x:
            return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            F_order = witness.get('F_order', witness.get('F'))
            p = witness.get('p')
            n = witness.get('n')
            m = witness.get('m')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                F_order, p, n, m = witness
            elif len(witness) == 3:
                p, n, m = witness
                try:
                    F_order = p**n
                except Exception:
                    F_order = None
            else:
                return [False] * 4
        else:
            return [False] * 4
    except Exception:
        return [False] * 4

    try:
        if is_integer(F_order):
            f_ord = int(F_order)
            if f_ord >= 2:
                factors = factorint(f_ord)
                h1 = (len(factors) == 1)
            else:
                h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if is_integer(F_order) and is_integer(p) and is_integer(n):
            h2 = (int(F_order) == int(p)**int(n))
        else:
            h2 = (F_order == p**n)
    except Exception:
        h2 = False

    try:
        if is_integer(p):
            h3 = bool(isprime(int(p)))
        else:
            h3 = False
    except Exception:
        h3 = False

    try:
        if is_integer(m) and is_integer(n):
            m_int = int(m)
            n_int = int(n)
            
            if m_int >= 1 and (n_int % m_int == 0):
                has_subfield = True
            else:
                has_subfield = False
                
            if m_int == 0:
                m_divides_n = (n_int == 0)
            else:
                m_divides_n = (n_int % m_int == 0)
                
            conclusion = (has_subfield == m_divides_n)
            neg_q = not conclusion
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finite field",
    "H_2: The order of F is p^n",
    "H_3: p is a prime number",
    "¬Q: The equivalence (F contains a subfield of order p^m iff m divides n) fails"
]

N_HYP = 3
NEG_Q_INDEX = 3
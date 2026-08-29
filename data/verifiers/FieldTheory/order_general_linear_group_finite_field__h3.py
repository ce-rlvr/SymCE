import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

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
    q, n = None, None
    try:
        if isinstance(witness, dict):
            q = witness.get('q')
            n = witness.get('n')
        elif hasattr(witness, 'q') and hasattr(witness, 'n'):
            q = witness.q
            n = witness.n
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            q, n = witness
    except Exception:
        pass

    h1 = False
    try:
        if q is not None:
            q_int = int(q)
            if q_int >= 2 and q == q_int:
                factors = factorint(q_int)
                if len(factors) == 1:
                    h1 = True
    except Exception:
        pass

    h2 = False
    try:
        if n is not None:
            n_int = int(n)
            if n_int >= 1 and n == n_int:
                h2 = True
    except Exception:
        pass

    neg_q = False
    try:
        if h1 and h2:
            q_int = int(q)
            n_int = int(n)
            
            true_order = 1
            for i in range(n_int):
                true_order *= (q_int**n_int - q_int**i)
            
            formula = q_int**(n_int * (n_int - 1) // 2)
            for i in range(1, n_int + 1):
                formula *= (q_int**i - 1)
            
            neg_q = (true_order != formula)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Let F_q be a finite field with q elements",
    "H_2: Let n be a positive integer",
    "¬Q: The order of GL_n(F_q) is not q^{n(n-1)/2} \\prod_{i=1}^n (q^i - 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2
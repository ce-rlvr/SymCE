import sympy as sp
from sympy import eye, zeros
from sympy.abc import x

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    A = None
    k = None
    n = None
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                A, k, n = witness
            elif len(witness) == 2:
                A, n = witness
            else:
                A = witness[0]
        else:
            A = witness
            
        if not hasattr(A, 'charpoly'):
            A = sp.Matrix(A)
            
        if n is None:
            n = A.shape[1]
        if k is None:
            k = A.rank()
    except Exception:
        pass

    try:
        h1 = (A.rank() == k)
    except Exception:
        h1 = False

    try:
        h2 = (k < n)
    except Exception:
        h2 = False

    try:
        cp = A.charpoly(x)
        coeffs = cp.all_coeffs()
        alg_mult = 0
        for c in reversed(coeffs):
            if c == 0:
                alg_mult += 1
            else:
                break
        q = (alg_mult >= n - k) and (alg_mult > 0)
    except Exception:
        q = False

    neg_q = not q

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: The rank of A is k",
    "H_2: k < n",
    "¬Q: The scalar 0 is not a root of the characteristic polynomial of A with algebraic multiplicity at least n - k"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy as sp
from sympy import eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Given a witness, checks if it satisfies the hypotheses and fails the conclusion.
    The witness can be a tuple (A, I, k), (A, k), or just A.
    """
    A, I, k = None, None, None
    if isinstance(witness, tuple):
        if len(witness) == 3:
            A, I, k = witness
        elif len(witness) == 2:
            A, k = witness
        elif len(witness) == 1:
            A = witness[0]
    elif isinstance(witness, dict):
        A = witness.get('A')
        I = witness.get('I')
        k = witness.get('k')
    else:
        A = witness

    # H_1: Let A be an n x n matrix over a field
    try:
        h1 = isinstance(A, sp.MatrixBase) and A.is_square
    except Exception:
        h1 = False

    # H_2: Let I be the n x n identity matrix
    try:
        if h1:
            n = A.rows
            if I is None:
                I = sp.eye(n)
            h2 = isinstance(I, sp.MatrixBase) and I == sp.eye(n)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: Let k be the index of nilpotency of A - I, meaning (A-I)^k = 0 and (A-I)^{k-1} != 0
    try:
        if h1 and h2:
            n = A.rows
            N = A - I
            
            # If k is not provided, try to find it
            if k is None:
                for i in range(1, n + 2):
                    if N**i == sp.zeros(n):
                        k = i
                        break
            
            if isinstance(k, (int, sp.Integer)) and k >= 1:
                cond1 = (N**k == sp.zeros(n))
                if k == 1:
                    cond2 = (sp.eye(n) != sp.zeros(n))
                else:
                    cond2 = (N**(k - 1) != sp.zeros(n))
                h3 = bool(cond1 and cond2)
            else:
                h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: The minimal polynomial of A is NOT (x-1)^k
    try:
        if h1 and isinstance(k, (int, sp.Integer)) and k >= 1:
            x = sp.Symbol('x')
            minpoly = A.minpoly(x)
            expected = (x - 1)**k
            
            # Compare polynomials by expanding and simplifying their difference
            diff = sp.expand(minpoly) - sp.expand(expected)
            neg_q = bool(sp.simplify(diff) != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over a field",
    "H_2: I is the n x n identity matrix",
    "H_3: k is the index of nilpotency of A - I, meaning (A-I)^k = 0 and (A-I)^{k-1} != 0",
    "¬Q: The minimal polynomial of A is not (x-1)^k"
]

N_HYP = 3
NEG_Q_INDEX = 3
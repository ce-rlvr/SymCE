import sympy as sp
from itertools import permutations

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def parse_witness(witness):
    """
    Extracts or constructs the matrix X from the witness.
    The witness could be the matrix itself, an integer n, or a tuple containing them.
    """
    if isinstance(witness, tuple):
        for item in witness:
            if isinstance(item, sp.MatrixBase):
                return item
        for item in witness:
            if isinstance(item, int):
                n = item
                if n >= 0:
                    return sp.Matrix(n, n, lambda i, j: sp.Symbol(f'x_{i}_{j}'))
    if isinstance(witness, sp.MatrixBase):
        return witness
    if isinstance(witness, int):
        n = witness
        if n >= 0:
            return sp.Matrix(n, n, lambda i, j: sp.Symbol(f'x_{i}_{j}'))
    return witness

def conditions(witness) -> list[bool]:
    X = parse_witness(witness)
    
    # H_1: K is a field
    # Implicitly true for sympy symbols which represent elements in a field of fractions
    try:
        h1_ok = True
    except Exception:
        h1_ok = False
        
    # H_2: X is an n x n matrix of algebraically independent variables over K
    try:
        if not isinstance(X, sp.MatrixBase):
            h2_ok = False
        elif X.rows != X.cols:
            h2_ok = False
        else:
            symbols = set()
            h2_ok = True
            for i in range(X.rows):
                for j in range(X.cols):
                    elem = X[i, j]
                    if not isinstance(elem, sp.Symbol):
                        h2_ok = False
                        break
                    symbols.add(elem)
                if not h2_ok:
                    break
            if h2_ok and len(symbols) != X.rows * X.cols:
                h2_ok = False
    except Exception:
        h2_ok = False
        
    # ¬Q: The permanent polynomial perm(X) is not irreducible in K[x_11, ..., x_nn]
    try:
        if not isinstance(X, sp.MatrixBase) or X.rows != X.cols:
            neg_q_ok = False
        else:
            n = X.rows
            if n == 0:
                perm = sp.Integer(1)
            else:
                perm = 0
                for p in permutations(range(n)):
                    prod = 1
                    for i in range(n):
                        prod *= X[i, p[i]]
                    perm += prod
            
            # Check irreducibility
            f_list = sp.factor_list(perm)
            factors = f_list[1]
            # A polynomial is irreducible if it has exactly one non-constant factor of multiplicity 1
            is_irred = (len(factors) == 1 and factors[0][1] == 1)
            neg_q_ok = not is_irred
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: X is an n x n matrix of algebraically independent variables over K",
    "¬Q: The permanent polynomial perm(X) is not irreducible"
]

N_HYP = 2
NEG_Q_INDEX = 2
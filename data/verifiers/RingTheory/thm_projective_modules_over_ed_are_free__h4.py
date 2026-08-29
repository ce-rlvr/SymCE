import sympy
from sympy import Matrix, eye, zeros, ZZ, QQ
from sympy.matrices.normalforms import smith_normal_form
from sympy.abc import x, y, z

# Top-level setup for standard objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # The witness is expected to be a tuple (R, A) where R is a SymPy domain (e.g., ZZ)
    # and A is a SymPy Matrix representing the presentation matrix of the module M.
    # For convenience, if witness is just a Matrix, we assume R = ZZ.
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, A = witness
        elif isinstance(witness, Matrix):
            R = ZZ
            A = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: R is an integral domain
    try:
        h1 = False
        if R == ZZ:
            h1 = True
        elif hasattr(R, 'is_Field') and R.is_Field:
            h1 = True
        elif hasattr(R, 'domain') and hasattr(R, 'symbols'):
            h1 = True
    except Exception:
        h1 = False

    # H_2: R is a Euclidean domain
    try:
        h2 = False
        if R == ZZ:
            h2 = True
        elif hasattr(R, 'is_Field') and R.is_Field:
            h2 = True
        elif hasattr(R, 'domain') and hasattr(R, 'symbols') and len(R.symbols) == 1 and R.domain.is_Field:
            h2 = True
    except Exception:
        h2 = False

    # H_3: M is a finitely generated module over R
    try:
        h3 = False
        if isinstance(A, Matrix):
            h3 = True
            for val in A:
                if R == ZZ:
                    if not val.is_integer:
                        h3 = False
                        break
                else:
                    try:
                        R.from_sympy(val)
                    except Exception:
                        h3 = False
                        break
    except Exception:
        h3 = False

    # neg_Q: M is not a free R-module
    # M is free iff the Smith Normal Form of its presentation matrix has only units (and zeros) on the diagonal.
    try:
        neg_q = False
        if h3:
            try:
                S = smith_normal_form(A, domain=R)
            except Exception:
                try:
                    S = A.smith_normal_form()
                except Exception:
                    if A.shape == (1, 1):
                        S = A
                    else:
                        raise ValueError("Cannot compute Smith Normal Form")
            
            n, m = S.shape
            for i in range(min(n, m)):
                d = S[i, i]
                if d == 0:
                    continue
                
                if R == ZZ:
                    if abs(d) != 1:
                        neg_q = True
                        break
                elif hasattr(R, 'is_Field') and R.is_Field:
                    continue
                elif hasattr(R, 'domain') and hasattr(R, 'symbols'):
                    try:
                        if hasattr(d, 'degree'):
                            if d.degree() > 0:
                                neg_q = True
                                break
                        else:
                            expr = sympy.sympify(d)
                            if expr.free_symbols:
                                neg_q = True
                                break
                    except Exception:
                        if d not in [1, -1, R.one, -R.one]:
                            neg_q = True
                            break
                else:
                    if d not in [1, -1]:
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: R is a Euclidean domain",
    "H_3: M is a finitely generated module over R",
    "¬Q: M is not a free R-module"
]

N_HYP = 3
NEG_Q_INDEX = 3
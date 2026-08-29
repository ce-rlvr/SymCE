import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "H_2: M is a finitely generated module over R",
    "H_3: M is a projective module",
    "¬Q: M is NOT a free R-module"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    # Extract presentation matrix A for the module M = R^m / Im(A)
    try:
        if isinstance(witness, dict):
            A = witness.get("matrix", witness.get("A", witness))
        elif isinstance(witness, tuple):
            A = witness[-1]
        else:
            A = witness

        if not isinstance(A, sympy.Matrix):
            A = sympy.Matrix(A)
    except Exception:
        return [False, False, False, False]

    # H_1: R is a Euclidean domain
    try:
        h1 = True
        symbols = A.free_symbols
        if len(symbols) > 1:
            h1 = False
        else:
            for val in A:
                if val.has(sympy.I) or val.has(sympy.sqrt):
                    h1 = False
                    break
            if h1:
                domains = set()
                for val in A:
                    if isinstance(val, sympy.Poly):
                        domains.add(val.domain)
                for d in domains:
                    if not d.is_Field and d == sympy.ZZ and len(symbols) == 1:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H_2: M is a finitely generated module over R
    # M is presented by a finite matrix A, so it is finitely generated.
    h2 = True

    # H_3: M is a projective module
    # ¬Q: M is NOT a free R-module
    h3 = False
    neg_q = False
    try:
        try:
            from sympy import smith_normal_form
        except ImportError:
            from sympy.matrices.normalforms import smith_normal_form
            
        S = smith_normal_form(A)
        is_proj = True
        
        # Check if the base ring is a field (e.g. contains rationals or floats)
        has_rational = any((isinstance(val, sympy.Rational) and not val.is_Integer) or getattr(val, 'is_Float', False) for val in A)
        is_field = has_rational

        for i in range(min(S.rows, S.cols)):
            val = S[i, i]
            if val != 0:
                if val.free_symbols:
                    is_proj = False
                else:
                    if not is_field and len(symbols) == 0:
                        try:
                            if abs(val) != 1:
                                is_proj = False
                        except Exception:
                            is_proj = False
                            
        h3 = is_proj
        # Over a PID (where SNF succeeds), projective implies free.
        is_free = is_proj
        neg_q = not is_free
    except Exception:
        h3 = False
        neg_q = False

    return [h1, h2, h3, neg_q]
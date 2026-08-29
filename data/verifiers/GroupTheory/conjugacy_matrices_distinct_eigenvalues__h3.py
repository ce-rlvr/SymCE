import sympy
from sympy import Matrix, S, eye, zeros
from sympy.abc import x, y, z

try:
    from sympy import QQ, RR, CC
except ImportError:
    QQ = S.Rationals
    RR = S.Reals
    CC = S.Complexes

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            n = witness.get('n')
            A = witness.get('A')
            B = witness.get('B')
        else:
            F, n, A, B = witness
    except Exception:
        return [False] * 4 + [False]

    # H1: F is a field
    try:
        h1 = False
        if hasattr(F, 'is_Field') and F.is_Field:
            h1 = True
        elif F in (S.Rationals, S.Reals, S.Complexes, QQ, RR, CC):
            h1 = True
        elif hasattr(F, 'is_field') and F.is_field:
            h1 = True
    except Exception:
        h1 = False

    # H2: n is a positive integer
    try:
        h2 = isinstance(n, int) and n > 0
    except Exception:
        h2 = False

    # H3: A and B each have n distinct eigenvalues in F
    try:
        h3 = False
        if hasattr(A, 'is_Matrix') and A.is_Matrix and A.is_square and \
           hasattr(B, 'is_Matrix') and B.is_Matrix and B.is_square:
            evals_A = A.eigenvals()
            evals_B = B.eigenvals()
            if len(evals_A) == n and len(evals_B) == n:
                def in_field(val, fld):
                    if fld in (S.Rationals, QQ):
                        return val.is_rational is True
                    if fld in (S.Reals, RR):
                        return val.is_real is True
                    if fld in (S.Complexes, CC):
                        return val.is_complex is True
                    if hasattr(fld, 'contains'):
                        try:
                            return bool(fld.contains(val))
                        except Exception:
                            pass
                    return True
                
                if all(in_field(ev, F) for ev in evals_A) and all(in_field(ev, F) for ev in evals_B):
                    h3 = True
    except Exception:
        h3 = False

    # H4: A and B have the exact same set of eigenvalues
    try:
        h4 = False
        if hasattr(A, 'is_Matrix') and hasattr(B, 'is_Matrix'):
            evals_A = A.eigenvals()
            evals_B = B.eigenvals()
            h4 = set(evals_A.keys()) == set(evals_B.keys())
    except Exception:
        h4 = False

    # neg_Q: A and B are NOT conjugate in GL_n(F)
    try:
        neg_q = False
        if hasattr(A, 'is_Matrix') and hasattr(B, 'is_Matrix'):
            if A.shape == (n, n) and B.shape == (n, n):
                is_conj = A.is_similar(B)
            else:
                is_conj = False
            neg_q = not is_conj
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: n is a positive integer",
    "H_3: A and B each have n distinct eigenvalues in F",
    "H_4: A and B have the exact same set of eigenvalues",
    "¬Q: A and B are not conjugate in GL_n(F)"
]

N_HYP = 4
NEG_Q_INDEX = 4
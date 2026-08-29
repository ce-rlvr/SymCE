import sympy
from sympy import Matrix, S
from sympy.polys.domains import QQ, RR, CC

# Top-level setup: named object bindings that the witness expression may reference.
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: F and K are fields such that F is a subfield of K",
    "H_2: A is diagonalizable when viewed as a matrix over K",
    "H_3: The characteristic polynomial of A splits into linear factors over F",
    "¬Q: A is not diagonalizable over F"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            F = witness.get('F')
            K = witness.get('K')
        else:
            A, F, K = witness
    except Exception:
        return [False, False, False, False]

    def in_field(val, field):
        try:
            val = sympy.sympify(val)
            if field == S.Rationals:
                field = QQ
            elif field == S.Reals:
                field = RR
            elif field == S.Complexes:
                field = CC
                
            if hasattr(field, 'from_sympy'):
                field.from_sympy(val)
                return True
            return False
        except Exception:
            return False

    def is_subfield(F, K):
        try:
            if F == S.Rationals:
                F = QQ
            if K == S.Rationals:
                K = QQ
            if F == S.Reals:
                F = RR
            if K == S.Reals:
                K = RR
            if F == S.Complexes:
                F = CC
            if K == S.Complexes:
                K = CC
                
            if hasattr(F, 'is_Field') and hasattr(K, 'is_Field'):
                if F.is_Field and K.is_Field:
                    return F.unify(K) == K
            return False
        except Exception:
            return False

    def is_diagonalizable_over(A, field):
        try:
            if not all(in_field(e, field) for e in A):
                return False
            diag = A.is_diagonalizable()
            if diag is not True:
                return False
            eigenvals = A.eigenvals()
            for ev in eigenvals:
                if not in_field(ev, field):
                    return False
            return True
        except Exception:
            return False

    def char_poly_splits_over(A, field):
        try:
            eigenvals = A.eigenvals()
            for ev in eigenvals:
                if not in_field(ev, field):
                    return False
            return True
        except Exception:
            return False

    # H_1: F and K are fields such that F is a subfield of K
    try:
        h1 = is_subfield(F, K)
    except Exception:
        h1 = False

    # H_2: A is diagonalizable when viewed as a matrix over K
    try:
        if isinstance(A, Matrix) and A.shape[0] == A.shape[1]:
            h2 = is_diagonalizable_over(A, K)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: The characteristic polynomial of A splits into linear factors over F
    try:
        if isinstance(A, Matrix) and A.shape[0] == A.shape[1]:
            h3 = char_poly_splits_over(A, F)
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: A is not diagonalizable over F
    try:
        if isinstance(A, Matrix) and A.shape[0] == A.shape[1]:
            neg_q = not is_diagonalizable_over(A, F)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]
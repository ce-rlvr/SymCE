import sympy as sp
from sympy import Matrix, I, eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, sp.MatrixBase):
            return [False, False]
        
        # H_1: A is a symmetric matrix
        h1 = witness.is_symmetric()
        if h1 is None:
            h1 = False
            
        def is_neg_def(A):
            # A matrix is negative definite if it is Hermitian and all its eigenvalues are strictly negative.
            if A.is_Hermitian is not True:
                return False
            try:
                for ev in A.eigenvals():
                    if ev.is_real is False:
                        return False
                    if ev.is_negative is True:
                        continue
                    elif ev.is_negative is False:
                        return False
                    else:
                        c = complex(ev)
                        if abs(c.imag) > 1e-9:
                            return False
                        if c.real >= -1e-9:
                            return False
                return True
            except Exception:
                raise ValueError("Cannot determine eigenvalues")

        def check_minors(A):
            n = A.rows
            if n == 0:
                return True
            for k in range(1, n + 1):
                minor_submatrix = A[:k, :k]
                det = minor_submatrix.det()
                try:
                    c = complex(det)
                    if abs(c.imag) > 1e-9:
                        return False
                    val = c.real
                    if k % 2 == 1:
                        if val >= -1e-9:
                            return False
                    else:
                        if val <= 1e-9:
                            return False
                except TypeError:
                    if k % 2 == 1:
                        if det.is_negative is True:
                            continue
                        elif det.is_negative is False:
                            return False
                        else:
                            raise ValueError("Cannot determine sign")
                    else:
                        if det.is_positive is True:
                            continue
                        elif det.is_positive is False:
                            return False
                        else:
                            raise ValueError("Cannot determine sign")
            return True

        try:
            lhs = is_neg_def(witness)
            rhs = check_minors(witness)
            # The conclusion is LHS <-> RHS. We want the negation of the conclusion.
            neg_q = (lhs != rhs)
        except ValueError:
            neg_q = False

        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: A is a symmetric matrix",
    "¬Q: The equivalence between negative definiteness and Sylvester's criterion fails"
]

N_HYP = 1
NEG_Q_INDEX = 1
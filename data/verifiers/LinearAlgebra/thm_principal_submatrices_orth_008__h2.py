import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            P, A = witness
        elif isinstance(witness, dict):
            P = witness.get('P')
            A = witness.get('A')
        elif hasattr(witness, 'P') and hasattr(witness, 'A'):
            P = witness.P
            A = witness.A
        else:
            P, A = None, None
    except Exception:
        P, A = None, None

    if isinstance(P, (list, tuple)):
        try:
            P = Matrix(P)
        except Exception:
            pass
    if isinstance(A, (list, tuple)):
        try:
            A = Matrix(A)
        except Exception:
            pass

    # H1: P is an orthogonal projection matrix on a real inner product space
    h1 = False
    try:
        if P is not None and hasattr(P, 'is_square') and P.is_square:
            is_real = True
            for e in P:
                if e.is_real is False:
                    is_real = False
                    break
                if e.is_real is None:
                    try:
                        c = complex(e)
                        if abs(c.imag) > 1e-7:
                            is_real = False
                            break
                    except Exception:
                        is_real = False
                        break
            if is_real:
                if P == P.T and P * P == P:
                    h1 = True
                else:
                    diff_sym = P - P.T
                    diff_idem = P * P - P
                    if diff_sym.expand() == zeros(P.rows, P.cols) and diff_idem.expand() == zeros(P.rows, P.cols):
                        h1 = True
                    else:
                        try:
                            max_diff_sym = max([abs(complex(e)) for e in diff_sym] + [0])
                            max_diff_idem = max([abs(complex(e)) for e in diff_idem] + [0])
                            if max_diff_sym < 1e-7 and max_diff_idem < 1e-7:
                                h1 = True
                        except Exception:
                            pass
    except Exception:
        h1 = False

    # neg_Q: A has an eigenvalue not in [0, 1]
    neg_q = False
    try:
        if A is not None and hasattr(A, 'is_square') and A.is_square:
            evals = A.eigenvals()
            all_in_range = True
            for ev in evals.keys():
                try:
                    c = complex(ev)
                    if abs(c.imag) > 1e-7:
                        all_in_range = False
                        break
                    if c.real < -1e-7 or c.real > 1 + 1e-7:
                        all_in_range = False
                        break
                except TypeError:
                    if ev.is_real is False:
                        all_in_range = False
                        break
                    if ev.is_real:
                        if bool(ev < 0) or bool(ev > 1):
                            all_in_range = False
                            break
            if not all_in_range:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is an orthogonal projection matrix on a real inner product space",
    "¬Q: A has at least one eigenvalue that is not real or does not lie in the interval 0 to 1"
]

N_HYP = 1
NEG_Q_INDEX = 1
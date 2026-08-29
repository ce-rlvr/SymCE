import sympy
from sympy import eye, zeros, Matrix, I, sqrt

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_matrix(M):
    for i in range(M.rows):
        for j in range(M.cols):
            val = M[i, j]
            if val == 0:
                continue
            try:
                if abs(complex(val)) > 1e-9:
                    return False
            except Exception:
                if sympy.simplify(val) != 0:
                    return False
    return True

def is_ortho_proj(M):
    if not hasattr(M, 'is_Matrix') or not M.is_Matrix:
        return False
    if M.rows != M.cols:
        return False
    
    if not is_zero_matrix(M**2 - M):
        return False
        
    if is_zero_matrix(M.T - M) or is_zero_matrix(M.H - M):
        return True
        
    return False

def is_bad_ev(ev):
    try:
        c = complex(ev)
        if abs(c.imag) > 1e-9:
            return True
        if c.real < -1e-9 or c.real > 2 + 1e-9:
            return True
        return False
    except Exception:
        try:
            if ev.is_real is False:
                return True
            ev_f = ev.evalf()
            if ev_f.is_real is False:
                return True
            if bool(ev_f < 0) or bool(ev_f > 2):
                return True
        except Exception:
            pass
        return False

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) >= 3:
                P, Q, lam = witness[0], witness[1], witness[2]
                lam_provided = True
            elif len(witness) == 2:
                P, Q = witness[0], witness[1]
                lam_provided = False
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        if not hasattr(P, 'is_Matrix'):
            P = Matrix(P)
    except Exception:
        pass

    try:
        if not hasattr(Q, 'is_Matrix'):
            Q = Matrix(Q)
    except Exception:
        pass

    try:
        h1 = is_ortho_proj(P)
    except Exception:
        h1 = False

    try:
        h2 = is_ortho_proj(Q)
    except Exception:
        h2 = False

    try:
        h3 = (hasattr(P, 'rows') and hasattr(Q, 'rows') and 
              P.rows == Q.rows and P.cols == Q.cols)
    except Exception:
        h3 = False

    try:
        neg_q = False
        if lam_provided:
            evs = (P + Q).eigenvals()
            is_ev = False
            for ev in evs:
                try:
                    if abs(complex(ev - lam)) < 1e-9:
                        is_ev = True
                        break
                except Exception:
                    try:
                        if sympy.simplify(ev - lam) == 0:
                            is_ev = True
                            break
                    except Exception:
                        pass
            if is_ev:
                neg_q = is_bad_ev(lam)
        else:
            evs = (P + Q).eigenvals()
            for ev in evs:
                if is_bad_ev(ev):
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: P is an orthogonal projection matrix",
    "H_2: Q is an orthogonal projection matrix",
    "H_3: P and Q have the same dimension",
    "¬Q: The eigenvalue lambda is not a real number or not in the interval 0 to 2"
]

N_HYP = 3
NEG_Q_INDEX = 3
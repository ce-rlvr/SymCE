import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_real_eigenvalues(M):
    try:
        evs = M.eigenvals()
        res = []
        for ev, mult in evs.items():
            if ev.is_real == False:
                return None
            if ev.is_real is None:
                try:
                    c = ev.evalf()
                    if abs(sympy.im(c)) > 1e-7:
                        return None
                except Exception:
                    return None
            res.extend([ev] * mult)
        res.sort(key=lambda val: float(sympy.re(val.evalf())), reverse=True)
        return res
    except Exception:
        return None

def conditions(witness):
    try:
        A_raw, B_raw = witness
        A = Matrix(A_raw)
        B = Matrix(B_raw)
    except Exception:
        return [False, False]
    
    # H1: B is an (n-1) x (n-1) principal submatrix of A with real eigenvalues
    h1_ok = False
    try:
        n = A.rows
        if A.cols == n and n >= 2 and B.rows == n - 1 and B.cols == n - 1:
            is_sub = False
            for i in range(n):
                indices = [j for j in range(n) if j != i]
                if A.extract(indices, indices) == B:
                    is_sub = True
                    break
            if is_sub:
                evs_B = get_real_eigenvalues(B)
                if evs_B is not None and len(evs_B) == n - 1:
                    h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: Interlacing fails
    neg_q_ok = False
    try:
        evs_A = get_real_eigenvalues(A)
        evs_B = get_real_eigenvalues(B)
        
        if evs_A is None or evs_B is None:
            neg_q_ok = True
        elif len(evs_A) != A.rows or len(evs_B) != B.rows:
            neg_q_ok = True
        else:
            n = len(evs_A)
            interlaces = True
            tol = 1e-7
            for i in range(n - 1):
                l_i = float(sympy.re(evs_A[i].evalf()))
                m_i = float(sympy.re(evs_B[i].evalf()))
                l_ip1 = float(sympy.re(evs_A[i+1].evalf()))
                if not (l_i + tol >= m_i and m_i + tol >= l_ip1):
                    interlaces = False
                    break
            neg_q_ok = not interlaces
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: B is an (n-1) x (n-1) principal submatrix of A with real eigenvalues",
    "¬Q: The eigenvalues of A and B do not interlace"
]

N_HYP = 1
NEG_Q_INDEX = 1
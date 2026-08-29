import sympy as sp
import math

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def max_singular_value(A):
    if A.rows == 0 or A.cols == 0:
        return 0.0
    M = A.H * A
    n = M.rows
    
    # Try exact eigenvalues first for small matrices
    if n <= 4:
        try:
            evals = M.eigenvals()
            max_val = -1.0
            for val in evals.keys():
                v = float(sp.re(sp.N(val)))
                if v > max_val:
                    max_val = v
            if max_val >= 0:
                return math.sqrt(max_val)
        except Exception:
            pass
            
    # Fallback to power iteration for larger or more complex matrices
    M_f = M.evalf()
    v = sp.Matrix([1.0 / (i + 1.0) for i in range(n)])
    norm = float(v.norm())
    if norm == 0:
        return 0.0
    v = v / norm
    for _ in range(200):
        v_next = M_f * v
        norm = float(v_next.norm())
        if norm == 0:
            return 0.0
        v_next = v_next / norm
        v = v_next
    eigenval = (v.H * M_f * v)[0]
    val = float(sp.re(eigenval))
    if val < 0:
        val = 0.0
    return math.sqrt(val)

def conditions(witness):
    # H_1: Let A be an n x n complex matrix
    try:
        if not isinstance(witness, sp.MatrixBase):
            A = sp.Matrix(witness)
        else:
            A = witness
        h1 = A.is_square and len(A.free_symbols) == 0
    except Exception:
        h1 = False
        A = None

    # H_2: Assume sigma_1(A) < 1
    sv_A = 0.0
    try:
        if h1:
            sv_A = max_singular_value(A)
            h2 = bool(sv_A < 1.0)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: Let I be the n x n identity matrix
    try:
        h3 = h1
    except Exception:
        h3 = False

    # ¬Q: I - A is not invertible, or sigma_1((I - A)^-1) > 1 / (1 - sigma_1(A))
    try:
        if h1 and h2:
            n = A.rows
            I = sp.eye(n)
            I_minus_A = I - A
            if I_minus_A.det() == 0:
                neg_q = True
            else:
                inv_mat = I_minus_A.inv()
                sv_inv = max_singular_value(inv_mat)
                bound = 1.0 / (1.0 - sv_A)
                # We use a small tolerance to avoid false positives due to floating point inaccuracies
                neg_q = bool(sv_inv > bound + 1e-9)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n complex matrix",
    "H_2: sigma_1(A) < 1",
    "H_3: I is the n x n identity matrix",
    "¬Q: I - A is not invertible or sigma_1((I - A)^-1) > 1 / (1 - sigma_1(A))"
]

N_HYP = 3
NEG_Q_INDEX = 3
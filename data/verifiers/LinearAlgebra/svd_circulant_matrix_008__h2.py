import sympy as sp
import math

# Top-level setup: named object bindings that the witness expression may reference.
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def to_list(vec):
    if isinstance(vec, sp.MatrixBase):
        return list(vec)
    return list(vec)

def is_circulant(C):
    if not isinstance(C, sp.MatrixBase):
        return False
    if not C.is_square:
        return False
    n = C.rows
    for i in range(n):
        for j in range(n):
            if sp.simplify(C[i, j] - C[0, (j - i) % n]) != 0:
                return False
    return True

def get_singular_values_circulant(C):
    n = C.rows
    r = [C[0, j] for j in range(n)]
    abs_vals = []
    for k in range(n):
        val = 0
        for j in range(n):
            val += r[j] * sp.exp(-2 * sp.I * sp.pi * j * k / n)
        abs_vals.append(sp.simplify(sp.Abs(val)))
    return abs_vals

def get_dft_abs(c):
    n = len(c)
    abs_vals = []
    for k in range(n):
        val = 0
        for j in range(n):
            val += c[j] * sp.exp(-2 * sp.I * sp.pi * j * k / n)
        abs_vals.append(sp.simplify(sp.Abs(val)))
    return abs_vals

def compare_multisets(list1, list2):
    if len(list1) != len(list2):
        return False
    used = [False] * len(list2)
    for val1 in list1:
        matched = False
        for i, val2 in enumerate(list2):
            if not used[i]:
                diff = sp.simplify(val1 - val2)
                if diff == 0:
                    used[i] = True
                    matched = True
                    break
                else:
                    try:
                        if abs(complex(diff.evalf())) < 1e-7:
                            used[i] = True
                            matched = True
                            break
                    except Exception:
                        pass
        if not matched:
            return False
    return True

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness must provide both the matrix C and the vector c, e.g., as a tuple (C, c) or dict.
    """
    try:
        if isinstance(witness, dict):
            C = witness.get('C')
            c = witness.get('c')
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            C, c = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
    
    # H_1: C is an n x n complex circulant matrix
    try:
        h1_ok = is_circulant(C)
    except Exception:
        h1_ok = False
        
    # neg_Q: The singular values of C are NOT exactly the absolute values of the discrete Fourier transform of the vector c
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            c_list = to_list(c)
            if len(c_list) != C.rows:
                neg_q_ok = True
            else:
                sv_C = get_singular_values_circulant(C)
                dft_c = get_dft_abs(c_list)
                match = compare_multisets(sv_C, dft_c)
                neg_q_ok = not match
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: C is an n \\times n complex circulant matrix",
    "¬Q: The singular values of C are not exactly the absolute values of the discrete Fourier transform of the vector c"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def ip(x, y, G):
    """
    Computes the inner product <x, y> with respect to metric G.
    If G is None, uses the standard Hermitian inner product.
    """
    x = sympy.Matrix(x)
    if x.shape[1] != 1:
        x = x.reshape(x.shape[0] * x.shape[1], 1)
    y = sympy.Matrix(y)
    if y.shape[1] != 1:
        y = y.reshape(y.shape[0] * y.shape[1], 1)
        
    if G is not None:
        G = sympy.Matrix(G)
        return (x.H * G * y)[0, 0]
    else:
        return (x.H * y)[0, 0]

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for Bessel's Inequality.
    The witness is expected to be a tuple: (G, e_list, v) or (e_list, v)
    where G is the inner product metric matrix (optional, defaults to identity),
    e_list is a list of orthonormal vectors, and v is a vector.
    """
    try:
        if isinstance(witness, (list, tuple)):
            if len(witness) == 3:
                G, e_list, v = witness
            elif len(witness) == 2:
                e_list, v = witness
                G = None
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: {e_1, e_2, ..., e_n} is an orthonormal set in V
    h1_ok = False
    try:
        if isinstance(e_list, (list, tuple)) and len(e_list) >= 1:
            orthonormal = True
            for i in range(len(e_list)):
                for j in range(len(e_list)):
                    val = ip(e_list[i], e_list[j], G)
                    expected = 1 if i == j else 0
                    diff = sympy.expand(val - expected)
                    if diff != 0:
                        diff = sympy.simplify(diff)
                        if diff != 0:
                            orthonormal = False
                            break
                if not orthonormal:
                    break
            h1_ok = orthonormal
    except Exception:
        h1_ok = False

    # H_2: v is a vector in V
    h2_ok = False
    try:
        v_mat = sympy.Matrix(v)
        if G is not None:
            G_mat = sympy.Matrix(G)
            dim = G_mat.shape[0]
            if G_mat.shape[0] != G_mat.shape[1]:
                dim = -1 # invalid G
        else:
            dim = v_mat.shape[0] * v_mat.shape[1]
            
        if dim > 0 and v_mat.shape[0] * v_mat.shape[1] == dim:
            dims_ok = True
            for e in e_list:
                e_mat = sympy.Matrix(e)
                if e_mat.shape[0] * e_mat.shape[1] != dim:
                    dims_ok = False
                    break
            if dims_ok:
                h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: \sum_{i=1}^n |\langle v, e_i \rangle|^2 > \|v\|^2
    neg_q_ok = False
    try:
        LHS = 0
        for e in e_list:
            val = ip(v, e, G)
            # |<v, e_i>|^2 = <v, e_i> * conjugate(<v, e_i>)
            LHS += sympy.expand(val * sympy.conjugate(val))
            
        RHS = ip(v, v, G)
        diff = sympy.simplify(LHS - RHS)
        
        if diff.is_real:
            neg_q_ok = bool(diff > 0)
        elif diff.is_real is False:
            c_diff = complex(diff)
            if abs(c_diff.imag) < 1e-9:
                neg_q_ok = c_diff.real > 1e-9
        else:
            try:
                neg_q_ok = bool(diff > 0)
            except TypeError:
                neg_q_ok = float(diff) > 1e-9
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: {e_1, e_2, ..., e_n} is an orthonormal set in V",
    "H_2: v is a vector in V",
    "¬Q: sum_{i=1}^n |<v, e_i>|^2 > ||v||^2"
]

N_HYP = 2
NEG_Q_INDEX = 2
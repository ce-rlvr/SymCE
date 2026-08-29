import sympy as sp
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture:
    "There exists a unique ordered basis F = {f_1, ..., f_n} for V such that B(e_i, f_j) = \delta_{ij}"
    
    The witness is expected to provide the bilinear form B and the set of vectors E = {e_1, ..., e_n}.
    It can be a tuple (B, E) or a dictionary {'B': B, 'E': E}.
    B should be a square matrix representing the bilinear form on V = R^m.
    E should be a list of column vectors (or a matrix whose columns are the vectors).
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            B_raw = witness.get('B')
            E_raw = witness.get('E')
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            B_raw, E_raw = witness
        else:
            B_raw, E_raw = None, None

        if B_raw is not None and E_raw is not None:
            B = sp.Matrix(B_raw)
            if B.is_square:
                m = B.shape[0]
                
                if isinstance(E_raw, sp.Matrix):
                    if E_raw.shape[0] == m:
                        h1 = True
                        n = E_raw.shape[1]
                        E_mat = E_raw
                elif isinstance(E_raw, (list, tuple)):
                    E_converted = []
                    for v in E_raw:
                        v_mat = sp.Matrix(v)
                        if v_mat.shape == (m, 1):
                            E_converted.append(v_mat)
                        elif v_mat.shape == (1, m):
                            E_converted.append(v_mat.T)
                        else:
                            raise ValueError("Vector dimension mismatch")
                    h1 = True
                    n = len(E_converted)
                    E_mat = sp.Matrix.hstack(*E_converted) if n > 0 else sp.zeros(m, 0)
    except Exception:
        pass

    try:
        if h1:
            detB = sp.simplify(B.det())
            h2 = bool(detB != 0)
    except Exception:
        pass

    try:
        if h1 and h2:
            # For F to be a basis for V, it must have exactly m elements.
            # Since F is indexed 1 to n, we must have n == m.
            if n != m:
                neg_q = True
            else:
                # The condition B(e_i, f_j) = delta_{ij} translates to E^T * B * F = I.
                # A unique basis F exists iff E^T * B is invertible.
                # Since B is non-degenerate (invertible), this holds iff E is invertible.
                detE = sp.simplify(E_mat.det())
                neg_q = bool(detE == 0)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space",
    "H_2: B is a non-degenerate bilinear form on V",
    "¬Q: There does not exist a unique adjoint basis F for V"
]

N_HYP = 2
NEG_Q_INDEX = 2
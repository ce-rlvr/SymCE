import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    "Let V and W be vector spaces over F. Let {v_1, ..., v_n} be a basis for V.
    Then there exists a unique linear map T: V -> W such that T(v_i) = w_i for all i."
    
    The dropped hypothesis is that w_1, ..., w_n must be elements of W.
    
    Expected witness format: (V_dim, W_dim, v_list, w_list)
    where V_dim and W_dim are dimensions of V and W,
    v_list is a list of n column vectors (Matrix) of shape (V_dim, 1),
    w_list is a list of n target objects.
    """
    try:
        V_dim, W_dim, v_list, w_list = witness
    except Exception:
        return [False, False, False]
    
    # H_1: V and W are vector spaces over a field F
    try:
        h1 = isinstance(V_dim, int) and V_dim >= 0 and isinstance(W_dim, int) and W_dim >= 0
    except Exception:
        h1 = False
        
    # H_2: {v_1, ..., v_n} is a basis for V
    try:
        if isinstance(v_list, (list, tuple)) and len(v_list) == V_dim:
            if V_dim == 0:
                h2 = True
            else:
                if all(isinstance(v, Matrix) and v.shape == (V_dim, 1) for v in v_list):
                    M = Matrix.hstack(*v_list)
                    h2 = (M.rank() == V_dim)
                else:
                    h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: It is NOT the case that there exists a unique linear map T: V -> W such that T(v_i) = w_i
    # The conclusion holds iff w_list contains exactly n elements, all of which are in W.
    # In our representation, an element is in W iff it is a Matrix of shape (W_dim, 1).
    try:
        if isinstance(w_list, (list, tuple)) and len(w_list) == V_dim:
            conclusion_holds = all(isinstance(w, Matrix) and w.shape == (W_dim, 1) for w in w_list)
        else:
            conclusion_holds = False
        neg_q = not conclusion_holds
    except Exception:
        neg_q = True
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V and W are vector spaces over a field F",
    "H_2: {v_1, ..., v_n} is a basis for V",
    "¬Q: There does not exist a unique linear map T: V -> W such that T(v_i) = w_i for all i"
]

N_HYP = 2
NEG_Q_INDEX = 2
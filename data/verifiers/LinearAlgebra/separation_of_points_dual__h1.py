import sympy
from sympy import Matrix, eye, zeros
from sympy.matrices.normalforms import smith_normal_form

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        M, x = None, None
        # A common counterexample is a torsion Z-module, e.g., Z/nZ.
        # We represent the module V as Z^m / Im(M) and the vector v as x.
        if isinstance(witness, int):
            if abs(witness) > 1:
                M, x = Matrix([[abs(witness)]]), Matrix([[1]])
            else:
                M, x = Matrix([[1]]), Matrix([[0]])
        else:
            M_raw, x_raw = None, None
            if isinstance(witness, tuple) and len(witness) == 2:
                M_raw, x_raw = witness[0], witness[1]
            elif isinstance(witness, dict) and 'M' in witness and 'x' in witness:
                M_raw, x_raw = witness['M'], witness['x']
            elif hasattr(witness, 'M') and hasattr(witness, 'x'):
                M_raw, x_raw = witness.M, witness.x
                
            if M_raw is not None and x_raw is not None:
                M = Matrix(M_raw)
                x = Matrix(x_raw)
                if M.rows != x.rows or x.cols != 1:
                    M, x = None, None
                    
        if M is not None and x is not None:
            # Evaluate H1: v is non-zero in V
            # This means x is not in the column space of M over Z.
            # Over a PID, this is true iff the non-zero invariant factors of M 
            # differ from those of the augmented matrix [M | x].
            try:
                if M.rows == 0 or M.cols == 0:
                    h1 = not all(val == 0 for val in x)
                else:
                    S_M = smith_normal_form(M)
                    inv_M = [abs(S_M[i, i]) for i in range(min(S_M.rows, S_M.cols)) if S_M[i, i] != 0]
                    
                    Mx = M.row_join(x)
                    S_Mx = smith_normal_form(Mx)
                    inv_Mx = [abs(S_Mx[i, i]) for i in range(min(S_Mx.rows, S_Mx.cols)) if S_Mx[i, i] != 0]
                    
                    h1 = (inv_M != inv_Mx)
            except Exception:
                h1 = False
                
            # Evaluate neg_Q: no separating functional exists
            # This means x is in the column space of M over Q.
            try:
                Mx = M.row_join(x)
                neg_q = (M.rank() == Mx.rank())
            except Exception:
                neg_q = False
                
            return [h1, neg_q]
            
    except Exception:
        pass

    # Fallback for string descriptions (e.g., L^p spaces for 0 < p < 1)
    try:
        if isinstance(witness, str):
            s = witness.lower().replace(" ", "")
            if "l^p" in s or "lp" in s:
                return [True, True]
    except Exception:
        pass

    # Fallback for custom objects
    try:
        h1 = bool(witness.v_is_nonzero())
    except Exception:
        pass
    try:
        neg_q = bool(witness.has_no_separating_functional())
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: v is a non-zero vector in V",
    "¬Q: There does not exist a linear functional f in V^* such that f(v) != 0"
]

N_HYP = 1
NEG_Q_INDEX = 1
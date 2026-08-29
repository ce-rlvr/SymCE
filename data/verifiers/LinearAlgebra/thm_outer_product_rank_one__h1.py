import sympy
from sympy import Matrix, eye, zeros, Mod
from sympy.abc import x, y, z
import itertools

# Top-level setup for witness evaluation
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: M is an m x n matrix over F",
    "¬Q: The equivalence (rank(M) = 1 iff M = u v^T for non-zero u, v) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    from sympy import MatrixBase
    
    M_obj = None
    mod_obj = None
    
    # Extract matrix and optional modulus from the witness
    if isinstance(witness, tuple) and len(witness) == 2:
        M_raw, mod_raw = witness
        try:
            M_obj = Matrix(M_raw)
            mod_obj = int(mod_raw)
        except Exception:
            M_obj = M_raw
            mod_obj = mod_raw
    else:
        try:
            M_obj = Matrix(witness)
        except Exception:
            M_obj = witness
            
    # Infer modulus from Mod elements if not explicitly provided
    if isinstance(M_obj, MatrixBase) and mod_obj is None:
        mods = M_obj.atoms(Mod)
        if mods:
            try:
                mod_obj = int(list(mods)[0].args[1])
            except Exception:
                pass
                
    # Normalize matrix elements to integers if modulus is present
    if isinstance(M_obj, MatrixBase) and mod_obj is not None:
        try:
            M_int = M_obj.applyfunc(lambda val: int(val.args[0]) if isinstance(val, Mod) else int(val))
            M_obj = M_int
        except Exception:
            pass

    # H_1: M is an m x n matrix over F
    try:
        h1 = isinstance(M_obj, MatrixBase)
    except Exception:
        h1 = False

    # Evaluate P: rank(M) == 1
    try:
        if mod_obj is not None:
            rank_M = 0
            for k in range(1, min(M_obj.rows, M_obj.cols) + 1):
                has_nonzero_minor = False
                for row_indices in itertools.combinations(range(M_obj.rows), k):
                    for col_indices in itertools.combinations(range(M_obj.cols), k):
                        subM = M_obj.extract(row_indices, col_indices)
                        det = subM.det()
                        if (det % mod_obj) != 0:
                            has_nonzero_minor = True
                            break
                    if has_nonzero_minor:
                        break
                if has_nonzero_minor:
                    rank_M = k
                else:
                    break
            P = (rank_M == 1)
        else:
            P = (M_obj.rank() == 1)
    except Exception:
        P = False

    # Evaluate Q: exists non-zero u, v such that M = u v^T
    try:
        Q = False
        if mod_obj is not None:
            m_rows, n_cols = M_obj.rows, M_obj.cols
            for u_tup in itertools.product(range(mod_obj), repeat=m_rows):
                if all(val == 0 for val in u_tup): 
                    continue
                
                valid_v_choices = []
                for j in range(n_cols):
                    choices_for_j = []
                    for v_j in range(mod_obj):
                        match_i = True
                        for i in range(m_rows):
                            if (u_tup[i] * v_j) % mod_obj != M_obj[i, j] % mod_obj:
                                match_i = False
                                break
                        if match_i:
                            choices_for_j.append(v_j)
                    valid_v_choices.append(choices_for_j)
                
                # If every column has at least one valid v_j, we can form v
                if all(len(choices) > 0 for choices in valid_v_choices):
                    # Ensure we can pick a v that is not entirely zero
                    can_be_nonzero = False
                    for choices in valid_v_choices:
                        if any(v_j != 0 for v_j in choices):
                            can_be_nonzero = True
                            break
                    if can_be_nonzero:
                        Q = True
                        break
        else:
            if M_obj.is_zero_matrix:
                Q = False
            else:
                if M_obj.rank() == 1:
                    Q = True
                else:
                    Q = False
    except Exception:
        Q = False

    # The conclusion is P <-> Q. The negation is P != Q.
    try:
        neg_Q = (P != Q)
    except Exception:
        neg_Q = False

    return [h1, neg_Q]
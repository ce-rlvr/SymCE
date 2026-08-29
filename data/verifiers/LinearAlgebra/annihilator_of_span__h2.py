import sympy
from sympy import Matrix

# Top-level setup
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def is_in_span(v, basis):
    if not basis:
        if isinstance(v, Matrix):
            return v.is_zero_matrix
        elif hasattr(v, 'is_zero'):
            return v.is_zero
        else:
            try:
                return Matrix(v).is_zero_matrix
            except Exception:
                return v == 0
            
    try:
        cols = []
        for b in basis:
            b_mat = Matrix(b)
            if b_mat.shape[1] != 1:
                b_mat = b_mat.T
            cols.append(b_mat)
        M = Matrix.hstack(*cols)
        
        v_mat = Matrix(v)
        if v_mat.shape[1] != 1:
            v_mat = v_mat.T
            
        if M.shape[0] != v_mat.shape[0]:
            return False
            
        return M.row_join(v_mat).rank() == M.rank()
    except Exception:
        pass
        
    try:
        from sympy import solve, symbols
        coeffs = symbols(f'c0:{len(basis)}')
        eq = v - sum(c*b for c, b in zip(coeffs, basis))
        if isinstance(eq, Matrix):
            eqs = list(eq)
        else:
            eqs = [eq]
        sol = solve(eqs, coeffs)
        return bool(sol)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            V = witness.get('V')
            S = witness.get('S')
        elif hasattr(witness, 'V') and hasattr(witness, 'S'):
            V = witness.V
            S = witness.S
        else:
            V, S = witness
    except Exception:
        return [False, False]
        
    h1 = False
    try:
        if isinstance(V, int) and V > 0:
            h1 = True
        elif hasattr(V, 'rank'):
            h1 = True
        elif isinstance(V, (list, tuple, set, frozenset)):
            V_list = list(V)
            if len(V_list) > 0 and not isinstance(V_list[0], (list, tuple, set, frozenset, Matrix)):
                V = [V_list]
            else:
                V = V_list
            h1 = True
        elif V is not None:
            h1 = True
    except Exception:
        pass
        
    neg_q = False
    try:
        if isinstance(S, Matrix):
            S_vecs = [S.col(i) for i in range(S.shape[1])]
        elif isinstance(S, (list, tuple, set, frozenset)):
            S_list = list(S)
            if len(S_list) > 0 and not isinstance(S_list[0], (list, tuple, set, frozenset, Matrix)):
                S_vecs = [S_list]
            else:
                S_vecs = S_list
        else:
            S_vecs = [S]
            
        is_subset = True
        
        if isinstance(V, (list, tuple)):
            try:
                if all(s in V for s in S_vecs):
                    is_subset = True
                    neg_q = False
                    return [bool(h1), bool(neg_q)]
            except Exception:
                pass

        if isinstance(V, int):
            for s in S_vecs:
                s_mat = Matrix(s)
                if len(s_mat) != V:
                    is_subset = False
                    break
        elif hasattr(V, 'rank'):
            basis = [V.col(i) for i in range(V.shape[1])]
            for s in S_vecs:
                if not is_in_span(s, basis):
                    is_subset = False
                    break
        elif isinstance(V, (list, tuple)):
            for s in S_vecs:
                if not is_in_span(s, V):
                    is_subset = False
                    break
        else:
            is_subset = False
            
        neg_q = not is_subset
    except Exception:
        neg_q = True
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "¬Q: The annihilator of S is not equal to the annihilator of the subspace spanned by S"
]

N_HYP = 1
NEG_Q_INDEX = 1
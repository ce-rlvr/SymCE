import sympy
import itertools

# Top-level setup for Linear Algebra
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def rank_mod_p(M, p):
    M = M.copy()
    rows, cols = M.shape
    rank = 0
    for c in range(cols):
        pivot = None
        for r in range(rank, rows):
            if M[r, c] % p != 0:
                pivot = r
                break
        if pivot is not None:
            if pivot != rank:
                M.row_swap(pivot, rank)
            inv = sympy.mod_inverse(M[rank, c], p)
            for j in range(c, cols):
                M[rank, j] = (M[rank, j] * inv) % p
            for r in range(rows):
                if r != rank and M[r, c] % p != 0:
                    factor = M[r, c]
                    for j in range(c, cols):
                        M[r, j] = (M[r, j] - factor * M[rank, j]) % p
            rank += 1
    return rank

def nullspace_mod_p(M, p):
    M = M.copy().applyfunc(lambda x: x % p)
    rows, cols = M.shape
    rank = 0
    pivots = []
    for c in range(cols):
        pivot = None
        for r in range(rank, rows):
            if M[r, c] % p != 0:
                pivot = r
                break
        if pivot is not None:
            if pivot != rank:
                M.row_swap(pivot, rank)
            inv = sympy.mod_inverse(M[rank, c], p)
            for j in range(c, cols):
                M[rank, j] = (M[rank, j] * inv) % p
            for r in range(rows):
                if r != rank and M[r, c] % p != 0:
                    factor = M[r, c]
                    for j in range(c, cols):
                        M[r, j] = (M[r, j] - factor * M[rank, j]) % p
            pivots.append(c)
            rank += 1
            
    free_vars = [c for c in range(cols) if c not in pivots]
    null_basis = []
    for free_var in free_vars:
        vec = sympy.zeros(cols, 1)
        vec[free_var, 0] = 1
        for i, piv in enumerate(pivots):
            vec[piv, 0] = (-M[i, free_var]) % p
        null_basis.append(vec)
    return null_basis

def inner_product(u, v, A=None, p=None):
    is_complex = any(e.has(sympy.I) for e in u) or any(e.has(sympy.I) for e in v)
    u_adj = u.H if is_complex else u.T
    if A is not None:
        val = (u_adj * A * v)[0, 0]
    else:
        val = (u_adj * v)[0, 0]
    if p is not None:
        val = val % p
    return sympy.simplify(val)

def is_orthonormal(S, A=None, p=None):
    for i in range(len(S)):
        for j in range(len(S)):
            val = inner_product(S[i], S[j], A, p)
            expected = 1 if i == j else 0
            if p is not None:
                if (val - expected) % p != 0:
                    return False
            else:
                if sympy.simplify(val - expected) != 0:
                    return False
    return True

def is_in_span(v, V_basis, p=None):
    if isinstance(V_basis, str):
        return True
    if not V_basis:
        return False
    M = sympy.Matrix.hstack(*V_basis)
    if p is not None:
        M_mod = sympy.Matrix(M).applyfunc(lambda x: x % p)
        M_aug = sympy.Matrix.hstack(M_mod, sympy.Matrix(v).applyfunc(lambda x: x % p))
        return rank_mod_p(M_mod, p) == rank_mod_p(M_aug, p)
    else:
        return M.rank() == sympy.Matrix.hstack(M, v).rank()

def conditions(witness):
    try:
        S = []
        V_basis = []
        A = None
        p = None
        
        if isinstance(witness, dict):
            S = witness.get('S', [])
            V_basis = witness.get('V', [])
            A = witness.get('A', None)
            p = witness.get('p', None)
        elif isinstance(witness, tuple):
            if isinstance(witness[0], str):
                V_basis = witness[0]
                S = witness[1]
                A = witness[2] if len(witness) > 2 else None
                p = witness[3] if len(witness) > 3 else None
            else:
                if len(witness) == 2:
                    S, V_basis = witness
                elif len(witness) == 3:
                    S, V_basis, A = witness
                elif len(witness) == 4:
                    S, V_basis, A, p = witness
        else:
            S = witness
            V_basis = []

        if not isinstance(S, (list, tuple)):
            S = [S]
            
        if not V_basis and S and hasattr(S[0], 'shape'):
            n = S[0].shape[0]
            V_basis = [sympy.zeros(n, 1) for _ in range(n)]
            for i in range(n):
                V_basis[i][i, 0] = 1
                
        if isinstance(V_basis, sympy.Matrix):
            V_basis = [V_basis[:, i] for i in range(V_basis.shape[1])]
            
        if not S:
            if not V_basis:
                return [False, False]
                
        h1_in_V = True
        for v in S:
            if not is_in_span(v, V_basis, p):
                h1_in_V = False
                break
                
        h1_ortho = is_orthonormal(S, A, p)
        h1 = h1_in_V and h1_ortho
        
        if isinstance(V_basis, str):
            if V_basis in ["l2", "l_2", "Hilbert", "R[x]", "R[X]"]:
                return [bool(h1), True]
            else:
                return [bool(h1), False]
                
        M = sympy.Matrix.hstack(*V_basis)
        if S:
            S_mat = sympy.Matrix.hstack(*S)
            is_complex = any(e.has(sympy.I) for e in S_mat) or any(e.has(sympy.I) for e in M)
            S_adj = S_mat.H if is_complex else S_mat.T
            
            if A is not None:
                Eq_mat = S_adj * A * M
            else:
                Eq_mat = S_adj * M
                
            if p is not None:
                Eq_mat = sympy.Matrix(Eq_mat).applyfunc(lambda x: x % p)
                null_c = nullspace_mod_p(Eq_mat, p)
                W_basis = [(M * c).applyfunc(lambda x: x % p) for c in null_c]
            else:
                null_c = Eq_mat.nullspace()
                W_basis = [M * c for c in null_c]
        else:
            W_basis = V_basis
            
        if not W_basis:
            neg_Q = False
        else:
            if p is not None:
                dim_W = len(W_basis)
                W_mat = sympy.Matrix.hstack(*W_basis)
                W_elements = []
                for coeffs in itertools.product(range(p), repeat=dim_W):
                    c_vec = sympy.Matrix(coeffs)
                    v = (W_mat * c_vec).applyfunc(lambda x: x % p)
                    W_elements.append(v)
                
                norm1_W = []
                for v in W_elements:
                    if inner_product(v, v, A, p) == 1:
                        norm1_W.append(v)
                        
                def find_ortho_basis(current_basis, remaining_dim):
                    if remaining_dim == 0:
                        return True
                    for v in norm1_W:
                        is_ortho = True
                        for u in current_basis:
                            if inner_product(u, v, A, p) != 0:
                                is_ortho = False
                                break
                        if is_ortho:
                            if find_ortho_basis(current_basis + [v], remaining_dim - 1):
                                return True
                    return False
                
                has_ortho_basis = find_ortho_basis([], dim_W)
                neg_Q = not has_ortho_basis
            else:
                is_complex = False
                for v in W_basis:
                    if any(e.has(sympy.I) for e in v):
                        is_complex = True
                        break
                
                W_mat = sympy.Matrix.hstack(*W_basis)
                if A is not None:
                    Restricted_A = W_mat.H * A * W_mat if is_complex else W_mat.T * A * W_mat
                else:
                    Restricted_A = W_mat.H * W_mat if is_complex else W_mat.T * W_mat
                    
                if is_complex:
                    neg_Q = sympy.simplify(Restricted_A.det()) == 0
                else:
                    is_pos_def = True
                    try:
                        if Restricted_A.is_positive_definite is False:
                            is_pos_def = False
                        elif Restricted_A.is_positive_definite is None:
                            for i in range(1, Restricted_A.shape[0] + 1):
                                minor = sympy.simplify(Restricted_A[:i, :i].det())
                                try:
                                    if bool(minor <= 0):
                                        is_pos_def = False
                                        break
                                except TypeError:
                                    pass
                    except Exception:
                        for i in range(1, Restricted_A.shape[0] + 1):
                            minor = sympy.simplify(Restricted_A[:i, :i].det())
                            try:
                                if bool(minor <= 0):
                                    is_pos_def = False
                                    break
                            except TypeError:
                                pass
                    neg_Q = not is_pos_def

        return [bool(h1), bool(neg_Q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: S is an orthonormal set of vectors in V",
    "¬Q: S cannot be extended to an orthonormal basis of V"
]

N_HYP = 1
NEG_Q_INDEX = 1
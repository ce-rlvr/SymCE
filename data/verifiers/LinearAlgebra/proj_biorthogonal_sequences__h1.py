import sympy as sp
from sympy import Matrix, eye, zeros, symbols

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        U = [Matrix(u) for u in witness['U']]
        V = [Matrix(v) for v in witness['V']]
        P = Matrix(witness['P'])
        inner_product = witness.get('inner_product', lambda x, y: x.dot(y))
    except Exception:
        return [False, False, False]

    k = len(U)
    if k == 0 or len(V) != k:
        return [False, False, False]

    # H1: biorthogonality
    h1 = True
    try:
        for i in range(k):
            for j in range(k):
                val = inner_product(U[i], V[j])
                if isinstance(val, Matrix) or hasattr(val, 'shape'):
                    val = val[0, 0] if val.shape == (1, 1) else val
                expected = 1 if i == j else 0
                if sp.simplify(val - expected) != 0:
                    h1 = False
                    break
            if not h1:
                break
    except Exception:
        h1 = False

    # H2: P(x) = sum <x, v_i> u_i
    h2 = True
    try:
        n = U[0].shape[0]
        if P.shape != (n, n):
            h2 = False
        else:
            x_syms = symbols(f'x0:{n}')
            x_vec = Matrix(n, 1, x_syms)
            
            Px_formula = zeros(n, 1)
            for i in range(k):
                coeff = inner_product(x_vec, V[i])
                if isinstance(coeff, Matrix) or hasattr(coeff, 'shape'):
                    coeff = coeff[0, 0] if coeff.shape == (1, 1) else coeff
                Px_formula += coeff * U[i]
                
            Px_matrix = P * x_vec
            
            diff = Px_matrix - Px_formula
            diff = diff.expand()
            if not all(sp.simplify(e) == 0 for e in diff):
                h2 = False
    except Exception:
        h2 = False

    # Conclusion: P is an idempotent projection onto the span of U
    neg_q = False
    try:
        # 1. P is idempotent: P^2 == P
        diff_P = (P * P - P).expand()
        is_idempotent = all(sp.simplify(e) == 0 for e in diff_P)
        
        # 2. Im(P) == span(U)
        U_mat = Matrix.hstack(*U)
        rank_U = U_mat.rank()
        rank_P = P.rank()
        P_U_mat = Matrix.hstack(P, U_mat)
        rank_P_U = P_U_mat.rank()
        
        is_onto_span = (rank_P == rank_U) and (rank_P_U == rank_U)
        
        q = is_idempotent and is_onto_span
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Sequences u and v satisfy biorthogonality <u_i, v_j> = delta_ij",
    "H_2: P is a linear operator defined by P(x) = sum <x, v_i> u_i",
    "¬Q: P is NOT an idempotent projection operator onto the span of {u_1, ..., u_k}"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "H_2: T* is the adjoint operator of T",
    "¬Q: ||T*T|| != ||T||^2"
]

N_HYP = 2
NEG_Q_INDEX = 2

def operator_norm(M, p):
    if p == 1 or str(p) == '1':
        return max([sum([sympy.Abs(M[i, j]) for i in range(M.rows)]) for j in range(M.cols)])
    elif p == sympy.oo or str(p) == 'oo' or str(p) == 'inf':
        return max([sum([sympy.Abs(M[i, j]) for j in range(M.cols)]) for i in range(M.rows)])
    elif p == 2 or str(p) == '2':
        M_H_M = M.H * M
        evals = M_H_M.eigenvals()
        max_eval = max([sympy.re(e) for e in evals.keys()])
        return sympy.sqrt(max_eval)
    else:
        raise ValueError(f"Unsupported operator norm: {p}")

def conditions(witness):
    h1_ok = False
    h2_ok = False
    neg_q = False
    
    T = None
    T_star = None
    p = 1
    G = None
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                T, T_star, p = witness
            elif len(witness) == 2:
                T, p = witness
            elif len(witness) == 1:
                T = witness[0]
        elif isinstance(witness, dict):
            T = witness.get('T')
            T_star = witness.get('T_star')
            p = witness.get('p', 1)
            G = witness.get('G')
        else:
            T = witness
    except Exception:
        pass

    try:
        if not hasattr(T, 'is_square'):
            T = sympy.Matrix(T)
        if hasattr(T, 'is_square') and T.is_square and hasattr(T, 'H'):
            h1_ok = True
    except Exception:
        pass

    try:
        if h1_ok:
            if G is not None:
                if not hasattr(G, 'is_square'):
                    G = sympy.Matrix(G)
                if G.is_square:
                    expected_T_star = G.inv() * T.H * G
                else:
                    expected_T_star = T.H
            else:
                expected_T_star = T.H
            
            if T_star is not None:
                if not hasattr(T_star, 'is_square'):
                    T_star = sympy.Matrix(T_star)
                if T_star == expected_T_star or T_star.equals(expected_T_star):
                    h2_ok = True
            else:
                T_star = expected_T_star
                h2_ok = True
    except Exception:
        pass

    try:
        if h1_ok and h2_ok:
            norm_T = operator_norm(T, p)
            norm_T_star_T = operator_norm(T_star * T, p)
            
            diff = sympy.simplify(norm_T_star_T - norm_T**2)
            try:
                diff_float = float(diff)
                if abs(diff_float) > 1e-9:
                    neg_q = True
            except TypeError:
                if diff != 0:
                    neg_q = True
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q]
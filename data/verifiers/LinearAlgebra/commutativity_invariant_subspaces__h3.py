import sympy as sp
from sympy import eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V is a vector space",
    "H_2: P is a projection operator on V",
    "¬Q: The equivalence (A commutes with P iff range and kernel of P are invariant under A) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # Parse witness
        if isinstance(witness, tuple) and len(witness) == 2:
            A_mat, P_mat = witness
            if hasattr(A_mat, 'shape') and hasattr(P_mat, 'shape'):
                if A_mat.shape == P_mat.shape and A_mat.shape[0] == A_mat.shape[1]:
                    n = A_mat.shape[0]
                    vars_syms = sp.symbols(f'x0:{n}')
                    A_exprs = tuple(A_mat * sp.Matrix(vars_syms))
                    P_exprs = tuple(P_mat * sp.Matrix(vars_syms))
                else:
                    return [False, False, False]
            else:
                return [False, False, False]
        elif isinstance(witness, tuple) and len(witness) == 3:
            A_in, P_in, vars_in = witness
            if isinstance(vars_in, int):
                n = vars_in
                if n <= 0:
                    return [False, False, False]
                vars_syms = sp.symbols(f'x0:{n}')
                if callable(A_in) and callable(P_in):
                    A_res = A_in(*vars_syms)
                    P_res = P_in(*vars_syms)
                    A_exprs = tuple(A_res) if isinstance(A_res, (list, tuple)) else (A_res,)
                    P_exprs = tuple(P_res) if isinstance(P_res, (list, tuple)) else (P_res,)
                else:
                    return [False, False, False]
            else:
                if not isinstance(vars_in, (list, tuple)):
                    vars_in = [vars_in]
                vars_syms = tuple(sp.sympify(v) for v in vars_in)
                if callable(A_in) and callable(P_in):
                    A_res = A_in(*vars_syms)
                    P_res = P_in(*vars_syms)
                    A_exprs = tuple(A_res) if isinstance(A_res, (list, tuple)) else (A_res,)
                    P_exprs = tuple(P_res) if isinstance(P_res, (list, tuple)) else (P_res,)
                else:
                    A_exprs = tuple(A_in) if isinstance(A_in, (list, tuple)) else (A_in,)
                    P_exprs = tuple(P_in) if isinstance(P_in, (list, tuple)) else (P_in,)
        else:
            return [False, False, False]

        # H1: V is a vector space (represented by a valid dimension > 0)
        h1_ok = False
        if len(vars_syms) > 0 and len(A_exprs) == len(vars_syms) and len(P_exprs) == len(vars_syms):
            h1_ok = True

        if not h1_ok:
            return [False, False, False]

        def apply_trans(exprs, v):
            subs_pairs = list(zip(vars_syms, v))
            return tuple(sp.sympify(e).subs(subs_pairs, simultaneous=True) for e in exprs)

        def is_zero(expr):
            return sp.simplify(sp.expand(expr)) == 0

        # H2: P is a projection operator
        P_v = apply_trans(P_exprs, vars_syms)
        P_P_v = apply_trans(P_exprs, P_v)
        
        h2_ok = True
        for e1, e2 in zip(P_P_v, P_v):
            if not is_zero(e1 - e2):
                h2_ok = False
                break

        # Conclusion: A commutes with P iff (Im(P) invariant and Ker(P) invariant)
        A_v = apply_trans(A_exprs, vars_syms)
        A_P_v = apply_trans(A_exprs, P_v)
        P_A_v = apply_trans(P_exprs, A_v)
        
        commutes = True
        for e1, e2 in zip(A_P_v, P_A_v):
            if not is_zero(e1 - e2):
                commutes = False
                break

        P_A_P_v = apply_trans(P_exprs, A_P_v)
        inv_range = True
        for e1, e2 in zip(P_A_P_v, A_P_v):
            if not is_zero(e1 - e2):
                inv_range = False
                break

        v_minus_P_v = tuple(sp.simplify(v - p) for v, p in zip(vars_syms, P_v))
        A_ker = apply_trans(A_exprs, v_minus_P_v)
        P_A_ker = apply_trans(P_exprs, A_ker)
        
        inv_kernel = True
        for e in P_A_ker:
            if not is_zero(e):
                inv_kernel = False
                break

        Q = (commutes == (inv_range and inv_kernel))
        neg_Q = not Q

        return [h1_ok, h2_ok, neg_Q]

    except Exception:
        return [False, False, False]
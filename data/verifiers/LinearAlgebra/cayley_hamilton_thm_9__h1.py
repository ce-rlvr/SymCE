import sympy
from sympy import Matrix, eye, zeros, Symbol, simplify, expand, degree
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V is a vector space over F of finite dimension n",
    "H_2: T is a linear operator from V to V",
    "H_3: p(t) is the characteristic polynomial of T",
    "¬Q: p(T) is not the zero operator on V"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    T = None
    p_expr = None
    t_sym = None
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                T, p_expr, t_sym = witness
            elif len(witness) == 2:
                T, p_expr = witness
                t_sym = Symbol('t')
        else:
            T = witness
            t_sym = Symbol('t')
            p_expr = T.charpoly(t_sym).as_expr()
    except Exception:
        pass

    try:
        h1 = isinstance(T, MatrixBase)
    except Exception:
        h1 = False

    try:
        h2 = h1 and T.is_square
    except Exception:
        h2 = False

    try:
        cp = T.charpoly(t_sym).as_expr()
        h3 = expand(p_expr - cp) == 0
    except Exception:
        h3 = False

    try:
        p_expr_exp = expand(p_expr)
        n = T.shape[0]
        p_T = zeros(n, n)
        if p_expr_exp == 0:
            pass
        else:
            d = int(degree(p_expr_exp, t_sym))
            for power in range(d + 1):
                if power == 0:
                    coeff = p_expr_exp.subs(t_sym, 0)
                else:
                    coeff = p_expr_exp.coeff(t_sym, power)
                p_T += coeff * (T ** power)
        
        p_T_exp = p_T.applyfunc(expand)
        if p_T_exp.is_zero_matrix:
            neg_q = False
        else:
            p_T_simp = p_T_exp.applyfunc(simplify)
            neg_q = not p_T_simp.is_zero_matrix
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]
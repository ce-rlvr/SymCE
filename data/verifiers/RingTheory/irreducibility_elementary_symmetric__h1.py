import sympy
from itertools import combinations

CONDITION_LABELS = ["H_1: n >= 2 is an integer", "H_2: k is an integer such that 1 <= k <= n", "H_3: e_k is the k-th elementary symmetric polynomial", "¬Q: e_k is reducible"]
N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                n, k = witness
                expr = None
            elif len(witness) == 3:
                n, k, expr = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        n_val = int(n)
        h1 = (n_val >= 2) and (n_val == n)
    except Exception:
        h1 = False

    try:
        k_val = int(k)
        h2 = (1 <= k_val <= n_val) and (k_val == k)
    except Exception:
        h2 = False

    h3 = False
    neg_q = False

    try:
        if h1 and h2:
            X = sympy.symbols(f'x1:{n_val+1}')
            expected_e_k = sum(sympy.Mul(*c) for c in combinations(X, k_val))
            
            if expr is not None:
                if isinstance(expr, str):
                    expr_sym = sympy.sympify(expr)
                else:
                    expr_sym = expr
                h3 = bool(sympy.simplify(expr_sym - expected_e_k) == 0)
                poly_to_check = expr_sym
            else:
                h3 = True
                poly_to_check = expected_e_k
            
            if h3:
                if n_val > 10:
                    neg_q = False
                else:
                    f_list = sympy.factor_list(poly_to_check)
                    total_factors = sum(power for factor, power in f_list[1] if not factor.is_number)
                    neg_q = (total_factors >= 2)
    except Exception:
        pass

    return [h1, h2, h3, neg_q]
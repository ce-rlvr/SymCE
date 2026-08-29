import sympy
from sympy import Symbol

x = Symbol('x')

CONDITION_LABELS = [
    "H_1: a_1, a_2, ..., a_n are distinct integers",
    "H_2: f(x) = (x-a_1)(x-a_2)...(x-a_n) - 1",
    "¬Q: f(x) is not irreducible over Q"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    # Parse witness
    try:
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], (list, tuple)):
            a_list, f_expr = witness
        else:
            a_list = witness
            f_expr = 1
            for a in a_list:
                f_expr *= (x - a)
            f_expr -= 1
    except Exception:
        return [False, False, False]

    # H_1: a_1, a_2, ..., a_n are distinct integers
    try:
        h1 = True
        if not isinstance(a_list, (list, tuple)):
            h1 = False
        else:
            for a in a_list:
                if not isinstance(a, (int, sympy.Integer)):
                    h1 = False
                    break
            if h1:
                h1 = len(a_list) == len(set(a_list))
    except Exception:
        h1 = False

    # H_2: f(x) = (x-a_1)(x-a_2)...(x-a_n) - 1
    try:
        expected_f = 1
        for a in a_list:
            expected_f *= (x - a)
        expected_f -= 1
        
        diff = sympy.simplify(f_expr - expected_f)
        h2 = (diff == 0)
    except Exception:
        h2 = False

    # ¬Q: f(x) is not irreducible over Q
    try:
        f_simp = sympy.simplify(f_expr)
        if f_simp == 0:
            neg_q = True
        else:
            factors = sympy.factor_list(f_simp, domain='QQ')
            # factors[1] contains a list of (factor, multiplicity) tuples for non-constant factors
            if len(factors[1]) == 0:
                is_irred = False
            elif len(factors[1]) == 1 and factors[1][0][1] == 1:
                is_irred = True
            else:
                is_irred = False
            neg_q = not is_irred
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]
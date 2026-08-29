import sympy
from sympy import expand, Add, Pow, Symbol, ZZ, QQ
from sympy.abc import x, y, z

def is_in_laurent_ring(expr, R, x_sym):
    expr_exp = expand(expr)
    if expr_exp == 0:
        return True
    if isinstance(expr_exp, Add):
        terms = expr_exp.args
    else:
        terms = [expr_exp]
        
    for term in terms:
        coeff, power = term.as_independent(x_sym, as_Add=False)
        if not (power == 1 or power == x_sym or (isinstance(power, Pow) and power.base == x_sym and power.exp.is_integer)):
            return False
        try:
            if hasattr(R, 'from_sympy'):
                _ = R.from_sympy(coeff)
        except Exception:
            return False
    return True

def reduce_in_R(expr, R, x_sym):
    expr_exp = expand(expr)
    if expr_exp == 0:
        return sympy.Integer(0)
    if isinstance(expr_exp, Add):
        terms = expr_exp.args
    else:
        terms = [expr_exp]
        
    reduced_terms = []
    for term in terms:
        coeff, power = term.as_independent(x_sym, as_Add=False)
        try:
            if hasattr(R, 'from_sympy'):
                r_coeff = R.from_sympy(coeff)
                if r_coeff != R.zero:
                    sym_coeff = R.to_sympy(r_coeff)
                    reduced_terms.append(sym_coeff * power)
            else:
                reduced_terms.append(term)
        except Exception:
            reduced_terms.append(term)
    if not reduced_terms:
        return sympy.Integer(0)
    return Add(*reduced_terms)

def is_unit_in_R(coeff, R):
    try:
        if hasattr(R, 'from_sympy') and hasattr(R, 'is_unit'):
            r_coeff = R.from_sympy(coeff)
            return R.is_unit(r_coeff)
    except Exception:
        pass
    try:
        inv = sympy.S(1) / coeff
        if hasattr(R, 'from_sympy'):
            _ = R.from_sympy(inv)
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        if len(witness) == 4:
            R, u, v, x_sym = witness
        elif len(witness) == 3:
            R, u, v = witness
            x_sym = sympy.Symbol('x')
        elif len(witness) == 2:
            R, u = witness
            v = None
            x_sym = sympy.Symbol('x')
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(getattr(R, 'is_domain', False))
    except Exception:
        h1 = False

    h2 = True

    try:
        if v is not None:
            if not is_in_laurent_ring(u, R, x_sym) or not is_in_laurent_ring(v, R, x_sym):
                is_unit = False
            else:
                uv_minus_1 = reduce_in_R(u * v - 1, R, x_sym)
                is_unit = (uv_minus_1 == 0)
        else:
            is_unit = False
        
        u_reduced = reduce_in_R(u, R, x_sym)
        is_axk = False
        if u_reduced != 0 and not isinstance(u_reduced, Add):
            coeff, expr = u_reduced.as_independent(x_sym, as_Add=False)
            if expr == 1 or expr == x_sym or (isinstance(expr, Pow) and expr.base == x_sym and expr.exp.is_integer):
                is_axk = is_unit_in_R(coeff, R)
                
        neg_q = is_unit and not is_axk
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: Ring is Laurent polynomials over R",
    "¬Q: u is a unit but not of the form a*x^k"
]

N_HYP = 2
NEG_Q_INDEX = 2
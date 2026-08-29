import sympy
from sympy.calculus.util import function_range

# Top-level setup
x, y, z = sympy.symbols('x y z')

CONDITION_LABELS = [
    "H_1: K is a non-empty compact subset of R^n",
    "¬Q: f does not attain its infimum on K"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                K, f = witness
                if isinstance(f, sympy.Lambda):
                    x_var = f.variables[0]
                    expr = f.expr
                else:
                    x_var = None
                    expr = None
            elif len(witness) == 3:
                K, expr, x_var = witness
                if isinstance(expr, sympy.Lambda):
                    x_var = expr.variables[0]
                    expr = expr.expr
            else:
                K, expr, x_var = None, None, None
        else:
            K, expr, x_var = None, None, None
    except Exception:
        return [False, False]

    # H_1: K is a non-empty compact subset of R^n
    try:
        if isinstance(K, sympy.Set):
            if not K.is_empty and K.is_subset(sympy.S.Reals):
                if K.is_bounded == True and K.is_closed == True:
                    h1 = True
    except Exception:
        h1 = False

    # neg_Q: f does not attain its infimum on K
    try:
        if h1 and expr is not None and x_var is not None:
            expr = sympy.sympify(expr)
            if expr.free_symbols - {x_var}:
                return [h1, False]

            if isinstance(K, sympy.FiniteSet):
                neg_q = False
                return [h1, neg_q]

            rng = function_range(expr, x_var, K)
            if type(rng).__name__ not in ('ImageSet', 'ConditionSet'):
                inf_val = rng.inf
                if inf_val == -sympy.oo:
                    neg_q = True
                else:
                    is_in = inf_val in rng
                    if is_in == False or is_in is sympy.S.false:
                        neg_q = True
                    elif is_in == True or is_in is sympy.S.true:
                        neg_q = False
                    else:
                        sols = sympy.solveset(sympy.Eq(expr, inf_val), x_var, domain=K)
                        if sols is sympy.S.EmptySet:
                            neg_q = True
                        else:
                            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]
import sympy

x = sympy.Symbol('x')

def conditions(witness):
    try:
        if isinstance(witness, int) and witness > 0:
            poly = x**witness - 1
            factors = sympy.factor_list(poly, domain='QQ')[1]
            degrees = sorted([f[0].as_poly(x).degree() for f in factors])
            is_iso = (degrees == [1, 1, 2])
            return [not is_iso]
            
        if isinstance(witness, sympy.Expr):
            factors = sympy.factor_list(witness, domain='QQ')[1]
            degrees = sorted([f[0].as_poly(x).degree() for f in factors])
            is_iso = (degrees == [1, 1, 2])
            return [not is_iso]
    except Exception:
        pass

    return [True]

CONDITION_LABELS = ["not Q: The factor ring is not isomorphic to Q x Q x Q(i)"]

N_HYP = 0
NEG_Q_INDEX = 0
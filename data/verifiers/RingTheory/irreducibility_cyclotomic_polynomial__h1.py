import sympy
from sympy import Symbol

x = Symbol('x')

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    poly = None
    
    try:
        val = sympy.sympify(witness)
        try:
            p = int(val)
            is_int = (p == val)
        except TypeError:
            is_int = False
            
        if is_int:
            if p >= 2:
                h1 = True
                poly = sum(x**i for i in range(p))
        else:
            p = sympy.degree(val, gen=x) + 1
            if p >= 2:
                expected = sum(x**i for i in range(p))
                if sympy.expand(val - expected) == 0:
                    h1 = True
                    poly = val
    except Exception:
        pass

    try:
        if h1 and poly is not None:
            factors = sympy.factor_list(poly)
            # A polynomial is irreducible if it has exactly one factor with multiplicity 1
            is_irreducible = (len(factors[1]) == 1 and factors[1][0][1] == 1)
            neg_q = not is_irreducible
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Phi_p(x) = x^{p-1} + x^{p-2} + ... + x + 1 is the p-th cyclotomic polynomial",
    "¬Q: Phi_p(x) is not irreducible over Q"
]

N_HYP = 1
NEG_Q_INDEX = 1
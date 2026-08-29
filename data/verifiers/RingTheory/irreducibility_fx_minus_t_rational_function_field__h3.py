import sympy
from sympy import symbols, Poly, factor_list

X, T = symbols('X T')

def conditions(witness):
    try:
        p_witness = Poly(witness, X)
        h1 = True
        h2 = True
    except Exception:
        h1 = False
        h2 = False

    try:
        if not h1:
            neg_q = False
        else:
            expr = witness - T
            p = Poly(expr, X)
            
            if p.is_zero or p.degree() <= 0:
                is_irred = False
            else:
                coeff, factors = factor_list(expr, X)
                
                non_trivial_factors = 0
                for factor, mult in factors:
                    if Poly(factor, X).degree() >= 1:
                        non_trivial_factors += mult
                
                if non_trivial_factors == 1:
                    is_irred = True
                else:
                    is_irred = False
                    
            neg_q = not is_irred
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: T is a transcendental element over K",
    "¬Q: f(X) - T is not irreducible"
]

N_HYP = 2
NEG_Q_INDEX = 2
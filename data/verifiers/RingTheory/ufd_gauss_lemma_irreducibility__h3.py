import sympy
from sympy import factor_list, Symbol, sympify
from sympy.ntheory import factorint

x = Symbol('x')
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple):
            f = witness[-1]
            if len(witness) == 3:
                R, F, _ = witness
                if str(R) in ('ZZ', 'Z', 'Integers'):
                    h1 = True
                if str(F) in ('QQ', 'Q', 'Rationals'):
                    h2 = True
            else:
                h1 = True
                h2 = True
        else:
            f = witness
            h1 = True
            h2 = True
    except Exception:
        return [False, False, False, False]

    if not (h1 and h2):
        return [h1, h2, False, False]

    try:
        f_sym = sympify(f)
        free = f_sym.free_symbols
        if len(free) > 1:
            h3 = False
        else:
            var = list(free)[0] if free else Symbol('x')
            coeff, factors = factor_list(f_sym, var, domain='ZZ')
            c = abs(int(coeff))
            if c != 0:
                prime_factors_count = sum(factorint(c).values())
                poly_factors_count = sum(mult for _, mult in factors)
                h3 = (prime_factors_count + poly_factors_count) == 1
    except Exception:
        h3 = False

    try:
        f_sym = sympify(f)
        free = f_sym.free_symbols
        if len(free) > 1:
            neg_q = False
        else:
            var = list(free)[0] if free else Symbol('x')
            coeff, factors = factor_list(f_sym, var, domain='QQ')
            poly_factors_count = sum(mult for _, mult in factors)
            is_irred_Q = (poly_factors_count == 1)
            neg_q = not is_irred_Q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    'H_1: R is a unique factorization domain',
    'H_2: F is the field of fractions of R',
    'H_3: f is irreducible over R',
    '¬Q: f is not irreducible over F'
]

N_HYP = 3
NEG_Q_INDEX = 3
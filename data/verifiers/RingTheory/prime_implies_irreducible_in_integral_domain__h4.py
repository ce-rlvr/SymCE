import sympy
from sympy import sympify, factor_list, isprime
from sympy.polys.domains import ZZ, QQ, Domain
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: p is a non-zero element of R",
    "H_3: p is not a unit in R",
    "¬Q: p is not an irreducible element of R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def check_irreducible(R, p_sym):
    if hasattr(R, 'is_Field') and R.is_Field:
        return False
        
    if R == ZZ:
        return isprime(abs(int(p_sym)))
        
    try:
        coeff, factors = factor_list(p_sym, domain=R)
        if len(factors) == 1 and factors[0][1] == 1:
            coeff_R = R.from_sympy(sympify(coeff))
            try:
                R.exquo(R.one, coeff_R)
                return True
            except Exception:
                return False
        elif len(factors) == 0:
            if hasattr(R, 'domain'):
                return check_irreducible(R.domain, sympify(coeff))
            return False
        else:
            return False
    except Exception:
        pass
        
    return False

def conditions(witness):
    # Parse witness: can be a tuple (R, p) or just p (defaulting to ZZ)
    if isinstance(witness, tuple) and len(witness) == 2:
        R, p = witness
    else:
        R, p = ZZ, witness
        
    # H_1: R is an integral domain
    try:
        h1 = isinstance(R, Domain)
    except Exception:
        h1 = False
        
    # H_2: p is a non-zero element of R
    try:
        p_sym = sympify(p)
        p_R = R.from_sympy(p_sym)
        h2 = (p_R is not None) and (p_R != R.zero)
    except Exception:
        h2 = False
        
    # H_3: p is not a unit in R
    try:
        if not h2:
            h3 = False
        else:
            try:
                R.exquo(R.one, p_R)
                is_unit = True
            except Exception:
                is_unit = False
            h3 = not is_unit
    except Exception:
        h3 = False
        
    # ¬Q: p is not an irreducible element of R
    try:
        if not h2:
            neg_q = False
        else:
            is_irred = check_irreducible(R, p_sym)
            neg_q = not is_irred
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]
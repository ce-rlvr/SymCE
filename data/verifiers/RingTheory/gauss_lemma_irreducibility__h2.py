import sympy
from sympy import Poly
from sympy.abc import x, y, z

def parse_witness(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        R_in, f_in = witness
        if isinstance(f_in, sympy.Poly):
            f = f_in.set_domain(R_in)
        else:
            f = sympy.Poly(f_in, domain=R_in)
        R = f.domain
    elif isinstance(witness, sympy.Poly):
        f = witness
        R = f.domain
    else:
        f = sympy.Poly(witness)
        R = f.domain
    return R, f

def conditions(witness) -> list[bool]:
    try:
        R, f = parse_witness(witness)
    except Exception:
        return [False, False, False, False, False]

    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(f, sympy.Poly) and len(f.gens) <= 1
    except Exception:
        h2 = False

    try:
        h3 = bool(f.degree() >= 1)
    except Exception:
        h3 = False

    try:
        c = f.content()
        try:
            R.exquo(R.one, c)
            h4 = True
        except Exception:
            h4 = False
    except Exception:
        h4 = False

    try:
        F = R.get_field()
        
        c_R, factors_R = sympy.factor_list(f, domain=R)
        try:
            R.exquo(R.one, c_R)
            c_R_is_unit = True
        except Exception:
            c_R_is_unit = False
            
        if f.degree() <= 0:
            irred_R = False
        elif not c_R_is_unit:
            irred_R = False
        else:
            irred_R = (len(factors_R) == 1 and factors_R[0][1] == 1)
            
        c_F, factors_F = sympy.factor_list(f, domain=F)
        if f.degree() <= 0:
            irred_F = False
        else:
            irred_F = (len(factors_F) == 1 and factors_F[0][1] == 1)
            
        neg_q = bool(irred_R != irred_F)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f is a polynomial over R",
    "H_3: degree of f is greater than or equal to 1",
    "H_4: f is primitive over R",
    "¬Q: f is irreducible over R iff f is irreducible over F fails"
]

N_HYP = 4
NEG_Q_INDEX = 4
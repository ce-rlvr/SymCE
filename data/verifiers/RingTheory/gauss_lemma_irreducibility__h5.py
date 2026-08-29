import sympy
from sympy import Poly
from sympy.abc import x, y, z
from sympy import ZZ, QQ

def is_irreducible_over_domain(p):
    try:
        if p.degree() < 1:
            return False
        c, factors = p.factor_list()
        num_factors = sum(exp for fac, exp in factors if fac.degree() >= 1)
        if num_factors != 1:
            return False
        domain = p.domain
        if domain.is_Field:
            return True
        if hasattr(domain, 'is_unit'):
            if not domain.is_unit(c):
                return False
        else:
            if domain == ZZ:
                if abs(c) != 1:
                    return False
            else:
                try:
                    domain.exquo(domain.one, c)
                except Exception:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        R = witness.domain
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    try:
        R = witness.domain
        F = R.get_field()
        h2 = bool(F.is_Field)
    except Exception:
        h2 = False

    try:
        h3 = isinstance(witness, Poly) and len(witness.gens) == 1
    except Exception:
        h3 = False

    try:
        h4 = bool(witness.degree() >= 1)
    except Exception:
        h4 = False

    try:
        irr_R = is_irreducible_over_domain(witness)
        R = witness.domain
        F = R.get_field()
        f_F = witness.set_domain(F)
        irr_F = is_irreducible_over_domain(f_F)
        neg_q = bool(irr_R != irr_F)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: F is the field of fractions of R",
    "H_3: f is a polynomial over R",
    "H_4: degree of f is at least 1",
    "¬Q: Irreducibility over R differs from irreducibility over F"
]

N_HYP = 4
NEG_Q_INDEX = 4
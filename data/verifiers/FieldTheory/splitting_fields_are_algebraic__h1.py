import sympy
from sympy import Poly
from sympy.abc import x, t

QQ = sympy.QQ
ZZ = sympy.ZZ
RR = sympy.RR
CC = sympy.CC

def conditions(witness):
    try:
        F, S, E = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = True
        if not hasattr(F, 'is_Field') or not F.is_Field:
            h1 = False
        if not isinstance(S, (list, set, tuple)):
            h1 = False
        if h1:
            for p in S:
                if not isinstance(p, Poly):
                    h1 = False
                    break
                if not p.is_univariate:
                    h1 = False
                    break
                if not F.unify(p.domain) == F:
                    h1 = False
                    break
    except Exception:
        h1 = False

    try:
        h2 = False
        if hasattr(E, 'is_Field') and E.is_Field and F.unify(E) == E:
            roots_in_E = set()
            splits_completely = True
            for p in S:
                if p.is_zero:
                    roots_in_E.add('ALL_E')
                    continue
                
                try:
                    factors = p.factor_list(domain=E)
                    for fac, mult in factors[1]:
                        if fac.degree() > 1:
                            splits_completely = False
                            break
                        if fac.degree() == 1:
                            c1 = fac.coeff_monomial(fac.gen)
                            c0 = fac.coeff_monomial(1)
                            root = -c0 / c1
                            roots_in_E.add(root)
                except Exception:
                    splits_completely = False
                    break
                
                if not splits_completely:
                    break
            
            if splits_completely:
                if 'ALL_E' in roots_in_E:
                    h2 = True
                else:
                    if len(roots_in_E) == 0:
                        h2 = (E == F)
                    elif F == sympy.QQ and type(E).__name__ == 'AlgebraicField':
                        try:
                            gen_field = sympy.QQ.algebraic_field(*roots_in_E)
                            h2 = (E == gen_field)
                        except Exception:
                            h2 = False
                    elif F == sympy.RR and E == sympy.CC:
                        h2 = any(r not in sympy.RR for r in roots_in_E)
                    elif E == F:
                        h2 = all(r in F for r in roots_in_E)
                    else:
                        h2 = False
    except Exception:
        h2 = False

    try:
        neg_q = False
        if E == F:
            neg_q = False
        elif type(E).__name__ == 'FractionField':
            neg_q = True
        elif type(E).__name__ == 'AlgebraicField':
            neg_q = False
        elif E == sympy.CC and F == sympy.RR:
            neg_q = False
        elif E in (sympy.RR, sympy.CC) and F == sympy.QQ:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is an arbitrary set of polynomials over F",
    "H_2: E is a splitting field of S over F",
    "¬Q: There exists an element in E that is not algebraic over F"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy import Poly, Symbol, QQ, RR, CC
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: L is an extension field of K",
    "H_3: f(x) is a monic polynomial over K of degree n",
    "H_4: f(alpha) = 0",
    "H_5: The degree of the field extension K(alpha) over K is exactly n",
    "¬Q: f(x) is not irreducible over K"
]

N_HYP = 5
NEG_Q_INDEX = 5

def conditions(witness):
    K = None
    L = None
    f = None
    alpha = None
    n = None

    try:
        if isinstance(witness, dict):
            K = witness.get('K', QQ)
            L = witness.get('L', CC)
            f = witness.get('f')
            alpha = witness.get('alpha')
            n = witness.get('n')
        elif isinstance(witness, tuple):
            if len(witness) == 5:
                K, L, f, alpha, n = witness
            elif len(witness) == 4:
                K, L, f, alpha = witness
                n = Poly(f).degree() if f is not None else None
            elif len(witness) == 3:
                f, alpha, n = witness
                K = getattr(f, 'domain', QQ) if hasattr(f, 'domain') else QQ
                L = CC
            elif len(witness) == 2:
                f, alpha = witness
                K = getattr(f, 'domain', QQ) if hasattr(f, 'domain') else QQ
                L = CC
                n = Poly(f).degree() if f is not None else None
        else:
            K = getattr(witness, 'K', QQ)
            L = getattr(witness, 'L', CC)
            f = getattr(witness, 'f', None)
            alpha = getattr(witness, 'alpha', None)
            n = getattr(witness, 'n', None)
    except Exception:
        pass

    # H1: K is a field
    try:
        h1 = False
        if hasattr(K, 'is_Field') and K.is_Field:
            h1 = True
        elif K in [sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals]:
            h1 = True
        elif K == QQ:
            h1 = True
    except Exception:
        h1 = False

    # H2: L is an extension field of K
    try:
        h2 = False
        is_L_field = False
        if hasattr(L, 'is_Field') and L.is_Field:
            is_L_field = True
        elif L in [sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals]:
            is_L_field = True
        elif L == QQ:
            is_L_field = True
            
        if is_L_field:
            if hasattr(L, 'unify') and hasattr(K, 'unify'):
                try:
                    h2 = (L.unify(K) == L)
                except Exception:
                    h2 = True
            elif K == L:
                h2 = True
            elif K in [QQ, sympy.S.Rationals] and L in [sympy.S.Reals, sympy.S.Complexes, CC, RR]:
                h2 = True
            elif K == sympy.S.Reals and L in [sympy.S.Complexes, CC]:
                h2 = True
            else:
                h2 = True
    except Exception:
        h2 = False

    # H3: f(x) is a monic polynomial over K of degree n
    try:
        h3 = False
        f_poly = f if isinstance(f, Poly) else Poly(f, x)
        if f_poly.LC() == 1 and f_poly.degree() == n:
            h3 = True
    except Exception:
        h3 = False

    # H4: f(alpha) = 0
    try:
        f_poly = f if isinstance(f, Poly) else Poly(f, x)
        val = f_poly.as_expr().subs(f_poly.gen, alpha)
        h4 = (sympy.simplify(val) == 0)
    except Exception:
        h4 = False

    # H5: The degree of the field extension K(alpha) over K is exactly n
    try:
        h5 = False
        x_sym = Symbol('x')
        if K in [QQ, sympy.S.Rationals]:
            mp = sympy.minpoly(alpha, x_sym)
            if Poly(mp, x_sym).degree() == n:
                h5 = True
        else:
            mp = sympy.minpoly(alpha, x_sym, domain=K)
            if Poly(mp, x_sym).degree() == n:
                h5 = True
    except Exception:
        h5 = False

    # neg_Q: f(x) is not irreducible over K
    try:
        neg_Q = False
        f_poly = f if isinstance(f, Poly) else Poly(f, x, domain=K)
        if f_poly.is_irreducible is False:
            neg_Q = True
        else:
            factors = f_poly.factor_list()[1]
            total_factors = sum(mult for factor, mult in factors)
            if total_factors > 1:
                neg_Q = True
    except Exception:
        neg_Q = False

    return [h1, h2, h3, h4, h5, neg_Q]
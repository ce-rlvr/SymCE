import sympy
from sympy import Symbol, Poly

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

CONDITION_LABELS = [
    "H_1: A is a finitely generated commutative K-algebra",
    "H_2: A is a reduced ring",
    "¬Q: A is not isomorphic to the coordinate ring of V for any affine algebraic set V over K"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, str):
            expr = sympy.sympify(witness)
        elif isinstance(witness, (tuple, list)):
            ideal_part = witness[-1]
            if isinstance(ideal_part, (tuple, list)):
                if len(ideal_part) == 0:
                    return [False, False, False]
                expr = ideal_part[0]
            else:
                expr = ideal_part
            if isinstance(expr, str):
                expr = sympy.sympify(expr)
        else:
            expr = witness

        if isinstance(expr, sympy.Poly):
            f = expr.set_domain('QQ')
        else:
            expr = sympy.sympify(expr)
            free = expr.free_symbols
            if len(free) > 1:
                return [False, False, False]
            elif len(free) == 1:
                gen = list(free)[0]
            else:
                gen = x
            f = Poly(expr, gen, domain='QQ')

        if not f.is_univariate:
            return [False, False, False]

        h1 = True

        if f.is_zero or f.degree() == 0:
            h2 = True
        else:
            h2 = f.is_squarefree

        if f.is_zero or f.degree() == 0:
            neg_q = False
        else:
            rts = sympy.roots(f)
            distinct_rational_roots = [r for r in rts if r.is_rational]
            splits_completely_distinct = (len(distinct_rational_roots) == f.degree())
            neg_q = not splits_completely_distinct

        return [bool(h1), bool(h2), bool(neg_q)]

    except Exception:
        return [False, False, False]
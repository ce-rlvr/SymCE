import sympy
from sympy import Symbol, Poly, Rational, Integer

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

def conditions(witness):
    try:
        expr = witness.as_expr() if hasattr(witness, 'as_expr') else witness
    except Exception:
        expr = witness

    h1_ok = False
    try:
        if hasattr(witness, 'is_irreducible') and not isinstance(witness, sympy.Poly):
            h1_ok = bool(witness.is_irreducible() if callable(witness.is_irreducible) else witness.is_irreducible)
        else:
            h1_ok = bool(sympy.polys.polytools.is_irreducible(expr, domain='QQ'))
    except Exception:
        h1_ok = False

    h2_ok = False
    try:
        if hasattr(witness, 'degree') and not isinstance(witness, sympy.Poly):
            d = witness.degree() if callable(witness.degree) else witness.degree
            h2_ok = bool(d >= 1)
        else:
            h2_ok = bool(sympy.degree(expr) >= 1)
    except Exception:
        h2_ok = False

    neg_q_ok = False
    try:
        if hasattr(witness, 'is_primitive') and not isinstance(witness, sympy.Poly):
            prim = witness.is_primitive() if callable(witness.is_primitive) else witness.is_primitive
            neg_q_ok = not bool(prim)
        else:
            content = sympy.polys.polytools.primitive(expr)[0]
            neg_q_ok = bool(abs(content) != 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is an irreducible polynomial",
    "H_2: The degree of f is greater than or equal to 1",
    "not Q: f is not a primitive polynomial"
]

N_HYP = 2
NEG_Q_INDEX = 2
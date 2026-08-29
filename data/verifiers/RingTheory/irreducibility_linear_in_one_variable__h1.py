import math
from sympy import sympify, Poly, Integer
from sympy.abc import x, y

def mod_n(expr, n):
    expr = sympify(expr).expand()
    if n == 0:
        return expr
    gens = list(expr.free_symbols)
    if not gens:
        return Integer(expr % n)
    p = Poly(expr, *gens)
    res = Integer(0)
    for monom, coeff in p.terms():
        term = Integer(coeff % n)
        for gen, power in zip(gens, monom):
            term *= gen**power
        res += term
    return res

def conditions(witness) -> list[bool]:
    try:
        n = int(witness.get('n', 0))
        a = sympify(witness['a'])
        b = sympify(witness['b'])
        U = sympify(witness['U'])
        V = sympify(witness['V'])
        P = sympify(witness['P'])
        Q = sympify(witness['Q'])
        x_P = int(witness.get('x_P', 0))
        y_P = int(witness.get('y_P', 0))
        x_Q = int(witness.get('x_Q', 0))
        y_Q = int(witness.get('y_Q', 0))
    except Exception:
        return [False, False, False, False]

    try:
        h1 = False
        if a.free_symbols.issubset({x}) and b.free_symbols.issubset({x}):
            if a.is_polynomial(x) and b.is_polynomial(x):
                h1 = True
    except Exception:
        h1 = False

    try:
        a_mod = mod_n(a, n)
        h2 = (a_mod != 0)
    except Exception:
        h2 = False

    try:
        identity = mod_n(U*a + V*b, n)
        h3 = (mod_n(identity - 1, n) == 0)
    except Exception:
        h3 = False

    try:
        lhs = mod_n(P * Q, n)
        rhs = mod_n(a * y + b, n)
        is_factorization = (mod_n(lhs - rhs, n) == 0)
        
        P_val = int(P.subs({x: x_P, y: y_P}))
        if n == 0:
            P_not_unit = (abs(P_val) != 1)
        else:
            P_not_unit = (math.gcd(P_val % n, n) > 1)
            
        Q_val = int(Q.subs({x: x_Q, y: y_Q}))
        if n == 0:
            Q_not_unit = (abs(Q_val) != 1)
        else:
            Q_not_unit = (math.gcd(Q_val % n, n) > 1)
            
        neg_q = is_factorization and P_not_unit and Q_not_unit
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are polynomials in x",
    "H_2: a is not the zero polynomial",
    "H_3: The greatest common divisor of a and b is 1",
    "neg_Q: The polynomial a*y + b is reducible"
]

N_HYP = 3
NEG_Q_INDEX = 3
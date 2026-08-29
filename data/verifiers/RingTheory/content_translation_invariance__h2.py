import sympy
from sympy import Poly, Symbol, QQ, ZZ

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            R, a, f, var_x = witness
        elif len(witness) == 3:
            R, a, f = witness
            var_x = x
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a Unique Factorization Domain
    try:
        h1 = bool(getattr(R, 'is_UFD', False))
    except Exception:
        h1 = False

    # H_2: a is an element of R
    try:
        if hasattr(R, '__contains__'):
            h2 = bool(a in R)
        else:
            # If R is a sympy Domain, we can check if 'a' can be converted to it
            try:
                R.from_sympy(sympy.sympify(a))
                h2 = True
            except Exception:
                h2 = False
    except Exception:
        h2 = False

    # ¬Q: The content of f(x+a) does not equal the content of f(x) up to a unit
    try:
        if isinstance(f, Poly):
            f_expr = f.as_expr()
            if len(f.gens) == 1:
                var_x = f.gens[0]
        else:
            f_expr = sympy.sympify(f)
            
        p1 = Poly(f_expr, var_x)
        p2 = Poly(f_expr.subs(var_x, var_x + a), var_x)
        
        c1 = p1.content()
        c2 = p2.content()
        
        if c1 == c2 or c1 == -c2:
            neg_q = False
        else:
            try:
                # Check if they are equal up to a unit in R
                c1_R = R.from_sympy(c1)
                c2_R = R.from_sympy(c2)
                q1 = R.exquo(c1_R, c2_R)
                q2 = R.exquo(c2_R, c1_R)
                neg_q = False
            except Exception:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: a is an element of R",
    "¬Q: The content of f(x+a) does not equal the content of f(x) up to a unit"
]

N_HYP = 2
NEG_Q_INDEX = 2
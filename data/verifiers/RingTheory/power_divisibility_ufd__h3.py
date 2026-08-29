import sympy
from sympy import symbols

# Top-level setup
# Define some common symbols in case the witness uses them for a polynomial ring UFD.
x, y, z = symbols('x y z')

def conditions(witness):
    try:
        # The witness is expected to be a tuple (a, b, n)
        if len(witness) == 3:
            a, b, n = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: R is a Unique Factorization Domain
    # We support Z (integers) and polynomial rings over fields (sympy expressions).
    try:
        is_int_a = isinstance(a, (int, sympy.Integer))
        is_int_b = isinstance(b, (int, sympy.Integer))
        is_expr_a = isinstance(a, (sympy.Expr, sympy.Poly))
        is_expr_b = isinstance(b, (sympy.Expr, sympy.Poly))
        
        h1 = (is_int_a or is_expr_a) and (is_int_b or is_expr_b)
        
        if is_int_a and is_int_b:
            domain = 'int'
        elif h1:
            domain = 'expr'
            a_expr = sympy.sympify(a)
            b_expr = sympy.sympify(b)
        else:
            domain = None
    except Exception:
        h1 = False
        domain = None

    # H_2: a and b are elements of R
    try:
        h2 = h1
    except Exception:
        h2 = False

    # H_3: a^n divides b^n in R
    try:
        if not h1:
            h3 = False
        elif not isinstance(n, (int, sympy.Integer)):
            h3 = False
        elif n < 0:
            h3 = False
        else:
            if domain == 'int':
                an = a**n
                bn = b**n
                if an == 0:
                    h3 = (bn == 0)
                else:
                    h3 = (bn % an == 0)
            elif domain == 'expr':
                an = a_expr**n
                bn = b_expr**n
                if an == 0:
                    h3 = (bn == 0)
                else:
                    try:
                        q, r = sympy.div(bn, an)
                        h3 = (r == 0)
                    except Exception:
                        # Fallback if sympy.div fails (e.g., no generators found)
                        try:
                            res = sympy.simplify(bn / an)
                            h3 = bool(res.is_polynomial() or res.is_Integer)
                        except Exception:
                            h3 = False
            else:
                h3 = False
    except Exception:
        h3 = False

    # ¬Q: a does not divide b in R
    try:
        if not h1:
            neg_q = False
        elif domain == 'int':
            if a == 0:
                divides_ab = (b == 0)
            else:
                divides_ab = (b % a == 0)
            neg_q = not divides_ab
        elif domain == 'expr':
            if a_expr == 0:
                divides_ab = (b_expr == 0)
            else:
                try:
                    q, r = sympy.div(b_expr, a_expr)
                    divides_ab = (r == 0)
                except Exception:
                    try:
                        res = sympy.simplify(b_expr / a_expr)
                        divides_ab = bool(res.is_polynomial() or res.is_Integer)
                    except Exception:
                        divides_ab = False
            neg_q = not divides_ab
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: a and b are elements of R",
    "H_3: a^n divides b^n in R",
    "¬Q: a does not divide b in R"
]

N_HYP = 3
NEG_Q_INDEX = 3
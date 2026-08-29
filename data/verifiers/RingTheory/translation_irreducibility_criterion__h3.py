import sympy
from sympy import Symbol, Poly

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x')
t = Symbol('t')
y = Symbol('y')

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the conjecture.
    The witness should be a dictionary containing:
      - 'p': a prime integer (characteristic of the field F = F_p(t))
      - 'f': the polynomial f(x) in F[x] as a sympy expression in x and t
      - 'c_minpoly': the minimal polynomial of c over F as a sympy expression in y and t
    """
    try:
        p = int(witness['p'])
        f_expr = witness['f']
        c_minpoly = witness['c_minpoly']
    except Exception:
        return [False, False, False, False]

    def is_irreducible_Fpt(expr, p, main_var):
        try:
            num, den = sympy.fraction(sympy.cancel(expr))
            poly = sympy.Poly(num, main_var, t, domain=sympy.FF(p))
            facs = poly.factor_list()
            main_factors = []
            for fac, mult in facs[1]:
                if main_var in fac.free_symbols:
                    main_factors.append((fac, mult))
            return len(main_factors) == 1 and main_factors[0][1] == 1
        except Exception:
            return False

    # H_1: F is a field and c is in an extension field
    try:
        h1 = False
        if sympy.isprime(p):
            if c_minpoly.free_symbols.issubset({y, t}):
                if is_irreducible_Fpt(c_minpoly, p, y):
                    h1 = True
    except Exception:
        h1 = False

    # H_2: f(x) is a polynomial in F[x]
    try:
        h2 = False
        if f_expr.free_symbols.issubset({x, t}):
            num, den = sympy.fraction(sympy.cancel(f_expr))
            if den.free_symbols.issubset({t}):
                sympy.Poly(num, x, t, domain=sympy.FF(p))
                h2 = True
    except Exception:
        h2 = False

    # H_3: f(x+c) is in F[x] and is irreducible in F[x]
    try:
        h3 = False
        c_poly = sympy.Poly(c_minpoly, y, t, domain=sympy.FF(p)).monic()
        c_minpoly_mod = c_poly.as_expr()
        
        num, den = sympy.fraction(sympy.cancel(f_expr))
        f_shifted = sympy.expand(num.subs(x, x + y))
        f_shifted_poly = sympy.Poly(f_shifted, x, y, t, domain=sympy.FF(p))
        f_shifted_mod = f_shifted_poly.as_expr()
        
        rem_expr = sympy.rem(f_shifted_mod, c_minpoly_mod, y)
        rem_poly = sympy.Poly(rem_expr, x, y, t, domain=sympy.FF(p))
        rem_mod = rem_poly.as_expr()
        
        if y not in rem_mod.free_symbols:
            if is_irreducible_Fpt(rem_mod, p, x):
                h3 = True
    except Exception:
        h3 = False

    # neg_Q: f(x) is reducible in F[x]
    try:
        neg_q = False
        num, den = sympy.fraction(sympy.cancel(f_expr))
        poly_x = sympy.Poly(num, x, t, domain=sympy.FF(p))
        deg = poly_x.degree(x)
        if deg >= 2:
            neg_q = not is_irreducible_Fpt(f_expr, p, x)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field and c is in an extension field",
    "H_2: f is a polynomial over F",
    "H_3: f(x+c) is over F and is irreducible",
    "not Q: f is reducible over F"
]

N_HYP = 3
NEG_Q_INDEX = 3
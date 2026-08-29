import sympy
from sympy import Poly, Rational, Integer
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: c is a non-zero element of R",
    "¬Q: The content of f(x) does not divide the content of f(cx) in R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # Parse the witness. It can be either (R, c, f) or (c, f).
        if len(witness) == 3:
            R, c, f = witness
            domain = R
            c_sym = sympy.sympify(c)
            if isinstance(f, Poly):
                gen = f.gens[0]
                f_expr = f.as_expr()
            else:
                gen = x
                f_expr = sympy.sympify(f)
        elif len(witness) == 2:
            c, f = witness
            c_sym = sympy.sympify(c)
            if isinstance(f, Poly):
                gen = f.gens[0]
                f_expr = f.as_expr()
                domain = f.domain
            else:
                gen = x
                f_expr = sympy.sympify(f)
                # Infer a common domain that includes c and the coefficients of f
                domain = Poly(f_expr + c_sym * gen, gen).domain
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a Unique Factorization Domain
    try:
        h1 = bool(domain.is_UFD)
    except Exception:
        h1 = False

    # H_2: c is a non-zero element of R
    try:
        c_elem = domain.from_sympy(c_sym)
        h2 = (c_elem is not None) and (c_elem != domain.zero)
    except Exception:
        h2 = False

    # ¬Q: The content of f(x) does not divide the content of f(cx) in R
    try:
        # Construct polynomials over the domain R
        p_f = Poly(f_expr, gen, domain=domain)
        p_fc = Poly(f_expr.subs(gen, c_sym * gen), gen, domain=domain)
        
        cont_f = p_f.content()
        cont_fc = p_fc.content()
        
        if cont_f == domain.zero:
            divides = (cont_fc == domain.zero)
        else:
            try:
                # Check exact divisibility in the domain R
                domain.exquo(cont_fc, cont_f)
                divides = True
            except Exception:
                divides = False
                
        neg_q = not divides
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]
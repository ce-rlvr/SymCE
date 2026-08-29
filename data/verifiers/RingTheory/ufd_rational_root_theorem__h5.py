import sympy
from sympy import Symbol, Poly
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: K is the fraction field of R",
    "H_3: f(x) is a polynomial over R of degree n >= 1",
    "H_4: p and q are coprime elements of R",
    "not Q: q does not divide a_n or p does not divide a_0 in R"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False, False]
        f, p, q = witness
    except Exception:
        return [False, False, False, False, False]

    try:
        f_sym = sympy.sympify(f)
        poly = Poly(f_sym, x)
        R = poly.domain
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    h2 = h1

    try:
        f_sym = sympy.sympify(f)
        poly = Poly(f_sym, x)
        h3 = bool(poly.degree() >= 1)
    except Exception:
        h3 = False

    try:
        f_sym = sympy.sympify(f)
        poly = Poly(f_sym, x)
        R = poly.domain
        p_sym = sympy.sympify(p)
        q_sym = sympy.sympify(q)
        p_dom = R.from_sympy(p_sym)
        q_dom = R.from_sympy(q_sym)
        
        if p_dom is None or q_dom is None:
            h4 = False
        else:
            gcd_pq = R.gcd(p_dom, q_dom)
            h4 = bool(R.is_unit(gcd_pq))
    except Exception:
        h4 = False

    try:
        f_sym = sympy.sympify(f)
        poly = Poly(f_sym, x)
        R = poly.domain
        a_n = poly.LC()
        a_0 = poly.nth(0)
        
        p_sym = sympy.sympify(p)
        q_sym = sympy.sympify(q)
        p_dom = R.from_sympy(p_sym)
        q_dom = R.from_sympy(q_sym)
        
        def divides_in_domain(a, b, dom):
            if b == dom.zero:
                return a == dom.zero
            try:
                dom.exquo(a, b)
                return True
            except Exception:
                return False

        if p_dom is None or q_dom is None:
            neg_q = False
        else:
            q_divides_an = divides_in_domain(a_n, q_dom, R)
            p_divides_a0 = divides_in_domain(a_0, p_dom, R)
            neg_q = not (q_divides_an and p_divides_a0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]
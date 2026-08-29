import sympy
from sympy.abc import x

def conditions(witness):
    f = None
    p = None
    c_list = None
    
    try:
        if isinstance(witness, (tuple, list)):
            f = sympy.sympify(witness[0])
            if len(witness) > 1:
                p = sympy.sympify(witness[1])
            if len(witness) > 2:
                c_list = witness[2]
        else:
            f = sympy.sympify(witness)
    except Exception:
        pass

    # H_1: f(x) is a polynomial in Z[x]
    try:
        if not isinstance(f, sympy.Expr):
            h1_ok = False
        elif not f.free_symbols.issubset({x}):
            h1_ok = False
        else:
            f_poly = sympy.Poly(f, x)
            h1_ok = (f_poly.domain == sympy.ZZ)
    except Exception:
        h1_ok = False

    # H_2: p is a prime number
    try:
        h2_ok = sympy.isprime(p)
    except Exception:
        h2_ok = False

    # H_3: There exist n distinct integers c_i such that |f(c_i)| = p for all 1 <= i <= n
    try:
        n = sympy.degree(f, x)
        if n < 1:
            h3_ok = False
        else:
            if c_list is None and p is not None:
                roots_pos = sympy.roots(f - p, x)
                roots_neg = sympy.roots(f + p, x)
                c_list = list(set([r for r in roots_pos if r.is_integer] + 
                                  [r for r in roots_neg if r.is_integer]))
            
            if c_list is not None:
                valid_c = []
                for c in set(c_list):
                    try:
                        if sympy.S(c).is_integer and abs(f.subs(x, c)) == p:
                            valid_c.append(c)
                    except Exception:
                        pass
                h3_ok = len(valid_c) >= n
            else:
                h3_ok = False
    except Exception:
        h3_ok = False

    # neg_Q: f(x) is not irreducible over Q
    try:
        factors = sympy.factor_list(f, domain='QQ')
        is_irred = (len(factors[1]) == 1 and factors[1][0][1] == 1)
        neg_q_ok = not is_irred
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a polynomial over Z",
    "H_2: p is a prime number",
    "H_3: There exist n distinct integers c_i such that abs(f(c_i)) equals p",
    "¬Q: f is not irreducible over Q"
]

N_HYP = 3
NEG_Q_INDEX = 3
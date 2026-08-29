import sympy

# Top-level setup
x, y, z = sympy.symbols('x y z')
QQ = sympy.QQ
ZZ = sympy.ZZ
RR = sympy.RR
CC = sympy.CC

def parse_witness(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                F, f, gen = witness
                return F, f, gen
            elif len(witness) == 2:
                F, f = witness
                if isinstance(f, sympy.Poly):
                    return F, f.as_expr(), f.gen
                else:
                    f_expr = sympy.sympify(f)
                    symbols = list(f_expr.free_symbols)
                    if len(symbols) == 1:
                        return F, f_expr, symbols[0]
                    elif len(symbols) > 1:
                        if x in symbols:
                            return F, f_expr, x
                        return F, f_expr, symbols[0]
                    else:
                        return F, f_expr, x
    except Exception:
        pass
    return None, None, None

def conditions(witness) -> list[bool]:
    # H1: F is a field
    try:
        F, f, gen = parse_witness(witness)
        h1 = False
        if F is not None:
            if hasattr(F, 'is_Field'):
                h1 = bool(F.is_Field)
            elif F in [sympy.QQ, sympy.RR, sympy.CC]:
                h1 = True
            elif F == sympy.ZZ:
                h1 = False
    except Exception:
        h1 = False

    # H2: The degree of f(x) is n, where n >= 1
    try:
        F, f, gen = parse_witness(witness)
        h2 = False
        if F is not None and f is not None and gen is not None:
            f_poly = sympy.Poly(f, gen)
            n = f_poly.degree()
            h2 = bool(n >= 1)
    except Exception:
        h2 = False

    # neg_Q: F[x]/<f(x)> is NOT an n-dimensional vector space over F
    try:
        F, f, gen = parse_witness(witness)
        neg_q = False
        if F is not None and f is not None and gen is not None:
            f_poly = sympy.Poly(f, gen)
            
            for c in f_poly.coeffs():
                c = sympy.sympify(c)
                in_F = False
                if F == sympy.QQ:
                    in_F = bool(c.is_Rational)
                elif F == sympy.RR:
                    in_F = bool(c.is_real)
                elif F == sympy.CC:
                    in_F = bool(c.is_complex)
                elif F == sympy.ZZ:
                    in_F = bool(c.is_Integer)
                else:
                    try:
                        if hasattr(F, 'from_sympy'):
                            F.from_sympy(c)
                            in_F = True
                        else:
                            in_F = False
                    except Exception:
                        in_F = False
                
                if not in_F:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: The degree of f(x) is n, where n >= 1",
    "not Q: The quotient ring modulo f(x) is not an n-dimensional vector space over F"
]

N_HYP = 2
NEG_Q_INDEX = 2
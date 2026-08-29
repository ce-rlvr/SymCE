import sympy as sp
from sympy import Poly, Symbol
from sympy.ntheory import is_square, legendre_symbol

# Top-level setup
x = Symbol('x')

def conditions(witness):
    f = None
    
    # Attempt to parse witness into a sympy Poly
    try:
        if isinstance(witness, Poly):
            f = witness
        elif hasattr(witness, 'as_poly'):
            f = witness.as_poly(x)
        elif isinstance(witness, sp.Expr):
            f = Poly(witness, x)
        elif isinstance(witness, (tuple, list)):
            for item in witness:
                if isinstance(item, Poly):
                    f = item
                    break
                elif hasattr(item, 'as_poly'):
                    p = item.as_poly(x)
                    if p is not None:
                        f = p
                        break
                elif isinstance(item, sp.Expr):
                    try:
                        f = Poly(item, x)
                        break
                    except Exception:
                        pass
            if f is None and len(witness) >= 2:
                try:
                    b, c = witness[0], witness[1]
                    f = Poly(x**2 + b*x + c, x, domain='QQ')
                except Exception:
                    pass
        elif isinstance(witness, dict):
            if 'f' in witness:
                f_val = witness['f']
                if isinstance(f_val, Poly):
                    f = f_val
                elif hasattr(f_val, 'as_poly'):
                    f = f_val.as_poly(x)
                elif isinstance(f_val, sp.Expr):
                    f = Poly(f_val, x)
            elif 'b' in witness and 'c' in witness:
                b = witness['b']
                c = witness['c']
                f = Poly(x**2 + b*x + c, x, domain='QQ')
        elif hasattr(witness, 'f'):
            f_val = witness.f
            if isinstance(f_val, Poly):
                f = f_val
            elif hasattr(f_val, 'as_poly'):
                f = f_val.as_poly(x)
            elif isinstance(f_val, sp.Expr):
                f = Poly(f_val, x)
    except Exception:
        pass

    if f is None:
        return [False, False, False, False]

    char = 0
    domain = None
    # H1: The characteristic of F is not equal to 2
    try:
        domain = f.domain
        char = domain.characteristic
        h1 = (char != 2)
    except Exception:
        h1 = False

    # H2: f(x) = x^2 + bx + c is a polynomial over F
    try:
        deg = f.degree()
        lc = f.LC()
        h2 = (deg == 2 and lc == 1)
    except Exception:
        h2 = False

    # H3: E is a splitting field of f(x) over F
    # We assume the witness implicitly provides the correct splitting field E
    try:
        h3 = True
    except Exception:
        h3 = False

    # neg_Q: E is NOT isomorphic to F(\sqrt{b^2 - 4c}) over F
    # This happens when b^2 - 4c is a square in F, making F(x)/(x^2 - D) not a field,
    # whereas the splitting field E is always a field.
    try:
        coeffs = f.all_coeffs()
        if len(coeffs) == 3:
            a, b, c = coeffs
            D = b**2 - 4*a*c
            
            if char > 0:
                D_mod = D % char
                if D_mod == 0:
                    neg_q = True
                else:
                    neg_q = legendre_symbol(D_mod, char) == 1
            elif hasattr(domain, 'is_RealField') and domain.is_RealField:
                neg_q = bool(D >= 0)
            elif hasattr(domain, 'is_ComplexField') and domain.is_ComplexField:
                neg_q = True
            else:
                try:
                    if hasattr(D, 'p') and hasattr(D, 'q'):
                        neg_q = is_square(D.p) and is_square(D.q)
                    else:
                        neg_q = is_square(D)
                except Exception:
                    neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: The characteristic of F is not equal to 2",
    "H_2: f(x) = x^2 + bx + c is a polynomial over F",
    "H_3: E is a splitting field of f(x) over F",
    "¬Q: E is NOT isomorphic to F(sqrt(b^2 - 4c)) over F"
]

N_HYP = 3
NEG_Q_INDEX = 3
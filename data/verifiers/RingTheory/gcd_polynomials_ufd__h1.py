import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy import eye, zeros

# Top-level setup for standard objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 2:
            f, g = witness
        elif len(witness) == 3:
            f, g, x = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: f and g are non-zero polynomials
    try:
        if hasattr(f, 'is_zero'):
            f_zero = f.is_zero() if callable(f.is_zero) else f.is_zero
            g_zero = g.is_zero() if callable(g.is_zero) else g.is_zero
            if f_zero is not None and g_zero is not None:
                h1 = (not f_zero) and (not g_zero)
            else:
                h1 = (f != 0) and (g != 0)
        else:
            h1 = (f != 0) and (g != 0)
    except Exception:
        h1 = False

    # ¬Q: gcd(f, g) != gcd(c(f), c(g)) * gcd(f_1, g_1)
    try:
        if hasattr(f, 'content') and hasattr(f, 'primitive_part'):
            cf = f.content()
            f1 = f.primitive_part()
            cg = g.content()
            g1 = g.primitive_part()
            
            gcd_c = cf.gcd(cg)
            gcd_1 = f1.gcd(g1)
            try:
                expected = gcd_c * gcd_1
            except Exception:
                expected = gcd_1 * gcd_c
            actual = f.gcd(g)
            
            if hasattr(actual, 'is_associate'):
                neg_q = not actual.is_associate(expected)
            elif hasattr(actual, 'equals'):
                neg_q = not (actual.equals(expected) or actual.equals(-expected))
            else:
                neg_q = (actual != expected) and (actual != -expected)
        else:
            if len(witness) == 3:
                x = witness[2]
            else:
                symbols = (sympy.sympify(f).as_expr() + sympy.sympify(g).as_expr()).free_symbols
                x = list(symbols)[0] if symbols else sympy.Symbol('x')
            
            f_poly = f if isinstance(f, sympy.Poly) else sympy.Poly(f, x)
            g_poly = g if isinstance(g, sympy.Poly) else sympy.Poly(g, x)
            
            cf, f1 = f_poly.primitive()
            cg, g1 = g_poly.primitive()
            
            domain = f_poly.domain
            if hasattr(domain, 'gcd'):
                gcd_c = domain.gcd(cf, cg)
            else:
                gcd_c = sympy.gcd(cf, cg)
            
            gcd_1 = f1.gcd(g1)
            
            try:
                expected = gcd_1.mul_ground(gcd_c)
            except Exception:
                expected = gcd_1 * gcd_c
                
            actual = f_poly.gcd(g_poly)
            
            actual_expr = actual.as_expr() if hasattr(actual, 'as_expr') else actual
            expected_expr = expected.as_expr() if hasattr(expected, 'as_expr') else expected
            
            diff = sympy.simplify(actual_expr - expected_expr)
            sum_ = sympy.simplify(actual_expr + expected_expr)
            neg_q = (diff != 0) and (sum_ != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f and g are non-zero polynomials",
    "¬Q: gcd(f, g) != gcd(c(f), c(g)) * gcd(f_1, g_1)"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
from sympy import Poly, Matrix, eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup
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

x_sym = sympy.Symbol('x')

def parse_witness(witness):
    n = 0
    if isinstance(witness, tuple):
        if len(witness) == 3:
            f, g, n = witness
        elif len(witness) == 2:
            f, g = witness
        else:
            return None, None, None
    elif isinstance(witness, dict):
        f = witness.get('f')
        g = witness.get('g')
        n = witness.get('n', 0)
    else:
        return None, None, None

    try:
        n = int(n)
    except Exception:
        n = 0

    if n == 0:
        def extract_modulus(poly):
            try:
                if hasattr(poly, 'domain') and hasattr(poly.domain, 'mod'):
                    return int(poly.domain.mod)
            except Exception:
                pass
            return 0
            
        n_f = extract_modulus(f)
        n_g = extract_modulus(g)
        if n_f > 0:
            n = n_f
        elif n_g > 0:
            n = n_g

    def to_expr(poly):
        if isinstance(poly, (list, tuple)):
            if len(poly) == 0:
                return sympy.Integer(0)
            res = poly[0] * x_sym**0
            for i in range(1, len(poly)):
                res = res + poly[i] * x_sym**i
            return res
        elif hasattr(poly, 'as_expr'):
            return poly.as_expr()
        elif isinstance(poly, str):
            return sympy.sympify(poly)
        else:
            return poly

    f = to_expr(f)
    g = to_expr(g)
        
    return f, g, n

def poly_deg(expr, var, n):
    if hasattr(expr, 'is_Matrix') and expr.is_Matrix:
        max_d = -1
        for i in range(expr.rows):
            for j in range(expr.cols):
                d = poly_deg(expr[i, j], var, n)
                if d > max_d:
                    max_d = d
        return max_d

    if hasattr(expr, 'expand'):
        expr = expr.expand()
    
    try:
        if n > 0:
            p = Poly(expr, var)
            coeffs = p.all_coeffs()
            mod_coeffs = []
            for c in coeffs:
                if hasattr(c, 'is_Integer') and c.is_Integer:
                    mod_coeffs.append(c % n)
                else:
                    try:
                        mod_coeffs.append(int(c) % n)
                    except Exception:
                        mod_coeffs.append(c)
            
            for i, c in enumerate(mod_coeffs):
                if c != 0:
                    return len(mod_coeffs) - 1 - i
            return -1
        else:
            p = Poly(expr, var)
            if p.is_zero:
                return -1
            return p.degree()
    except Exception:
        if not hasattr(expr, 'has') or not expr.has(var):
            is_zero = False
            try:
                if expr == 0:
                    is_zero = True
            except Exception:
                pass
            if is_zero:
                return -1
            return 0
            
        collected = sympy.collect(expr, var, evaluate=False)
        if not isinstance(collected, dict):
            try:
                return sympy.degree(expr, var)
            except Exception:
                return -1
                
        max_deg = -1
        for term, coeff in collected.items():
            if n > 0:
                try:
                    coeff = coeff % n
                except Exception:
                    pass
                    
            is_zero = False
            try:
                if coeff == 0:
                    is_zero = True
            except Exception:
                pass
                
            if is_zero:
                continue
            
            if term == 1:
                deg = 0
            elif term == var:
                deg = 1
            elif isinstance(term, sympy.Pow) and term.base == var:
                try:
                    deg = int(term.exp)
                except Exception:
                    continue
            else:
                continue
                
            if deg > max_deg:
                max_deg = deg
                
        return max_deg

def conditions(witness) -> list[bool]:
    try:
        f, g, n = parse_witness(witness)
        if f is None or g is None:
            return [False, False]
    except Exception:
        return [False, False]

    try:
        free_symbols = set()
        if hasattr(f, 'free_symbols'):
            free_symbols.update(f.free_symbols)
        if hasattr(g, 'free_symbols'):
            free_symbols.update(g.free_symbols)
            
        if len(free_symbols) == 1:
            var = list(free_symbols)[0]
        elif len(free_symbols) > 1:
            if x_sym in free_symbols:
                var = x_sym
            else:
                var = list(free_symbols)[0]
        else:
            var = x_sym
    except Exception:
        var = x_sym

    # H_1: f(x) and g(x) are non-zero polynomials
    try:
        deg_f = poly_deg(f, var, n)
        deg_g = poly_deg(g, var, n)
        h1_ok = (deg_f >= 0) and (deg_g >= 0)
    except Exception:
        h1_ok = False

    # neg_Q: deg(f*g) != deg(f) + deg(g)
    try:
        fg = f * g
        if hasattr(fg, 'expand'):
            fg = fg.expand()
        deg_fg = poly_deg(fg, var, n)
        neg_q_ok = (deg_fg != deg_f + deg_g)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f and g are non-zero polynomials",
    "¬Q: deg(f*g) != deg(f) + deg(g)"
]

N_HYP = 1
NEG_Q_INDEX = 1
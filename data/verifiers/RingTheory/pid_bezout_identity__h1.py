import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

from sympy import Poly, gcd, symbols, solve, simplify, ZZ, QQ

# Top-level setup for Ring Theory
x, y, z = symbols('x y z')

def get_witness_elements(witness):
    a, b = None, None
    vars = ()
    domain_name = 'ZZ'
    
    if isinstance(witness, tuple):
        if len(witness) == 2:
            a, b = witness
        elif len(witness) == 3:
            a, b, third = witness
            if isinstance(third, str):
                domain_name = third
            elif isinstance(third, tuple):
                vars = third
            else:
                domain_name = str(third)
        elif len(witness) >= 4:
            a, b, vars, domain_name = witness[:4]
            
    if hasattr(a, 'ring'):
        if not vars:
            vars = a.ring.symbols
        if domain_name == 'ZZ' and hasattr(a.ring, 'domain'):
            domain_name = 'ZZ' if a.ring.domain.is_ZZ else 'QQ'
        a = a.as_expr()
        b = b.as_expr()
        
    if not vars and hasattr(a, 'free_symbols') and hasattr(b, 'free_symbols'):
        vars = tuple(a.free_symbols | b.free_symbols)
        
    if isinstance(domain_name, str):
        if 'QQ' in domain_name or 'Q' in domain_name:
            domain_name = 'QQ'
        else:
            domain_name = 'ZZ'
            
    return a, b, vars, domain_name

def check_bezout(a, b, vars, domain_name):
    try:
        d = gcd(a, b)
    except Exception:
        return True
        
    # 1. Point evaluation check (necessary condition for Bézout's identity)
    if vars:
        for vals in itertools.product(range(-2, 3), repeat=len(vars)):
            subs_dict = dict(zip(vars, vals))
            a_val = a.subs(subs_dict)
            b_val = b.subs(subs_dict)
            d_val = d.subs(subs_dict)
            
            if domain_name == 'ZZ':
                try:
                    a_int = int(a_val)
                    b_int = int(b_val)
                    d_int = int(d_val)
                    g = math.gcd(a_int, b_int)
                    if g != 0 and d_int % g != 0:
                        return False
                    if g == 0 and d_int != 0:
                        return False
                except Exception:
                    pass
            elif domain_name == 'QQ':
                try:
                    if a_val == 0 and b_val == 0 and d_val != 0:
                        return False
                except Exception:
                    pass

    # 2. Linear system check for polynomial coefficients
    try:
        poly_a = Poly(a, *vars) if vars else Poly(a)
        poly_b = Poly(b, *vars) if vars else Poly(b)
        poly_d = Poly(d, *vars) if vars else Poly(d)
        
        max_deg = max(poly_a.total_degree(), poly_b.total_degree(), poly_d.total_degree())
        max_deg = max(max_deg, 1)
        max_deg = min(max_deg, 5)
        
        if vars:
            monomials = []
            for degrees in itertools.product(range(max_deg + 1), repeat=len(vars)):
                if sum(degrees) <= max_deg:
                    monomial = 1
                    for v, deg in zip(vars, degrees):
                        monomial *= v**deg
                    monomials.append(monomial)
        else:
            monomials = [1]
            
        X_poly = 0
        Y_poly = 0
        coeffs_vars = []
        for i, m in enumerate(monomials):
            cx = symbols(f'cx_{i}')
            cy = symbols(f'cy_{i}')
            coeffs_vars.extend([cx, cy])
            X_poly += cx * m
            Y_poly += cy * m
            
        expr = a * X_poly + b * Y_poly - d
        if vars:
            poly_expr = Poly(expr, *vars)
            equations = poly_expr.coeffs()
        else:
            equations = [expr]
            
        sol = solve(equations, coeffs_vars, dict=True)
        if not sol:
            return False
            
        if domain_name == 'ZZ':
            for s in sol:
                all_integers = True
                for var, val in s.items():
                    if val.is_Rational and not val.is_Integer:
                        if len(val.free_symbols) == 0:
                            all_integers = False
                            break
                if all_integers:
                    return True
            return False
    except Exception:
        pass
        
    return True

def conditions(witness):
    try:
        a, b, vars, domain_name = get_witness_elements(witness)
    except Exception:
        return [False, False]
        
    try:
        h1 = bool(simplify(a) != 0) and bool(simplify(b) != 0)
    except Exception:
        h1 = False
        
    try:
        neg_q = not check_bezout(a, b, vars, domain_name)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are non-zero elements of R",
    "¬Q: Bézout's identity fails for a and b (no x, y in R such that ax + by = gcd(a, b))"
]

N_HYP = 1
NEG_Q_INDEX = 1
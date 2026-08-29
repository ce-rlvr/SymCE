import sympy as sp
from sympy.abc import x, t
from sympy import Poly, factor_list, div
from sympy.ntheory import divisors
import itertools
import functools

# Top-level setup
# The witness is expected to be a sympy expression in x and t.
# We implicitly define the ring R = Z[t**2, t**3] and its fraction field F = Q(t).
# x and t are available in the namespace for the witness expression.
# A known counterexample for this setup is f(x) = x**2 - t**2.

def is_in_R(P, t_sym):
    try:
        P_poly = Poly(P, t_sym, domain='ZZ')
        return P_poly.coeff_monomial(t_sym) == 0
    except Exception:
        return False

def is_poly_in_R(P, x_sym, t_sym):
    try:
        P_poly = Poly(P, x_sym)
        for coeff in P_poly.coeffs():
            if not is_in_R(coeff, t_sym):
                return False
        return True
    except Exception:
        return False

def is_primitive_in_R(coeffs, t_sym):
    try:
        G = functools.reduce(sp.gcd, coeffs)
        G_poly = Poly(G, t_sym, domain='ZZ')
    except Exception:
        return False
        
    try:
        const, factors = factor_list(G_poly)
        bases = [f[0] for f in factors]
        exps = [f[1] for f in factors]
        const_divs = divisors(abs(const))
        
        for exps_choice in itertools.product(*[range(e + 1) for e in exps]):
            poly_part = sp.Mul(*[b**e for b, e in zip(bases, exps_choice)])
            for c in const_divs:
                d = c * poly_part
                d_expr = d.as_expr() if hasattr(d, 'as_expr') else d
                
                if d_expr == 1 or d_expr == -1:
                    continue
                    
                if is_in_R(d_expr, t_sym):
                    all_in_R = True
                    for coeff in coeffs:
                        try:
                            q, r = div(coeff, d_expr, t_sym, domain='ZZ')
                            if r != 0 or not is_in_R(q, t_sym):
                                all_in_R = False
                                break
                        except Exception:
                            all_in_R = False
                            break
                    if all_in_R:
                        return False
        return True
    except Exception:
        return False

def is_irreducible_in_F(f, x_sym, t_sym):
    try:
        const, factors = factor_list(f)
        x_factors = 0
        for base, exp in factors:
            if base.has(x_sym):
                x_factors += exp
        return x_factors == 1
    except Exception:
        return False

def is_irreducible_in_R(f, x_sym, t_sym):
    try:
        const, factors = factor_list(f)
        bases = [f[0] for f in factors]
        exps = [f[1] for f in factors]
        const_divs = divisors(abs(const))
        
        for exps_choice in itertools.product(*[range(e + 1) for e in exps]):
            poly_g = sp.Mul(*[b**e for b, e in zip(bases, exps_choice)])
            poly_h = sp.Mul(*[b**(max_e - e) for b, max_e, e in zip(bases, exps, exps_choice)])
            
            for c in const_divs:
                g = c * poly_g
                h = (const // c) * poly_h
                
                g_expr = g.as_expr() if hasattr(g, 'as_expr') else g
                h_expr = h.as_expr() if hasattr(h, 'as_expr') else h
                
                if g_expr == 1 or g_expr == -1:
                    continue
                if h_expr == 1 or h_expr == -1:
                    continue
                    
                if is_poly_in_R(g_expr, x_sym, t_sym) and is_poly_in_R(h_expr, x_sym, t_sym):
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        witness = sp.sympify(witness)
    except Exception:
        return [False] * 5

    h1 = True
    
    try:
        h2 = bool(is_poly_in_R(witness, x, t))
    except Exception:
        h2 = False
        
    try:
        h3 = bool(Poly(witness, x).degree() >= 1)
    except Exception:
        h3 = False
        
    try:
        coeffs = Poly(witness, x).coeffs()
        coeffs = [c for c in coeffs if c != 0]
        if not coeffs:
            h4 = False
        else:
            h4 = bool(is_primitive_in_R(coeffs, t))
    except Exception:
        h4 = False
        
    try:
        irr_R = is_irreducible_in_R(witness, x, t)
        irr_F = is_irreducible_in_F(witness, x, t)
        neg_q = bool(irr_R != irr_F)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is the field of fractions of R",
    "H_2: f is a polynomial over R",
    "H_3: degree of f is at least 1",
    "H_4: f is primitive over R",
    "not_Q: f is irreducible over R XOR f is irreducible over F"
]

N_HYP = 4
NEG_Q_INDEX = 4
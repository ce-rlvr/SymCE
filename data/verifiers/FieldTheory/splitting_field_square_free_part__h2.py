import sympy
from sympy import Poly, factor_list, QQ, ZZ, GF, Rational, Integer
from sympy.abc import x, y, z, t
import math
import itertools
import functools

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: g(x) is the square-free part of f(x)",
    "H_3: E is the splitting field of f(x) over F",
    "¬Q: E is not the splitting field of g(x) over F"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    H1 = False
    H2 = False
    H3 = False
    neg_Q = False
    
    try:
        # Parse witness
        if isinstance(witness, dict):
            F = witness.get('F')
            f = witness.get('f')
            g = witness.get('g')
            E = witness.get('E')
        elif isinstance(witness, tuple) and len(witness) == 4:
            F, f, g, E = witness
        else:
            f = witness
            if hasattr(f, 'domain'):
                F = f.domain
            else:
                f_poly = Poly(f)
                F = f_poly.domain
            
            try:
                f_poly = Poly(f, domain=F)
                if not f_poly.gens:
                    gen = x
                    f_poly = Poly(f, gen, domain=F)
                else:
                    gen = f_poly.gen
            except Exception:
                gen = x
                f_poly = Poly(f, gen, domain=F)
                
            f_prime = f_poly.diff()
            gcd_poly = f_poly.gcd(f_prime)
            g = f_poly.quo(gcd_poly).as_expr()
            E = "SplittingField(f)"
            
        # Determine generator
        try:
            f_poly = Poly(f, domain=F)
            if not f_poly.gens:
                gen = x
            else:
                gen = f_poly.gen
        except Exception:
            gen = x

        # H1: F is a field
        try:
            H1 = getattr(F, 'is_Field', False)
        except Exception:
            H1 = False
            
        # H2: g is the square-free part of f
        try:
            f_poly = Poly(f, gen, domain=F)
            g_poly = Poly(g, gen, domain=F)
            
            # Check if g is the product of distinct irreducible factors
            factors = factor_list(f_poly)[1]
            prod = Poly(1, gen, domain=F)
            for fac, mult in factors:
                prod = prod * Poly(fac, gen, domain=F)
            
            q1, r1 = g_poly.div(prod)
            q2, r2 = prod.div(g_poly)
            is_prod = r1.is_zero and r2.is_zero
            
            # Check if g is computed via f / gcd(f, f')
            f_prime = f_poly.diff()
            gcd_poly = f_poly.gcd(f_prime)
            sqf = f_poly.quo(gcd_poly)
            
            q3, r3 = g_poly.div(sqf)
            q4, r4 = sqf.div(g_poly)
            is_sqf = r3.is_zero and r4.is_zero
            
            H2 = is_prod or is_sqf
        except Exception:
            H2 = False
            
        # H3: E is the splitting field of f over F
        try:
            if E == "SplittingField(f)":
                H3 = True
            else:
                f_E = Poly(f, gen, domain=E)
                factors_E = factor_list(f_E)[1]
                splits_f = all(Poly(fac, gen, domain=E).degree() == 1 for fac, mult in factors_E)
                H3 = splits_f
        except Exception:
            H3 = False
            
        # neg_Q: E is NOT the splitting field of g over F
        try:
            if E == "SplittingField(f)":
                f_poly = Poly(f, gen, domain=F)
                g_poly = Poly(g, gen, domain=F)
                
                factors_f = factor_list(f_poly)[1]
                splits_f_F = all(Poly(fac, gen, domain=F).degree() == 1 for fac, mult in factors_f)
                
                factors_g = factor_list(g_poly)[1]
                splits_g_F = all(Poly(fac, gen, domain=F).degree() == 1 for fac, mult in factors_g)
                
                if splits_g_F and not splits_f_F:
                    neg_Q = True
                else:
                    neg_Q = False
            else:
                g_E = Poly(g, gen, domain=E)
                factors_g = factor_list(g_E)[1]
                splits_g = all(Poly(fac, gen, domain=E).degree() == 1 for fac, mult in factors_g)
                
                g_F = Poly(g, gen, domain=F)
                factors_gF = factor_list(g_F)[1]
                splits_g_F = all(Poly(fac, gen, domain=F).degree() == 1 for fac, mult in factors_gF)
                
                if not splits_g:
                    neg_Q = True
                elif splits_g_F and E != F:
                    neg_Q = True
                else:
                    neg_Q = False
        except Exception:
            neg_Q = False
            
    except Exception:
        pass
        
    return [bool(H1), bool(H2), bool(H3), bool(neg_Q)]
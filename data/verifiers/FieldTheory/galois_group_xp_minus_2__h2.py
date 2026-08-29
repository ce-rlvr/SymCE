import sympy
from sympy import sympify, isprime, factor_list, discriminant, Poly, roots, sqrt
from sympy.polys.numberfields import primitive_element
from sympy.abc import x
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def galois_group_order(f, x_sym):
    try:
        p_f = Poly(f, x_sym)
    except Exception:
        return None
        
    deg = p_f.degree()
    if deg <= 0:
        return 1
        
    # General path using primitive element of the splitting field
    try:
        rts_list = roots(f, x_sym, multiple=True)
        if len(rts_list) == deg:
            non_rat_rts = [r for r in rts_list if not r.is_Rational]
            if not non_rat_rts:
                return 1
            unique_rts = list(set(non_rat_rts))
            elem, mp = primitive_element(unique_rts, x_sym)
            return Poly(mp, x_sym).degree()
    except Exception:
        pass
        
    try:
        factors = factor_list(f)[1]
    except Exception:
        return None
        
    # Fast path for single irreducible factors of small degree
    if len(factors) == 1 and factors[0][1] == 1:
        poly_factor = Poly(factors[0][0], x_sym)
        if poly_factor.degree() == 3:
            disc = discriminant(poly_factor.as_expr(), x_sym)
            if sympy.sqrt(disc).is_Rational:
                return 3
            else:
                return 6
        elif poly_factor.degree() == 2:
            return 2
        elif poly_factor.degree() == 1:
            return 1
            
    return None

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                p_raw, f_raw = witness
            elif len(witness) >= 3:
                p_raw, f_raw = witness[0], witness[1]
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        def safe_sympify(expr):
            if isinstance(expr, str):
                expr = expr.replace('^', '**')
            return sympify(expr)
            
        p = safe_sympify(p_raw)
        f = safe_sympify(f_raw)
        
        # H1: p is an odd prime number
        try:
            h1 = isprime(p) and p % 2 == 1
        except Exception:
            h1 = False
            
        # H2: L is the splitting field of f(x) over Q
        # This is definitional for L, so it holds by construction if the witness provides f(x)
        h2 = True
        
        # ¬Q: The Galois group Gal(L/Q) does not have order p(p-1) or is not isomorphic to the semidirect product
        try:
            free_syms = f.free_symbols
            if len(free_syms) == 1:
                x_sym = list(free_syms)[0]
            elif len(free_syms) == 0:
                x_sym = x
            else:
                x_sym = x # fallback
                
            order = galois_group_order(f, x_sym)
            if order is None:
                # If we cannot compute the order, we conservatively return False
                neg_q = False
            else:
                expected_order = p * (p - 1)
                if order != expected_order:
                    neg_q = True
                else:
                    neg_q = False
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "H_2: L is the splitting field of f(x) over Q",
    "¬Q: The Galois group Gal(L/Q) does not have order p(p-1) or is not isomorphic to the semidirect product"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy import isprime, Poly, diff, factor_list, GF, sympify
from sympy.abc import X, t, u, v, x, y, z

# Top-level setup: named object bindings that the witness expression may reference.
# The witness should be a tuple (p, f) where p is a prime number (the characteristic)
# and f is an irreducible polynomial in X (or x) over F_p(t, u, v, ...) defining the extension.

CONDITION_LABELS = [
    "H_1: K is a field of characteristic p > 0",
    "H_2: L/K is a finite field extension",
    "¬Q: L/K is not a separable extension"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        p, f = witness
    except Exception:
        return [False, False, False]

    # H_1: K is a field of characteristic p > 0 (p must be a prime number)
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H_2: L/K is a finite field extension
    # This means f is an irreducible polynomial in the main variable over F_p(gens) of degree >= 1
    try:
        if not h1:
            h2 = False
        else:
            f_expr = sympify(f)
            if hasattr(f_expr, 'as_expr'):
                f_expr = f_expr.as_expr()
            
            gens = list(f_expr.free_symbols)
            if X in gens:
                main_var = X
            elif x in gens:
                main_var = x
            else:
                main_var = X
                
            if main_var in gens:
                gens.remove(main_var)
            gens = sorted(gens, key=lambda s: s.name)
            
            poly_f = Poly(f_expr, main_var, *gens, domain=GF(p))
            if poly_f.degree(main_var) < 1:
                h2 = False
            else:
                const, factors = factor_list(poly_f)
                # Must be irreducible (exactly one factor, with multiplicity 1)
                if len(factors) == 1 and factors[0][1] == 1:
                    h2 = True
                else:
                    h2 = False
    except Exception:
        h2 = False

    # ¬Q: L/K is not a separable extension
    # This means the formal derivative of the minimal polynomial f is identically zero mod p
    try:
        if not h1:
            neg_q = False
        else:
            f_expr = sympify(f)
            if hasattr(f_expr, 'as_expr'):
                f_expr = f_expr.as_expr()
            
            gens = list(f_expr.free_symbols)
            if X in gens:
                main_var = X
            elif x in gens:
                main_var = x
            else:
                main_var = X
                
            if main_var in gens:
                gens.remove(main_var)
            gens = sorted(gens, key=lambda s: s.name)
            
            df = diff(f_expr, main_var)
            poly_df = Poly(df, main_var, *gens, domain=GF(p))
            neg_q = bool(poly_df.is_zero)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]
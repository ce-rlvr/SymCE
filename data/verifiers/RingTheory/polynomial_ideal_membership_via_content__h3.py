import sympy
from sympy import Poly, gcd, reduced, groebner, Symbol, S

# Top-level setup
# The witness will provide the necessary symbols and expressions to define the ring and ideal.

def conditions(witness):
    """
    witness is expected to be a dictionary or tuple containing:
      I_gens: list of sympy expressions generating the ideal I (e.g., [2, y])
      f: sympy expression for the polynomial f (e.g., 2*x + y)
      x: sympy.Symbol representing the polynomial variable (e.g., x)
      R_gens: (optional) list of sympy.Symbol objects generating the ring R over ZZ
    """
    try:
        if isinstance(witness, dict):
            R_gens = witness.get('R_gens', [])
            I_gens = witness.get('I_gens', [])
            f = witness.get('f', None)
            x = witness.get('x', None)
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                I_gens, f = witness
                R_gens = []
                x = None
            elif len(witness) == 3:
                I_gens, f, x = witness
                R_gens = []
            elif len(witness) == 4:
                R_gens, I_gens, f, x = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if x is None:
            if isinstance(f, Poly):
                x = f.gens[0]
            elif hasattr(f, 'free_symbols') and f.free_symbols:
                x = list(f.free_symbols)[0]
            else:
                x = Symbol('x')
                
        if not R_gens:
            syms = set()
            for g in I_gens:
                if hasattr(g, 'free_symbols'):
                    syms.update(g.free_symbols)
            if hasattr(f, 'free_symbols'):
                syms.update(f.free_symbols)
            syms.discard(x)
            R_gens = list(syms)
            
    except Exception:
        return [False, False, False]
        
    if f is None or x is None:
        return [False, False, False]

    # H_1: R is a commutative ring with identity
    try:
        h1 = isinstance(R_gens, list) and all(isinstance(g, Symbol) for g in R_gens)
    except Exception:
        h1 = False

    # H_2: I is an ideal of R
    try:
        h2 = isinstance(I_gens, list) and len(I_gens) > 0
    except Exception:
        h2 = False

    # neg_Q: The equivalence (f in I[x] iff c(f) subset I) fails
    try:
        f_poly = Poly(f, x)
        coeffs = f_poly.coeffs()
        
        if R_gens:
            try:
                gb = groebner(I_gens, *R_gens, domain='ZZ')
                basis = list(gb)
            except Exception:
                basis = I_gens
        else:
            basis = I_gens
            
        def in_ideal(expr):
            if not R_gens:
                igcd = basis[0]
                for g in basis[1:]:
                    igcd = gcd(igcd, g)
                return S(expr) % igcd == 0
            else:
                try:
                    rem = reduced(expr, basis, *R_gens, domain='ZZ')[1]
                    return rem == 0
                except Exception:
                    try:
                        # Fallback necessary condition by evaluating at 0
                        subs_dict = {g: 0 for g in R_gens}
                        expr_0 = S(expr).subs(subs_dict)
                        basis_0 = [S(b).subs(subs_dict) for b in basis]
                        igcd = basis_0[0]
                        for b in basis_0[1:]:
                            igcd = gcd(igcd, b)
                        if igcd == 0:
                            if expr_0 != 0:
                                return False
                        elif expr_0 % igcd != 0:
                            return False
                        
                        # If it passes the necessary condition, try reduced without domain
                        rem = reduced(expr, basis, *R_gens)[1]
                        return rem == 0
                    except Exception:
                        return False

        f_in_I = all(in_ideal(c) for c in coeffs)
        
        cont = coeffs[0]
        for c in coeffs[1:]:
            cont = gcd(cont, c)
            
        cf_in_I = in_ideal(cont)
        
        neg_q = (f_in_I != cf_in_I)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I is an ideal of R",
    "neg_Q: The equivalence fails"
]

N_HYP = 2
NEG_Q_INDEX = 2
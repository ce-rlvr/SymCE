import sympy
from sympy import Symbol, Poly, degree, factor_list, RootOf

# Top-level setup for witness expressions
x = Symbol('x')
y = Symbol('y')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple of two polynomials (f, g) over QQ, representing
    the abstract field extensions L = QQ[x]/(f) and E = QQ[x]/(g).
    """
    try:
        f, g = witness
    except Exception:
        return [False, False, False]
    
    try:
        if isinstance(f, str):
            f = sympy.sympify(f)
        if isinstance(g, str):
            g = sympy.sympify(g)
            
        syms_f = f.free_symbols
        syms_g = g.free_symbols
        var_f = list(syms_f)[0] if syms_f else x
        var_g = list(syms_g)[0] if syms_g else x

        f = f.subs(var_f, x)
        g = g.subs(var_g, x)
        
        f_poly = Poly(f, x, domain='QQ')
        g_poly = Poly(g, x, domain='QQ')
    except Exception:
        return [False, False, False]

    # H1: L/K is a finite Galois extension
    # This means f is irreducible over QQ and splits completely in its root field.
    try:
        h1 = False
        if f_poly.is_irreducible:
            r_f = RootOf(f, 0)
            if getattr(r_f, 'is_Rational', False):
                factors_f = factor_list(f)[1]
            else:
                factors_f = factor_list(f, extension=r_f)[1]
            
            # Check if all factors are linear (degree 1)
            if all(degree(fac[0], x) == 1 for fac in factors_f):
                h1 = True
    except Exception:
        h1 = False

    # H2: E/K is an arbitrary field extension
    # This means g is irreducible over QQ.
    try:
        h2 = bool(g_poly.is_irreducible)
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails at the witness.
    # The dropped hypothesis is that L and E are subfields of a common field.
    # For abstract extensions, "the compositum field LE" is only uniquely defined 
    # if L and E are linearly disjoint over K (i.e., L \otimes_K E is a field).
    # If they are not linearly disjoint, f factors over E, meaning there are multiple 
    # non-isomorphic compositums or the tensor product has zero divisors.
    try:
        neg_q = False
        if h1 and h2:
            r_g = RootOf(g, 0)
            if getattr(r_g, 'is_Rational', False):
                factors_f_over_E = factor_list(f)[1]
            else:
                factors_f_over_E = factor_list(f, extension=r_g)[1]
            
            # If f factors into more than 1 irreducible polynomial over E, 
            # L and E are not linearly disjoint, so "the" compositum is undefined.
            if len(factors_f_over_E) > 1:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension",
    "H_2: E/K is an arbitrary field extension",
    "¬Q: The compositum field LE is not uniquely defined (L and E are not linearly disjoint)"
]

N_HYP = 2
NEG_Q_INDEX = 2
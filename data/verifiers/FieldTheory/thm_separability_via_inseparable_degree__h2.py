import sympy
from sympy import Symbol, Poly, diff, GF
from sympy.ntheory import isprime

# Top-level setup: named object bindings that the witness expression may reference.
# We define x and t to represent polynomials in F_p(t)[x].
x = Symbol('x')
t = Symbol('t')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Every finite field extension is separable."
    
    The witness should be a tuple (p, f) where:
      - p is a prime number (characteristic of the base field).
      - f is an irreducible polynomial in x over F_p(t).
      
    The base field is F = F_p(t) and the extension is E = F[x]/(f).
    """
    try:
        p, f = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    # H_2: f is a non-constant polynomial in x over F_p(t)
    try:
        f_sym = sympy.sympify(f)
        if not f_sym.free_symbols.issubset({x, t}):
            h2 = False
        else:
            poly_f = Poly(f_sym, x, t)
            h2 = bool(poly_f.degree(x) > 0)
    except Exception:
        h2 = False
        
    # H_3: f is irreducible over F_p(t)
    # By Gauss's Lemma, if f is irreducible in F_p[x, t] and has positive degree in x,
    # it is irreducible in F_p(t)[x].
    try:
        if h1 and h2:
            poly_fp = Poly(f_sym, x, t, domain=GF(p))
            factors = poly_fp.factor_list()
            # It must have exactly one irreducible factor with multiplicity 1
            h3 = bool(len(factors[1]) == 1 and factors[1][0][1] == 1)
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # ¬Q: The extension E/F is inseparable.
    # Since f is irreducible, the extension is inseparable if and only if 
    # the formal derivative of f with respect to x is identically zero in F_p[x, t].
    try:
        if h1 and h2:
            df_dx = diff(f_sym, x)
            poly_df = Poly(df_dx, x, t, domain=GF(p))
            neg_q = bool(poly_df.is_zero)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: f is a non-constant polynomial in x over F_p(t)",
    "H_3: f is irreducible over F_p(t)",
    "¬Q: The extension is inseparable (derivative of f w.r.t x is 0 mod p)"
]

N_HYP = 3
NEG_Q_INDEX = 3
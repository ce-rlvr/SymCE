import sympy
from sympy.abc import x, y, z

# Top-level setup for potential witness references
Z = sympy.S.Integers
Q = sympy.S.Rationals

def conditions(witness):
    """
    Given a witness, checks the hypotheses and the negated conclusion.
    Returns a list of booleans: [H_1, H_2, H_3, H_4, neg_Q]
    """
    # Extract f and p from the witness
    f = None
    p = None
    if isinstance(witness, dict):
        f = witness.get('f')
        p = witness.get('p', witness.get('P'))
    elif isinstance(witness, (tuple, list)):
        if len(witness) >= 2:
            f = witness[0]
            p = witness[1]
    
    if f is None or p is None:
        return [False, False, False, False, False]
        
    try:
        f = sympy.sympify(f)
        p = sympy.sympify(p)
    except Exception:
        return [False, False, False, False, False]

    # Identify the main variable in f
    try:
        free_vars = f.free_symbols
        if p in free_vars:
            free_vars = free_vars - {p}
        
        if len(free_vars) == 1:
            x_var = list(free_vars)[0]
        elif len(free_vars) > 1:
            x_sym = sympy.Symbol('x')
            if x_sym in free_vars:
                x_var = x_sym
            else:
                x_var = list(free_vars)[0]
        else:
            x_var = sympy.Symbol('x')
    except Exception:
        return [False, False, False, False, False]
        
    # H_1: D is a unique factorization domain
    # We assume D is Z or Q[y] based on the type of p, both of which are UFDs.
    h1 = True
    
    # H_2: P is a prime ideal of D
    try:
        if p.is_Integer:
            h2 = sympy.isprime(abs(int(p)))
        else:
            # If p is a symbol, it generates a prime ideal in Q[p]
            h2 = isinstance(p, sympy.Symbol)
    except Exception:
        h2 = False
        
    # H_3: The leading coefficient a_n is not an element of P
    try:
        f_poly = sympy.Poly(f, x_var)
        lc = f_poly.LC()
        if p.is_Integer:
            h3 = (lc % abs(int(p))) != 0
        else:
            h3 = sympy.simplify(lc.subs(p, 0)) != 0
    except Exception:
        h3 = False
        
    # H_4: The image of f(x) under the natural homomorphism is irreducible
    try:
        if p.is_Integer:
            f_mod = sympy.Poly(f, x_var, domain=sympy.GF(abs(int(p))))
            if f_mod.degree() <= 0:
                h4 = False
            else:
                factors = f_mod.factor_list()
                h4 = (len(factors[1]) == 1 and factors[1][0][1] == 1)
        else:
            f_mod = f.subs(p, 0)
            f_mod_poly = sympy.Poly(f_mod, x_var)
            if f_mod_poly.degree() <= 0:
                h4 = False
            else:
                factors = f_mod_poly.factor_list()
                # For D/P = Z, we must also ensure the content is 1 or -1
                h4 = (len(factors[1]) == 1 and factors[1][0][1] == 1 and factors[0] in [1, -1])
    except Exception:
        h4 = False
        
    # neg_Q: f(x) CAN be factored into two polynomials of positive degree
    try:
        factors = sympy.factor_list(f)
        # Count the number of factors (with multiplicity) that have positive degree in x_var
        pos_deg_count = sum(mult for fac, mult in factors[1] if sympy.Poly(fac, x_var).degree() > 0)
        neg_q = pos_deg_count >= 2
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: Let D be a unique factorization domain",
    "H_2: Let P be a prime ideal of D",
    "H_3: The leading coefficient a_n is not an element of P",
    "H_4: The image of f(x) under the natural homomorphism is irreducible",
    "¬Q: f(x) can be factored into two polynomials of positive degree"
]

N_HYP = 4
NEG_Q_INDEX = 4
import sympy
from sympy.abc import x, y, z, t
from sympy import I, pi, E, Rational, sqrt

def parse_witness(witness):
    F = None
    K = None
    f = None
    x_var = None
    
    if isinstance(witness, dict):
        F = witness.get('F')
        K = witness.get('K')
        f = witness.get('f')
        x_var = witness.get('x')
    elif isinstance(witness, (list, tuple)):
        if len(witness) == 2:
            F, f = witness
        elif len(witness) == 3:
            F, f, x_var = witness
        elif len(witness) == 4:
            F, K, f, x_var = witness
            
    if isinstance(f, sympy.Relational):
        f = f.lhs - f.rhs
    elif isinstance(f, sympy.Poly):
        f = f.as_expr()
        
    if x_var is None and isinstance(f, sympy.Expr):
        free = f.free_symbols
        if free:
            xs = [s for s in free if s.name == 'x']
            if xs:
                x_var = xs[0]
            else:
                x_var = sorted(list(free), key=lambda s: s.name)[0]
                
    return F, K, f, x_var

def conditions(witness):
    F, K, f, x_var = parse_witness(witness)
    
    # H1: F is an algebraically closed field
    h1_ok = False
    try:
        if F in ('CC', 'C', sympy.S.Complexes, sympy.CC):
            h1_ok = True
        elif str(F) in ('CC', 'C', 'Complexes', 'S.Complexes'):
            h1_ok = True
    except Exception:
        pass
        
    # H2: K is the splitting field of f(x) over F
    h2_ok = False
    try:
        if isinstance(f, sympy.Expr) and isinstance(x_var, sympy.Symbol):
            # Check if f is a valid polynomial in x_var
            poly = sympy.Poly(f, x_var)
            h2_ok = True
    except Exception:
        pass
        
    # neg_Q: K != F
    # Since F is algebraically closed (e.g., CC), K = F iff all roots of f(x) are in F.
    # A root is in CC if it is a complex number (i.e., has no free symbolic variables).
    neg_q_ok = False
    try:
        if h1_ok and h2_ok:
            roots = sympy.solve(f, x_var)
            if roots:
                for r in roots:
                    if not r.is_number:
                        neg_q_ok = True
                        break
    except Exception:
        pass
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is an algebraically closed field",
    "H_2: K is the splitting field of f(x) over F",
    "¬Q: The splitting field K is not equal to F"
]

N_HYP = 2
NEG_Q_INDEX = 2
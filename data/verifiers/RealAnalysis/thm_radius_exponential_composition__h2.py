import sympy as sp

# Top-level setup: named object bindings
x = sp.Symbol('x')

def conditions(witness):
    """
    Given a witness (A, R), where A is a sympy expression representing A(x)
    and R is a real number (or sp.oo), checks if it is a valid counterexample.
    """
    try:
        A, R = witness
    except Exception:
        return [False, False]
    
    # H_1: A(x) has a zero constant term (A(0) = 0)
    try:
        A_val = sp.limit(A, x, 0)
        h1_ok = bool(A_val == 0)
    except Exception:
        h1_ok = False
        
    # neg_Q: B(x) = exp(A(x)) has a radius of convergence strictly less than R
    try:
        B = sp.exp(A)
        B_R = None
        
        # Simplify B and try to find its poles if it's a rational function
        B_simp = sp.simplify(B)
        n, d = sp.fraction(sp.cancel(B_simp))
        if d != 1:
            try:
                sols = sp.solve(d, x)
                if sols:
                    B_R = min(float(abs(s)) for s in sols)
            except Exception:
                pass
        
        # If B is a polynomial, its radius of convergence is infinity
        if B_R is None:
            if B_simp.is_polynomial(x):
                B_R = float('inf')
                
        # Try to find singularities of B using sympy's calculus module
        if B_R is None:
            from sympy.calculus.singularities import singularities
            try:
                sings = singularities(B_simp, x)
                if sings.is_FiniteSet:
                    if sings:
                        B_R = min(float(abs(s)) for s in sings)
                    else:
                        B_R = float('inf')
            except Exception:
                pass
                
        # Fallback: exp(A(x)) is singular where A(x) is singular or infinite
        if B_R is None:
            try:
                from sympy.calculus.singularities import singularities
                sings_A = singularities(A, x)
                if sings_A.is_FiniteSet:
                    if sings_A:
                        B_R = min(float(abs(s)) for s in sings_A)
                    else:
                        B_R = float('inf')
            except Exception:
                pass
                
        # Fallback: try to find poles of A directly
        if B_R is None:
            try:
                n_A, d_A = sp.fraction(sp.cancel(A))
                if d_A != 1:
                    sols_A = sp.solve(d_A, x)
                    if sols_A:
                        B_R = min(float(abs(s)) for s in sols_A)
            except Exception:
                pass

        if B_R is not None:
            neg_q_ok = bool(B_R < float(R))
        else:
            neg_q_ok = False
            
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A(x) has a zero constant term (A(0) = 0)",
    "¬Q: B(x) = exp(A(x)) has a radius of convergence strictly less than R"
]

N_HYP = 1
NEG_Q_INDEX = 1
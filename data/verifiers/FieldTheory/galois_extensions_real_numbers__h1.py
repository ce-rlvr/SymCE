import sympy as sp
from sympy.abc import x
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "If E is a finite Galois extension of R, then E is isomorphic to R or C."
    
    The witness is expected to be a sympy expression (polynomial) representing 
    the algebra E = R[x]/(P(x)), or a matrix M representing R[M].
    """
    h1 = False
    neg_q = False
    
    try:
        poly = None
        
        # Extract polynomial from witness
        if hasattr(witness, 'minimal_polynomial'):
            x_sym = sp.Symbol('x')
            min_poly_expr = witness.minimal_polynomial(x_sym)
            poly = sp.Poly(min_poly_expr, x_sym)
        elif isinstance(witness, sp.Poly):
            poly = witness
        elif isinstance(witness, sp.Expr):
            free_symbols = witness.free_symbols
            if len(free_symbols) == 1:
                x_sym = list(free_symbols)[0]
                try:
                    poly = sp.Poly(witness, x_sym)
                except Exception:
                    return [False, False]
            elif len(free_symbols) == 0:
                return [False, False]
            else:
                return [False, False]
        else:
            return [False, False]
            
        if poly is None:
            return [False, False]
            
        # Must be a polynomial over R
        if not all(c.is_real for c in poly.coeffs()):
            return [False, False]
            
        deg = poly.degree()
        if deg < 1:
            return [False, False]
            
        expr = poly.as_expr()
        gen = poly.gen
        
        # A Galois extension over a field must be an étale algebra (separable polynomial)
        disc = sp.discriminant(expr, gen)
        if disc == 0:
            return [False, False]
            
        # Count real and complex roots
        roots = sp.roots(expr, gen, multiple=True)
        num_real = 0
        num_complex = 0
        
        if len(roots) == deg:
            for r in roots:
                if r.is_real:
                    num_real += 1
                elif r.is_real is False:
                    num_complex += 1
                else:
                    try:
                        im_val = float(sp.im(r).evalf())
                        if abs(im_val) < 1e-9:
                            num_real += 1
                        else:
                            num_complex += 1
                    except Exception:
                        pass
        else:
            # Fallback to numerical roots if exact roots cannot be found
            n_roots = sp.nroots(expr)
            for r in n_roots:
                try:
                    im_val = float(sp.im(r).evalf())
                    if abs(im_val) < 1e-9:
                        num_real += 1
                    else:
                        num_complex += 1
                except Exception:
                    pass
                    
        # E is a Galois extension of R iff E is isomorphic to R^n or C^n
        # This happens iff all roots are real (R^n) or all roots are complex (C^{n/2})
        if num_real + num_complex == deg:
            if num_real == deg or num_complex == deg:
                h1 = True
                
                # Check if E is isomorphic to R or C
                if deg == 1:
                    # Isomorphic to R
                    neg_q = False
                elif deg == 2 and num_complex == 2:
                    # Isomorphic to C
                    neg_q = False
                else:
                    # Isomorphic to R^n (n >= 2) or C^n (n >= 2), which are not fields
                    neg_q = True
                    
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: E is a finite Galois extension of R",
    "¬Q: E is not isomorphic to either R or C"
]

N_HYP = 1
NEG_Q_INDEX = 1
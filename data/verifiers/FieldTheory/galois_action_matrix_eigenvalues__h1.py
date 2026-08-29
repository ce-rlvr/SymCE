import sympy

# Top-level setup for linear algebra objects
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        A = witness['A']
        lambda_val = witness['lambda_val']
        sigma_lambda = witness['sigma_lambda']
        # K_domain represents the base field K. Defaults to Rational Field (QQ)
        K_domain = witness.get('K_domain', sympy.QQ)
        
        x = sympy.Symbol('x')
        
        def is_zero(expr):
            if expr == 0: return True
            simp = sympy.simplify(expr)
            if simp == 0: return True
            return sympy.expand(simp) == 0
        
        # H_1: A is an n x n matrix with entries in the base field K
        h1 = A.is_square and all(entry in K_domain for entry in A)
        
        # H_2: \lambda \in L is an eigenvalue of A
        charpoly = A.charpoly(x).as_expr()
        h2 = is_zero(charpoly.subs(x, lambda_val))
        
        # Verify that sigma_lambda is a valid Galois conjugate of lambda_val over K.
        # They must share the same minimal polynomial over K.
        is_conjugate = False
        if 'minpoly_K' in witness:
            mp = witness['minpoly_K']
            if is_zero(mp.subs(x, lambda_val)) and is_zero(mp.subs(x, sigma_lambda)):
                coeffs = sympy.Poly(mp, x).coeffs()
                if all(c in K_domain for c in coeffs):
                    is_conjugate = True
        else:
            mp = sympy.minpoly(lambda_val, x, domain=K_domain)
            if is_zero(mp.subs(x, sigma_lambda)):
                is_conjugate = True
                
        if not is_conjugate:
            neg_q = False
        else:
            # Helper to compute algebraic multiplicity of a root in a polynomial
            def get_mult(poly_expr, r):
                m = 0
                p = poly_expr
                for _ in range(A.shape[0] + 1):
                    if not is_zero(p.subs(x, r)):
                        break
                    m += 1
                    q, rem = sympy.div(p, x - r, domain='EX')
                    p = q
                return m
                
            mult_lambda = get_mult(charpoly, lambda_val)
            mult_sigma = get_mult(charpoly, sigma_lambda)
            
            # ¬Q: sigma(lambda) is NOT an eigenvalue of A OR has a different algebraic multiplicity
            neg_q = (mult_sigma == 0) or (mult_lambda != mult_sigma)
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix with entries in the base field K",
    "H_2: lambda is an eigenvalue of A",
    "¬Q: sigma(lambda) is NOT an eigenvalue of A OR has a different algebraic multiplicity"
]

N_HYP = 2
NEG_Q_INDEX = 2
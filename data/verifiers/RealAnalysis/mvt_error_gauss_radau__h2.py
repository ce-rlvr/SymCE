import sympy as sp

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness is expected to be a tuple (f, n) or a dictionary/object with 'f' and 'n',
    where f is a sympy expression in terms of x, and n is an integer >= 1.
    """
    try:
        if isinstance(witness, tuple):
            f, n = witness
        elif isinstance(witness, dict):
            f = witness['f']
            n = witness['n']
        else:
            f = witness.f
            n = witness.n
    except Exception:
        return [False, False]
        
    x = sp.Symbol('x', real=True)
    
    # H_1: f is 2n-1 times continuously differentiable on the interval from -1 to 1
    try:
        if not isinstance(n, int) or n < 1:
            h1 = False
        else:
            # Check if we can compute the (2n-1)-th derivative
            diff_f = sp.diff(f, x, 2*n-1)
            h1 = True
    except Exception:
        h1 = False

    # ¬Q: Conclusion fails (there does NOT exist c in (-1, 1) satisfying the equation)
    try:
        # Compute exact integral
        exact_int = sp.integrate(f, (x, -1, 1))
        
        # Compute Gauss-Radau quadrature I_n(f)
        # Nodes are roots of P_{n-1}(x) + P_n(x)
        P_n_minus_1 = sp.legendre(n-1, x)
        P_n = sp.legendre(n, x)
        poly = P_n_minus_1 + P_n
        
        # Find roots (nodes)
        roots = sp.solve(poly, x)
        nodes = []
        for r in roots:
            if r.is_real:
                nodes.append(r)
            else:
                try:
                    if abs(sp.im(sp.N(r))) < 1e-9:
                        nodes.append(sp.re(r))
                except Exception:
                    pass
                    
        # Fallback to real_roots if solve didn't return exactly n real roots
        if len(nodes) != n:
            nodes = sp.real_roots(poly)
            
        # Sort nodes to ensure deterministic order
        nodes = sorted(nodes, key=lambda val: float(sp.N(val)))
        
        # Compute weights by solving the Vandermonde system
        M = sp.Matrix([[node**k for node in nodes] for k in range(n)])
        rhs = sp.Matrix([[sp.Rational(2, k+1) if k % 2 == 0 else 0] for k in range(n)])
        weights = M.LUsolve(rhs)
        
        # Evaluate I_n(f)
        I_n = 0
        for i in range(n):
            I_n += weights[i] * f.subs(x, nodes[i])
            
        error = sp.simplify(exact_int - I_n)
        
        # Compute RHS coefficient: 2^{2n-1} * n * [(n-1)!]^4 / [(2n-1)!]^3
        num = (2**(2*n-1)) * n * (sp.factorial(n-1)**4)
        den = sp.factorial(2*n-1)**3
        coeff = sp.Rational(num, den)
        
        # Compute RHS expression: coeff * f^{(2n-1)}(c)
        c = sp.Symbol('c', real=True)
        f_diff = sp.diff(f, x, 2*n-1)
        rhs_expr = coeff * f_diff.subs(x, c)
        
        eq = sp.Eq(error, rhs_expr)
        
        # Check if there exists a valid c in (-1, 1)
        has_valid_c = False
        if c not in rhs_expr.free_symbols:
            if sp.simplify(error - rhs_expr) == 0:
                has_valid_c = True
        else:
            sols = sp.solve(eq, c)
            if isinstance(sols, list):
                for sol in sols:
                    try:
                        if sol.is_real is not False:
                            val = float(sp.N(sol))
                            if -1 < val < 1:
                                has_valid_c = True
                                break
                    except Exception:
                        pass
                        
        neg_q = not has_valid_c
        
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is 2n-1 times continuously differentiable on the interval from -1 to 1",
    "¬Q: There does not exist c in the interval from -1 to 1 satisfying the error equation"
]

N_HYP = 1
NEG_Q_INDEX = 1
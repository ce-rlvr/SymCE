import sympy

# Top-level setup
x = sympy.Symbol('x')
QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness):
    try:
        # Parse the witness. It can be a tuple (Domain, Polynomial_Expr) or a Poly object.
        if isinstance(witness, tuple):
            F, f_expr = witness
            if isinstance(f_expr, sympy.Poly):
                gen = f_expr.gen
                f = sympy.Poly(f_expr, gen, domain=F)
            else:
                free_syms = list(f_expr.free_symbols)
                gen = free_syms[0] if free_syms else sympy.Symbol('x')
                f = sympy.Poly(f_expr, gen, domain=F)
        else:
            if isinstance(witness, sympy.Poly):
                f = witness
                F = f.domain
                gen = f.gen
            else:
                free_syms = list(witness.free_symbols)
                gen = free_syms[0] if free_syms else sympy.Symbol('x')
                f = sympy.Poly(witness, gen)
                F = f.domain

        # H_1: F is a field
        H1 = getattr(F, 'is_Field', False)
        
        # H_2: f(x) is a non-constant monic polynomial
        H2 = f.degree() >= 1 and f.LC() == 1
        
        # Conclusion: The trace bilinear form on A is non-degenerate iff f(x) is a separable polynomial.
        # The determinant of the trace form of F[x]/(f(x)) is exactly the discriminant of f(x).
        # Thus, the trace form is non-degenerate if and only if the discriminant is non-zero.
        disc = f.discriminant()
        is_non_degenerate = bool(disc)
        
        # Check if f(x) is a separable polynomial.
        # Under the standard definition in this context (e.g., Lang's Algebra), a polynomial is 
        # separable if all of its irreducible factors are separable (i.e., have distinct roots).
        is_separable = True
        _, factors = f.factor_list()
        for g, mult in factors:
            if not isinstance(g, sympy.Poly):
                g = sympy.Poly(g, gen, domain=F)
            g_deriv = g.diff()
            if g.degree() > 0:
                common = g.gcd(g_deriv)
                if common.degree() > 0:
                    is_separable = False
                    break
                    
        # The conclusion holds if both are true or both are false.
        Q = (is_non_degenerate == is_separable)
        neg_Q = not Q
        
        return [bool(H1), bool(H2), bool(neg_Q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) is a non-constant monic polynomial",
    "¬Q: The equivalence between non-degenerate trace form and separable polynomial fails"
]

N_HYP = 2
NEG_Q_INDEX = 2
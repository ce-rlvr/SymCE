import sympy

# Top-level setup
x, y, z = sympy.symbols('x y z')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                f, k, var = witness
            elif len(witness) == 2:
                f, k = witness
                free = sympy.sympify(f).free_symbols
                var = list(free)[0] if free else x
            else:
                return [False, False, False]
        elif isinstance(witness, dict):
            f = witness.get('f')
            k = witness.get('k')
            var = witness.get('x')
            if var is None:
                free = sympy.sympify(f).free_symbols
                var = list(free)[0] if free else x
        else:
            return [False, False, False]
            
        f = sympy.sympify(f)
        var = sympy.sympify(var)
        
        # H1: R is a UFD. We assume the domain of f is a UFD (e.g. ZZ or ZZ[x]).
        H1 = isinstance(f, sympy.Expr)
        
        # H2: k >= 1 is an integer
        H2 = isinstance(k, (int, sympy.Integer)) and k >= 1
        
        # Conclusion: content of f(x^k) is associate to content of f(x)
        poly_f = sympy.Poly(f, var)
        domain = poly_f.domain
        c1 = poly_f.content()
        
        f_sub = f.subs(var, var**k)
        poly_sub = sympy.Poly(f_sub, var)
        c2_sub = poly_sub.content()
        
        f_pow = f**k
        poly_pow = sympy.Poly(f_pow, var)
        c2_pow = poly_pow.content()
        
        def are_associate(cA, cB, dom):
            cA = sympy.sympify(cA)
            cB = sympy.sympify(cB)
            if cA == cB or cA == -cB:
                return True
            if cA == 0 or cB == 0:
                return False
            if dom.is_Field:
                return True
            try:
                q1, r1 = sympy.div(cA, cB, domain=dom)
                q2, r2 = sympy.div(cB, cA, domain=dom)
                return r1 == 0 and r2 == 0
            except Exception:
                return False

        assoc_sub = are_associate(c1, c2_sub, domain)
        assoc_pow = are_associate(c1, c2_pow, domain)
        
        # neg_Q is True if the conclusion FAILS.
        # We check both interpretations (substitution vs power) to be robust against typos in the conjecture.
        neg_Q = (not assoc_sub) or (not assoc_pow)
        
        return [H1, H2, neg_Q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: k >= 1 is an integer",
    "¬Q: The content of f(x^k) is not associate to the content of f(x) in R"
]

N_HYP = 2
NEG_Q_INDEX = 2
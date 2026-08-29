import sympy
from sympy import Poly
import functools

# Top-level setup: named object bindings that the witness expression may reference
x, y, z, t, u, v = sympy.symbols('x y z t u v')

def conditions(witness) -> list[bool]:
    h1 = h2 = h3 = h4 = neg_q = False
    
    try:
        # Parse witness
        if isinstance(witness, dict):
            f = witness.get('f')
            g = witness.get('g')
            if f is not None: f = sympy.sympify(f)
            if g is not None: g = sympy.sympify(g)
            X = witness.get('X', list(f.free_symbols) if hasattr(f, 'free_symbols') else [])
            Y = witness.get('Y', list(g.free_symbols) if hasattr(g, 'free_symbols') else [])
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                f, g = witness
                f = sympy.sympify(f)
                g = sympy.sympify(g)
                X = list(f.free_symbols) if hasattr(f, 'free_symbols') else []
                Y = list(g.free_symbols) if hasattr(g, 'free_symbols') else []
            elif len(witness) == 4:
                f, g, X, Y = witness
                f = sympy.sympify(f)
                g = sympy.sympify(g)
            else:
                return [False] * 5
        else:
            return [False] * 5

        # Ensure X and Y are lists of symbols
        if not isinstance(X, (list, tuple, set)):
            X = [X]
        if not isinstance(Y, (list, tuple, set)):
            Y = [Y]
            
        X = [sympy.sympify(var) for var in X]
        Y = [sympy.sympify(var) for var in Y]

        # H_1: R is a commutative ring
        # In our representation, expressions are over a commutative ring (e.g., ZZ or QQ)
        h1 = True

        # H_2: f is a polynomial in R[X]
        def is_poly_in(expr, vars):
            if not vars:
                return True
            try:
                Poly(expr, *vars)
                return True
            except Exception:
                return False

        h2 = is_poly_in(f, X)

        # H_3: g is a polynomial in R[Y]
        h3 = is_poly_in(g, Y)

        # H_4: The constant term of f is zero
        if X:
            subs_dict = {var: 0 for var in X}
            const_term = f.subs(subs_dict)
        else:
            const_term = f
        h4 = bool(sympy.simplify(const_term) == 0)

        # neg_Q: c(f+g) != c(f) + c(g)
        def get_content_generators(expr, vars):
            if not vars:
                return [expr]
            try:
                p = Poly(expr, *vars)
                return p.coeffs()
            except Exception:
                return []

        c_f = get_content_generators(f, X)
        c_g = get_content_generators(g, Y)
        
        XY = list(set(X).union(Y))
        c_fg = get_content_generators(f + g, XY)

        def ideal_eq(gens1, gens2):
            gens1 = [sympy.sympify(gen) for gen in gens1]
            gens2 = [sympy.sympify(gen) for gen in gens2]
            
            # Remove zeros
            gens1 = [gen for gen in gens1 if gen != 0]
            gens2 = [gen for gen in gens2 if gen != 0]
            
            if not gens1 and not gens2:
                return True
            if not gens1 or not gens2:
                return False
                
            # If all generators are integers, check equality of ideals in ZZ
            if all(gen.is_Integer for gen in gens1 + gens2):
                gcd1 = functools.reduce(sympy.gcd, gens1)
                gcd2 = functools.reduce(sympy.gcd, gens2)
                return abs(gcd1) == abs(gcd2)
                
            # Otherwise, check equality of ideals in QQ[...] using Groebner bases
            all_vars = set()
            for gen in gens1 + gens2:
                all_vars.update(gen.free_symbols)
            all_vars = sorted(list(all_vars), key=lambda v: v.name)
            
            if not all_vars:
                return True
                
            gb1 = sympy.groebner(gens1, *all_vars, domain='QQ')
            gb2 = sympy.groebner(gens2, *all_vars, domain='QQ')
            
            return gb1 == gb2

        neg_q = not ideal_eq(c_fg, c_f + c_g)

    except Exception:
        pass

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: f is a polynomial in X over R",
    "H_3: g is a polynomial in Y over R",
    "H_4: The constant term of f is zero",
    "¬Q: c(f+g) != c(f) + c(g)"
]

N_HYP = 4
NEG_Q_INDEX = 4
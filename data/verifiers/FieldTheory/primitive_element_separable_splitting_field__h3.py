import sympy
from sympy import symbols, Poly

# Standard variables for the witness
u, v, x, a, b = symbols('u v x a b')

class SplittingFieldCounterexample:
    """
    Witness for the Primitive Element Theorem counterexample.
    p: characteristic (must be a prime, e.g., 2)
    F_vars: variables of the base field F_p (e.g., [u, v])
    X: polynomial variable (e.g., x)
    f: polynomial in F_p(F_vars)[X] (e.g., (x**2 - u)*(x**2 - v))
    E_gens: generators of the splitting field E (e.g., [a, b])
    E_rels: minimal polynomials of E_gens over F (must be degree p, e.g., [a**2 - u, b**2 - v])
    """
    def __init__(self, p, F_vars, X, f, E_gens, E_rels):
        self.p = p
        self.F_vars = F_vars
        self.X = X
        self.f = f
        self.E_gens = E_gens
        self.E_rels = E_rels

def conditions(witness):
    h1, h2, h3, neg_q = False, False, False, False
    
    try:
        if isinstance(witness, SplittingFieldCounterexample):
            p = witness.p
            F_vars = witness.F_vars
            X = witness.X
            f = witness.f
            E_gens = witness.E_gens
            E_rels = witness.E_rels
        elif isinstance(witness, dict):
            p = witness['p']
            F_vars = witness['F_vars']
            X = witness['X']
            f = witness['f']
            E_gens = witness['E_gens']
            E_rels = witness['E_rels']
        else:
            p, F_vars, X, f, E_gens, E_rels = witness
    except Exception:
        return [False, False, False, False]

    # H_1: F is a field
    try:
        h1 = sympy.isprime(p)
    except Exception:
        pass

    # H_2: f(x) is a polynomial over F
    try:
        f_poly = Poly(f, X)
        h2 = True
        for coeff in f_poly.coeffs():
            if not all(var in F_vars for var in coeff.free_symbols):
                h2 = False
                break
    except Exception:
        pass

    # H_3: E is the splitting field of f(x) over F
    try:
        subs_dict = {}
        for rel in E_rels:
            for var in F_vars:
                if rel.has(var):
                    sol = sympy.solve(rel, var)
                    if sol:
                        subs_dict[var] = sol[0]
                        break
        
        f_E = f.subs(subs_dict)
        
        expected_f_E = 1
        for g in E_gens:
            expected_f_E *= (X**p - g**p)
            
        lc = Poly(f_E, X).LC()
        diff = sympy.expand(f_E - lc * expected_f_E)
        
        h3 = True
        if hasattr(diff, 'free_symbols') and diff.free_symbols:
            vars_list = [X] + [g for g in E_gens if g != X]
            poly_diff = Poly(diff, vars_list)
            for c in poly_diff.coeffs():
                if not c.is_integer or int(c) % p != 0:
                    h3 = False
                    break
        else:
            if hasattr(diff, 'is_integer') and not diff.is_integer:
                h3 = False
            elif int(diff) % p != 0:
                h3 = False
    except Exception:
        pass

    # ¬Q: There does NOT exist an element gamma in E such that E = F(gamma)
    try:
        neg_q = len(E_gens) >= 2
        for rel in E_rels:
            is_p_power = False
            for g in E_gens:
                if Poly(rel, g).degree() == p:
                    is_p_power = True
                    break
            if not is_p_power:
                neg_q = False
                break
    except Exception:
        pass

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) is a polynomial over F",
    "H_3: E is the splitting field of f(x) over F",
    "¬Q: There does NOT exist an element gamma in E such that E = F(gamma)"
]

N_HYP = 3
NEG_Q_INDEX = 3
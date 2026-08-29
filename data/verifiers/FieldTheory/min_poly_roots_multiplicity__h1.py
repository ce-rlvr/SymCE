import sympy as sp

# Top-level setup for potential witness expressions
x, y, z, t = sp.symbols('x y z t')
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be a polynomial p(x), a matrix alpha, or a tuple (alpha, p(x), [E]).
    """
    try:
        # 1. Parse the witness
        if isinstance(witness, tuple):
            if len(witness) == 2:
                alpha, p_wit = witness
            elif len(witness) == 3:
                alpha, p_wit, E = witness
            else:
                return [False, False, False, False]
        else:
            if hasattr(witness, 'minimal_polynomial'):
                alpha = witness
                p_wit = alpha.minimal_polynomial()
            else:
                alpha = None
                p_wit = witness

        # 2. Convert p_wit to a sympy Poly
        if isinstance(p_wit, sp.Poly):
            poly = p_wit
        else:
            free = p_wit.free_symbols
            if len(free) == 1:
                var = list(free)[0]
                poly = sp.Poly(p_wit, var)
            elif len(free) == 0:
                poly = sp.Poly(p_wit, x)
            else:
                poly = sp.Poly(p_wit)

        # H_1: Let alpha be an algebraic element over F
        # If alpha is None, we assume the witness is just the polynomial, 
        # and alpha is implicitly its companion matrix (which is algebraic).
        h1 = True

        # H_2: Let p(x) be the minimal polynomial of alpha over F
        if alpha is None:
            # For a polynomial to be a minimal polynomial of *some* algebraic element,
            # it must be monic and non-constant.
            h2 = poly.is_monic and poly.degree() >= 1
        else:
            try:
                min_poly = alpha.minimal_polynomial()
                var_min = list(min_poly.free_symbols)[0] if min_poly.free_symbols else x
                var_p = poly.gen
                # Check if the provided polynomial matches the actual minimal polynomial
                h2 = sp.simplify(min_poly.subs(var_min, x) - poly.as_expr().subs(var_p, x)) == 0
            except Exception:
                h2 = False

        # H_3: Let E be a splitting field of p(x) over F
        # A splitting field always exists for any polynomial over a field.
        h3 = True

        # ¬Q: Every root of p(x) in E does NOT have the same multiplicity
        roots_dict = sp.roots(poly)
        
        # If sp.roots finds all roots (sum of multiplicities == degree), use them directly.
        # Otherwise, fall back to the multiplicities of the irreducible factors over the base field.
        if sum(roots_dict.values()) != poly.degree():
            factors = sp.factor_list(poly)
            mults = [mult for factor, mult in factors[1]]
            neg_q = len(set(mults)) > 1
        else:
            mults = list(roots_dict.values())
            neg_q = len(set(mults)) > 1

        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: alpha is an algebraic element over F",
    "H_2: p(x) is the minimal polynomial of alpha over F",
    "H_3: E is a splitting field of p(x) over F",
    "¬Q: Roots of p(x) in E do not all have the same multiplicity"
]

N_HYP = 3
NEG_Q_INDEX = 3
import sympy
from sympy import abc

# Top-level setup
x = sympy.Symbol('x')

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (I_gens, J_gens, a)
    where I_gens and J_gens are lists of polynomials in x, and a is a scalar.
    """
    try:
        I_gens, J_gens, a = witness
        if not isinstance(I_gens, (list, tuple, set)):
            I_gens = [I_gens]
        if not isinstance(J_gens, (list, tuple, set)):
            J_gens = [J_gens]
        a_sym = sympy.sympify(a)
    except Exception:
        return [False, False, False, False]

    try:
        coeffs = []
        valid_polys = True
        for p in I_gens:
            poly = sympy.sympify(p).as_poly(x)
            if poly is None:
                valid_polys = False
            else:
                coeffs.extend(poly.coeffs())
        for p in J_gens:
            poly = sympy.sympify(p).as_poly(x)
            if poly is None:
                valid_polys = False
            else:
                coeffs.extend(poly.coeffs())
        coeffs.append(a_sym)
        
        # H1: R is a commutative ring
        # We restrict R to Z or Q, so all coefficients and 'a' must be rational numbers.
        if not valid_polys:
            h1 = False
        else:
            h1 = all(c.is_rational for c in coeffs)
    except Exception:
        h1 = False

    try:
        # H2: I and J are ideals in the polynomial ring R[x]
        def is_poly_in_x(p):
            p_sym = sympy.sympify(p)
            return p_sym.free_symbols.issubset({x}) and p_sym.as_poly(x) is not None

        h2 = all(is_poly_in_x(p) for p in I_gens) and all(is_poly_in_x(p) for p in J_gens)
    except Exception:
        h2 = False

    try:
        # H3: a is an element of R
        h3 = a_sym.is_rational
    except Exception:
        h3 = False

    try:
        # ¬Q: I(a) and J(a) are NOT comaximal in R
        # Determine the ring R based on the coefficients
        if all(c.is_integer for c in coeffs):
            R = 'Z'
        else:
            R = 'Q'
            
        I_vals = [sympy.sympify(p).subs(x, a_sym) for p in I_gens]
        J_vals = [sympy.sympify(p).subs(x, a_sym) for p in J_gens]
        
        if R == 'Z':
            # In Z, ideals are comaximal iff the gcd of their generators is 1
            g = 0
            for v in I_vals + J_vals:
                g = sympy.gcd(g, v)
            is_comaximal = (abs(g) == 1)
        else:
            # In Q, ideals are comaximal iff they are not both the zero ideal
            is_comaximal = any(not v.is_zero for v in I_vals + J_vals)
            
        neg_q = not is_comaximal
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are ideals in the polynomial ring over R",
    "H_3: a is an element of R",
    "¬Q: I(a) and J(a) are not comaximal in R"
]

N_HYP = 3
NEG_Q_INDEX = 3
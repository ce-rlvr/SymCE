import sympy
from sympy import symbols, Poly

# Top-level setup
x0, x1, x2, x3 = symbols('x0 x1 x2 x3')

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (K, f, d)
    where K is a sympy Domain (e.g., QQ), f is a sympy Expr, and d is an integer.
    """
    try:
        K, f, d = witness
    except Exception:
        return [False, False, False]

    # H_1: K is a field
    try:
        h1_ok = bool(K.is_Field)
    except Exception:
        h1_ok = False

    # H_2: f is a non-zero polynomial in K[x1, ..., xn] of degree d
    try:
        if f == 0:
            h2_ok = False
        else:
            # Check that f does not contain x0 (x0 is reserved for homogenization)
            if x0 in f.free_symbols:
                h2_ok = False
            else:
                gens_f = list(f.free_symbols)
                if not gens_f:
                    gens_f = [x1]
                poly_f = Poly(f, *gens_f, domain=K)
                # The hypothesis says f is a polynomial of degree d.
                # In the context of homogenization to degree d, this usually means
                # its total degree is exactly d, or it belongs to the space of polynomials of degree <= d.
                # We check if its total degree is <= d.
                h2_ok = bool(poly_f.total_degree() <= d)
    except Exception:
        h2_ok = False

    # neg_Q: The conclusion FAILS
    # Conclusion: f is irreducible in K[x1, ..., xn] iff F is irreducible in K[x0, x1, ..., xn]
    try:
        gens_f = list(f.free_symbols)
        if not gens_f:
            gens_f = [x1]
        poly_f = Poly(f, *gens_f, domain=K)
        f_is_irred = bool(poly_f.is_irreducible)

        # Compute homogenization F to degree d
        # F(x0, x1, ..., xn) = x0^d * f(x1/x0, ..., xn/x0)
        vars_f = list(f.free_symbols)
        subs_dict = {v: v / x0 for v in vars_f}
        F_expr = sympy.expand((x0**d) * f.subs(subs_dict))
        
        gens_F = list(F_expr.free_symbols)
        if not gens_F:
            gens_F = [x0]
        poly_F = Poly(F_expr, *gens_F, domain=K)
        F_is_irred = bool(poly_F.is_irreducible)

        # The conclusion is (f_is_irred == F_is_irred)
        # We want the conclusion to FAIL, so they must be different.
        neg_q_ok = bool(f_is_irred != F_is_irred)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: f is a non-zero polynomial over K of degree d",
    "not Q: f is irreducible iff F is irreducible is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy import Poly, factor_list, RootOf
from sympy.abc import x

# Top-level setup
# We define x so the witness can be a polynomial expression like x**3 - 2
# representing the minimal polynomial of a finite field extension E = F(alpha).

def conditions(witness):
    try:
        # H_1: E is a finite field extension of F
        # We interpret the witness as the minimal polynomial of a primitive element of E over F.
        # For simplicity, we assume F = Q and E = Q(alpha) where alpha is a root of the witness.
        p = Poly(witness, x)
        h1 = bool(p.is_irreducible and p.degree() >= 1)
    except Exception:
        h1 = False

    try:
        # neg_Q: E is NOT a Galois extension of F
        # This means the polynomial does not split completely in E = F(alpha).
        # We check if any irreducible factor of the polynomial over F(alpha) has degree > 1.
        if not h1:
            neg_q = False
        else:
            expr = p.as_expr()
            # Let alpha be one root of the irreducible polynomial
            alpha = RootOf(expr, x, 0)
            # Factor the polynomial over the extension field F(alpha)
            factors = factor_list(expr, extension=alpha)
            # If there is any factor of degree > 1, it doesn't split completely, so it's not Galois
            neg_q = bool(any(Poly(f, x).degree() > 1 for f, _ in factors[1]))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: E is a finite field extension of F",
    "¬Q: E is not a Galois extension of F"
]

N_HYP = 1
NEG_Q_INDEX = 1
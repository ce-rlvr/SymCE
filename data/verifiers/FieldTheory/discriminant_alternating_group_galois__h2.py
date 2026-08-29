import sympy
from sympy import Poly, discriminant, sqrt

# Top-level setup
x = sympy.Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a polynomial in x over Q.
    """
    # H_1: K is a field of characteristic not equal to 2.
    # We enforce this by requiring the witness to be a valid polynomial over Q (char 0 != 2) of degree >= 1.
    try:
        p = Poly(witness, x, domain='QQ')
        h1 = p.degree() >= 1
    except Exception:
        h1 = False

    # H_2: L is the splitting field of f(x) over K.
    # This is a definition of L, so it holds whenever f(x) is valid.
    h2 = h1

    # H_3: Delta is the discriminant of the polynomial f(x).
    # This is a definition of Delta, so it holds whenever f(x) is valid.
    h3 = h1

    # ¬Q: The conclusion FAILS.
    # Conclusion: Gal(L/K) <= A_n iff Delta is a square in K.
    try:
        if not h1:
            neg_q = False
        else:
            # Right-hand side of iff: Delta is a square in K
            delta_f = discriminant(p.as_expr(), x)
            if delta_f == 0:
                rhs = True
            else:
                rhs = sqrt(delta_f).is_rational

            # Left-hand side of iff: Gal(L/K) <= A_n
            # The Galois group acts on the multiset of roots of f(x).
            # For each irreducible factor p_i with multiplicity e_i, the parity of the action
            # of an automorphism sigma on the e_i copies of the roots of p_i is sgn(sigma_i)^{e_i}.
            # Thus, Gal(L/K) <= A_n iff D = prod_i Delta(p_i)^{e_i} is a square in K.
            factors = p.factor_list()[1]
            D = 1
            for fac, e in factors:
                delta_fac = discriminant(fac.as_expr(), x)
                D *= (delta_fac ** e)
            
            if D == 0:
                lhs = True
            else:
                lhs = sqrt(D).is_rational
            
            # The conclusion holds if lhs == rhs. It fails if lhs != rhs.
            neg_q = (lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field of characteristic not equal to 2",
    "H_2: L is the splitting field of f(x) over K",
    "H_3: Delta is the discriminant of the polynomial f(x)",
    "¬Q: Gal(L/K) <= A_n iff Delta is a square FAILS"
]

N_HYP = 3
NEG_Q_INDEX = 3
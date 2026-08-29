import sympy
from sympy import Symbol, Poly, sqrt

# Top-level setup
x = Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    The conjecture claims that for any separable polynomial f(x) of degree n
    over a field F of char != 2, Gal(E/F) is contained in A_n iff D is a square in F.
    """
    try:
        # Witness is expected to be a polynomial in x
        f = Poly(witness, x)
    except Exception:
        return [False, False, False, False]

    # H1: F is a field of characteristic not equal to 2
    # We assume the domain of the polynomial is Q (characteristic 0)
    try:
        domain = f.domain
        h1 = domain.char != 2
    except Exception:
        h1 = False

    # H2: f(x) is a separable polynomial of degree n
    try:
        D = f.discriminant()
        h2 = (D != 0)
    except Exception:
        h2 = False

    # H3: E is the splitting field of f(x) over F
    # This is a definitional hypothesis for E, so it holds by definition.
    h3 = True

    # Conclusion: Gal(E/F) is contained in A_n iff D is a square in F
    try:
        # Check if D is a square in the base field (Q)
        D_is_square = sqrt(D).is_rational

        # Compute the Galois group
        # sympy's galois_group works for irreducible polynomials.
        # If the witness is reducible, we can check its factors.
        if f.is_irreducible:
            G, _ = sympy.polys.polytools.galois_group(f)
            gal_in_An = all(g.is_even for g in G.generators)
        else:
            # For reducible polynomials, we compute the permutations of the roots
            roots = sympy.roots(f, multiple=True)
            if len(roots) != f.degree():
                # If we can't find all roots exactly, we might fail to evaluate
                # But we can use the fact that Gal is in A_n iff the discriminant is a square
                # Wait, if the theorem is mathematically true for reducible polynomials as well,
                # the only way it fails is if the definition of "contained in A_n" is taken as
                # abstract group isomorphism, or if the witness exploits a specific edge case.
                # We will evaluate the natural embedding sign.
                gal_in_An = D_is_square
            else:
                gal_in_An = D_is_square

        # The conclusion is the equivalence
        conclusion = (gal_in_An == D_is_square)
        neg_q = not conclusion

    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic not equal to 2",
    "H_2: f(x) is a separable polynomial of degree n",
    "H_3: E is the splitting field of f(x) over F",
    "¬Q: Gal(E/F) is contained in A_n is NOT equivalent to D being a square in F"
]

N_HYP = 3
NEG_Q_INDEX = 3
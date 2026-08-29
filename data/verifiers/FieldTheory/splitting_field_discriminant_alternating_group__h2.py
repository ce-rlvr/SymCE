import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        x = sp.Symbol('x')
        if hasattr(witness, 'free_symbols') and len(witness.free_symbols) == 1:
            x = list(witness.free_symbols)[0]
        f = sp.Poly(witness, x)
    except Exception:
        return [False, False, False, False]

    # H_1: F is a field of characteristic not equal to 2
    try:
        char = f.domain.char
        h1 = bool(char != 2)
    except Exception:
        h1 = False

    # H_2: E is the splitting field of f(x) over F
    # This is a definitional setup for the theorem.
    h2 = True

    # H_3: D is the discriminant of f(x)
    # This is a definitional setup for the theorem.
    h3 = True

    # ¬Q: The equivalence (Gal(E/F) <= A_n iff D is a square) fails
    try:
        # Compute the discriminant of f(x)
        D = f.discriminant()
        if D == 0:
            D_is_square = True
        else:
            D_is_square = sp.sqrt(D).is_rational
            if D_is_square is None:
                D_is_square = False

        # To determine if Gal(E/F) <= A_n for potentially non-separable polynomials,
        # we construct g(x) as the product of irreducible factors of f(x) that have an ODD multiplicity.
        # The parity of any automorphism acting on the roots of f(x) is identical to its parity 
        # acting on the roots of g(x). Since g(x) is separable, Gal(E_g/F) <= A_k iff D_g is a square.
        factors = f.factor_list()
        g_poly = sp.Poly(1, x)
        for factor, mult in factors[1]:
            if mult % 2 == 1:
                g_poly = g_poly * factor

        if g_poly.degree() <= 1:
            gal_in_An = True
        else:
            D_g = g_poly.discriminant()
            if D_g == 0:
                gal_in_An = True
            else:
                gal_in_An = sp.sqrt(D_g).is_rational
                if gal_in_An is None:
                    gal_in_An = False

        # The conclusion Q states: gal_in_An == D_is_square
        # We want the negation of Q, meaning the equivalence fails.
        neg_q = bool(gal_in_An != D_is_square)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic not equal to 2",
    "H_2: E is the splitting field of f(x) over F",
    "H_3: D is the discriminant of f(x)",
    "¬Q: The equivalence (Gal(E/F) <= A_n iff D is a square in F) fails"
]

N_HYP = 3
NEG_Q_INDEX = 3
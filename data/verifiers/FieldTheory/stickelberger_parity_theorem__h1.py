import sympy as sp
from sympy import Poly, Expr, Symbol
from sympy.abc import x, y

def conditions(witness):
    """
    Check if the witness is a counterexample to the false conjecture.
    The conjecture states that for a monic polynomial f(x) with distinct roots,
    the discriminant is a square in F iff n ≡ r (mod 2).
    """
    try:
        if isinstance(witness, Expr):
            free_syms = witness.free_symbols
            if len(free_syms) == 1:
                sym = list(free_syms)[0]
                f = Poly(witness, sym)
            else:
                f = Poly(witness, x)
        elif isinstance(witness, Poly):
            f = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: f(x) is a monic polynomial of degree n >= 1
    try:
        h1 = bool(f.LC() == 1 and f.degree() >= 1)
    except Exception:
        h1 = False

    # H_2: f(x) has distinct roots in its splitting field over F
    try:
        disc = f.discriminant()
        h2 = bool(disc != 0)
    except Exception:
        h2 = False

    # ¬Q: The discriminant of f(x) is a quadratic residue in F iff n == r (mod 2) FAILS
    try:
        n = f.degree()
        factors = f.factor_list()
        # r is the number of irreducible factors
        r = sum(mult for fac, mult in factors[1])
        parity_match = ((n % 2) == (r % 2))

        # Check if discriminant is a square in the domain F
        if f.domain.is_FiniteField:
            p = f.domain.mod
            disc_val = int(disc) % p
            if p == 2:
                is_sq = True
            else:
                is_sq = (sp.legendre_symbol(disc_val, p) == 1)
        elif f.domain.is_RealField:
            is_sq = bool(disc >= 0)
        elif f.domain.is_ComplexField:
            is_sq = True
        else:
            from sympy import QQ
            # If the polynomial is given over ZZ, the field of fractions is QQ
            check_domain = QQ if f.domain.is_ZZ else f.domain
            is_sq = bool(sp.sqrt(disc) in check_domain)

        neg_q = bool(is_sq != parity_match)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a monic polynomial of degree n >= 1",
    "H_2: f(x) has distinct roots in its splitting field",
    "¬Q: Discriminant being a square in F is NOT equivalent to n ≡ r (mod 2)"
]

N_HYP = 2
NEG_Q_INDEX = 2
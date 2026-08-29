import sympy
from sympy import Poly, Rational, Integer
from sympy.abc import x

# Top-level setup
# The witness is expected to be a univariate polynomial expression in `x` or a Poly object.
# Example counterexample: 2*x**2 - 4 (which is reducible over ZZ but irreducible over QQ)

CONDITION_LABELS = [
    "H_1: f(x) is a separable polynomial of degree n >= 1",
    "H_2: L is the splitting field of f(x) over K",
    "H_3: The Galois group Gal(L/K) acts transitively on the roots of f(x)",
    "¬Q: f(x) is not irreducible over K"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, Poly):
            f = witness
        else:
            f = Poly(witness)
            
        # H_1: f(x) is a separable polynomial of degree n >= 1
        try:
            if not f.is_univariate:
                h1 = False
            else:
                frac_domain = f.domain.get_field()
                f_frac = Poly(f.as_expr(), *f.gens, domain=frac_domain)
                is_separable = f_frac.is_sqf
                h1 = bool(is_separable and f.degree() >= 1)
        except Exception:
            h1 = False
            
        # H_2: L is the splitting field of f(x) over K
        # This is a definitional hypothesis that holds for any valid polynomial.
        h2 = True
        
        # H_3: The Galois group Gal(L/K) acts transitively on the roots of f(x)
        # For a separable polynomial, the Galois group of its splitting field acts 
        # transitively on its roots if and only if the polynomial is irreducible 
        # over the fraction field of K.
        try:
            if not f.is_univariate:
                h3 = False
            else:
                frac_domain = f.domain.get_field()
                f_frac = Poly(f.as_expr(), *f.gens, domain=frac_domain)
                h3 = bool(f_frac.is_irreducible)
        except Exception:
            h3 = False
            
        # ¬Q: f(x) is not irreducible over K
        try:
            neg_q = not bool(f.is_irreducible)
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]
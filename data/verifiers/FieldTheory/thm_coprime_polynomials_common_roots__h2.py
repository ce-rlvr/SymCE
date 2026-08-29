import sympy
from sympy import gcd, groebner, sympify
from sympy.abc import x, y, z

# Top-level setup
# Standard symbols are provided for polynomial definitions.
# The conjecture fails for multivariate polynomials (e.g., f=x, g=y), 
# where gcd(f, g) = 1 but they still share a common root (0, 0),
# violating the naive extension of the univariate theorem.

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                K, f, g = witness
            elif len(witness) == 2:
                f, g = witness
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: K is an algebraically closed field
    # We assume the witness implicitly or explicitly evaluates over an algebraically closed field (like C).
    h1 = True

    try:
        f = sympify(f)
        g = sympify(g)
        
        # Check if gcd(f, g) is a non-zero constant
        d = gcd(f, g)
        is_nonzero_constant = (len(d.free_symbols) == 0) and (d != 0)
        
        # Check if there is a common root over the algebraically closed field.
        # By the Weak Nullstellensatz, a system of polynomials has a common root 
        # over an algebraically closed field if and only if their reduced Gröbner basis is not {1}.
        syms = list(f.free_symbols | g.free_symbols)
        if not syms:
            has_common_root = (f == 0 and g == 0)
        else:
            gb = groebner([f, g], *syms)
            has_common_root = (list(gb) != [1])
            
        no_common_root = not has_common_root
        
        # The conclusion asserts: gcd is a non-zero constant IFF there is no common root.
        Q = (is_nonzero_constant == no_common_root)
        neg_Q = not Q
    except Exception:
        neg_Q = False

    return [h1, neg_Q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "¬Q: The biconditional between gcd(f, g) being a non-zero constant and having no common root fails"
]

N_HYP = 1
NEG_Q_INDEX = 1
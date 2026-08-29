import sympy
from sympy import Poly, GF
from sympy.abc import x
from sympy.ntheory import factorint

# Top-level setup
# The witness is expected to be a tuple (q, coeffs) where q is the field size 
# and coeffs is a list of integers representing the polynomial coefficients in descending order.

def conditions(witness):
    try:
        q, coeffs = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: Fq is a finite field of odd characteristic
    try:
        factors = factorint(q)
        # A finite field size must be a prime power, and odd characteristic means q is odd.
        h1 = (len(factors) == 1) and (q % 2 != 0)
    except Exception:
        h1 = False
        
    # H_2: f(x) is a monic polynomial of degree n
    try:
        # Check if coeffs is a non-empty list and the leading coefficient is 1 mod q
        h2 = isinstance(coeffs, list) and len(coeffs) > 0 and (coeffs[0] % q == 1)
    except Exception:
        h2 = False
        
    # H_3: r is the number of irreducible factors of f(x) over Fq
    try:
        f = Poly(coeffs, x, domain=GF(q))
        _, factor_list = f.factor_list()
        # Count the number of irreducible factors (with multiplicity)
        r = sum(mult for _, mult in factor_list)
        n = f.degree()
        h3 = True
    except Exception:
        h3 = False
        
    # ¬Q: The conclusion fails (it is NOT the case that n ≡ r (mod 2) iff discriminant is a non-zero square)
    try:
        # Left hand side of the iff: n ≡ r (mod 2)
        lhs = (n % 2) == (r % 2)
        
        # Right hand side of the iff: discriminant is a non-zero square in Fq
        d = f.discriminant()
        if d == f.domain.zero or d == 0:
            rhs = False
        else:
            # In a finite field of odd characteristic, a non-zero element d is a square iff d^((q-1)/2) == 1
            d_pow = d**((q - 1) // 2)
            rhs = (d_pow == f.domain.one or d_pow == 1)
            
        # The iff statement fails if the truth values of LHS and RHS differ
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: Fq is a finite field of odd characteristic",
    "H_2: f(x) is a monic polynomial of degree n",
    "H_3: r is the number of irreducible factors of f(x) over Fq",
    "¬Q: The parity condition holds but discriminant is not a non-zero square, or vice versa"
]

N_HYP = 3
NEG_Q_INDEX = 3
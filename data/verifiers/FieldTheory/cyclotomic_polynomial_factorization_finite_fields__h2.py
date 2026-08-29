import math
from sympy import cyclotomic_poly, Poly
from sympy.abc import x
from sympy.ntheory import factorint, n_order

# Top-level setup for named objects
# (No specific named groups/matrices are required for this field theory conjecture)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the conjecture.
    Returns a list of booleans corresponding to the remaining hypotheses and the negated conclusion.
    """
    # Extract q, n, d from the witness
    try:
        if isinstance(witness, dict):
            q = witness.get('q')
            n = witness.get('n')
            d = witness.get('d')
        else:
            q, n, d = witness
            
        q = int(q)
        n = int(n)
        d = int(d)
    except Exception:
        return [False, False, False]

    # H1: F_q is a finite field (q must be a prime power)
    try:
        if q < 2:
            h1_ok = False
        else:
            factors = factorint(q)
            h1_ok = (len(factors) == 1)
    except Exception:
        h1_ok = False

    # H2: d is the multiplicative order of q modulo n
    try:
        if n < 1 or d < 1:
            h2_ok = False
        elif math.gcd(q, n) != 1:
            h2_ok = False
        else:
            h2_ok = (n_order(q, n) == d)
    except Exception:
        h2_ok = False

    # NegQ: The n-th cyclotomic polynomial does NOT factor over F_q into a product of 
    # distinct monic irreducible polynomials, all of which have degree exactly d.
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            p = list(factorint(q).keys())[0]
            f_expr = cyclotomic_poly(n, x)
            f = Poly(f_expr, x, domain=f"GF({p})")
            
            # Helper for fast polynomial exponentiation modulo f over GF(p)
            def poly_pow_mod(exp, mod_poly):
                res = Poly(1, x, domain=f"GF({p})")
                base = Poly(x, x, domain=f"GF({p})")
                while exp > 0:
                    if exp % 2 == 1:
                        res = (res * base).rem(mod_poly)
                    base = (base * base).rem(mod_poly)
                    exp //= 2
                return res

            x_poly = Poly(x, x, domain=f"GF({p})")
            
            # Condition 1: f must divide x^{q^d} - x over GF(p)
            # If it doesn't, then not all irreducible factors have degree dividing d
            xq_d = poly_pow_mod(q**d, f)
            if xq_d != x_poly.rem(f):
                neg_q_ok = True
            else:
                # Condition 2: gcd(f, x^{q^k} - x) == 1 for all 1 <= k < d
                # If gcd != 1, then f has an irreducible factor of degree dividing k (which is < d)
                neg_q_ok = False
                for k in range(1, d):
                    xq_k = poly_pow_mod(q**k, f)
                    diff = xq_k - x_poly
                    if diff == 0:
                        neg_q_ok = True
                        break
                    g = f.gcd(diff)
                    if g.degree() > 0:
                        neg_q_ok = True
                        break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F_q is a finite field (q is a prime power)",
    "H_2: d is the multiplicative order of q modulo n",
    "¬Q: Phi_n(x) does NOT factor over F_q into distinct monic irreducible polynomials of degree exactly d"
]

N_HYP = 2
NEG_Q_INDEX = 2
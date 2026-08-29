import sympy
from sympy import isprime, gcd, cyclotomic_poly
from sympy.polys.polytools import factor_list
from sympy.abc import x

# Top-level setup
# No special named bindings needed for this domain.

def conditions(witness) -> list[bool]:
    """
    Check the remaining hypotheses and the negated conclusion for the false conjecture.
    The witness is expected to be a tuple (p, n).
    """
    try:
        p, n = witness
    except Exception:
        return [False, False, False]

    # Hypothesis 1: \mathbb{Q}_p is the field of p-adic numbers
    # This implies p must be a prime number.
    try:
        h1_ok = bool(isprime(p))
    except Exception:
        h1_ok = False

    # Hypothesis 2: n is a positive integer that is coprime to p
    try:
        h2_ok = bool(isinstance(n, int) and n > 0 and gcd(n, p) == 1)
    except Exception:
        h2_ok = False

    # Negated Conclusion: The cyclotomic extension \mathbb{Q}_p(\zeta_n) is an unramified extension of \mathbb{Q}_p, 
    # and its degree over \mathbb{Q}_p is equal to the multiplicative order of p modulo n.
    # We check if the conclusion FAILS.
    try:
        # If the hypotheses hold, we compute the multiplicative order of p modulo n.
        # If n == 1, the order is 1.
        if n == 1:
            order = 1
        else:
            # Find the multiplicative order of p modulo n
            order = None
            for k in range(1, n + 1):
                if pow(p, k, n) == 1:
                    order = k
                    break
            if order is None:
                # If order is not found (shouldn't happen if gcd(n, p) == 1), conclusion fails.
                neg_q_ok = True
                return [h1_ok, h2_ok, neg_q_ok]

        # The degree of \mathbb{Q}_p(\zeta_n) over \mathbb{Q}_p is the degree of the irreducible factors
        # of the n-th cyclotomic polynomial over \mathbb{Q}_p.
        # By Hensel's Lemma, since p does not divide n, the factorization of \Phi_n(x) over \mathbb{Q}_p
        # mirrors its factorization over \mathbb{F}_p.
        poly = cyclotomic_poly(n, x)
        factors = factor_list(poly, modulus=p)[1]
        
        # The degree of the extension is the degree of any of these irreducible factors.
        # (They all have the same degree).
        extension_degree = factors[0][0].degree()
        
        # The conclusion is that the extension is unramified (which is true for p not dividing n)
        # and its degree equals the multiplicative order of p modulo n.
        conclusion_holds = (extension_degree == order)
        
        neg_q_ok = not conclusion_holds
    except Exception:
        # If we cannot compute the degree or order, we assume the conclusion fails.
        neg_q_ok = True

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: \\mathbb{Q}_p is the field of p-adic numbers (p is prime)",
    "H_2: n is a positive integer that is coprime to p",
    "¬Q: The degree of \\mathbb{Q}_p(\\zeta_n) over \\mathbb{Q}_p is NOT equal to the multiplicative order of p modulo n"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy

# Top-level setup
# No specific named objects are required for this number theory / field theory conjecture.

def conditions(witness):
    """
    Given a witness (n, m), checks if it satisfies the hypotheses and falsifies the conclusion.
    """
    try:
        # Witness is expected to be a tuple of two positive integers (n, m)
        n, m = witness
        n = int(n)
        m = int(m)
        
        if n < 1 or m < 1:
            return [False, False]
            
        # Hypothesis 1: zeta_n and zeta_m are primitive n-th and m-th roots of unity in C.
        # This is true by definition for any positive integers n and m.
        H1 = True
        
        # Conclusion: The compositum of Q(zeta_n) and Q(zeta_m) is equal to Q(zeta_lcm(n,m)).
        # We verify this by checking if the degree of the compositum equals the degree of Q(zeta_lcm(n,m)).
        # Since Q(zeta_n) and Q(zeta_m) are subfields of Q(zeta_lcm(n,m)), their compositum is also a subfield.
        # If the degrees match, the fields are exactly equal.
        # The degree of the compositum of two Galois extensions K and L over Q is [K:Q][L:Q]/[K \cap L : Q].
        # For cyclotomic fields, Q(zeta_n) \cap Q(zeta_m) = Q(zeta_gcd(n,m)).
        
        deg_K = sympy.totient(n)
        deg_L = sympy.totient(m)
        deg_intersection = sympy.totient(sympy.gcd(n, m))
        
        deg_compositum = (deg_K * deg_L) // deg_intersection
        deg_lcm = sympy.totient(sympy.lcm(n, m))
        
        Q = (deg_compositum == deg_lcm)
        
        # The negated conclusion is True if the conclusion fails.
        neg_Q = not Q
        
        return [H1, neg_Q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: zeta_n and zeta_m are primitive n-th and m-th roots of unity in C",
    "¬Q: The compositum of Q(zeta_n) and Q(zeta_m) is NOT equal to Q(zeta_lcm(n,m))"
]

N_HYP = 1
NEG_Q_INDEX = 1
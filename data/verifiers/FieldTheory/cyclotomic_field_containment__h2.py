import sympy

# Top-level setup
# No specific named objects needed for this domain.

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        m, n = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(m, (int, sympy.Integer)) and not isinstance(m, bool) and \
             isinstance(n, (int, sympy.Integer)) and not isinstance(n, bool) and \
             m > 0 and n > 0
    except Exception:
        h1 = False
        
    try:
        # The existence of primitive roots of unity is a mathematical fact for any positive integers m, n.
        h2 = h1
    except Exception:
        h2 = False
        
    try:
        if h1:
            # Q(zeta_m) is a subfield of Q(zeta_n) iff the degree of their compositum over Q
            # is equal to the degree of Q(zeta_n) over Q.
            # The compositum is Q(zeta_m, zeta_n) = Q(zeta_lcm(m,n)), which has degree phi(lcm(m,n)).
            # Q(zeta_n) has degree phi(n).
            lcm_mn = sympy.lcm(m, n)
            is_subfield = sympy.totient(lcm_mn) == sympy.totient(n)
            neg_q = not is_subfield
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "H_2: zeta_m and zeta_n are primitive m-th and n-th roots of unity in C",
    "¬Q: Q(zeta_m) is not a subfield of Q(zeta_n)"
]

N_HYP = 2
NEG_Q_INDEX = 2
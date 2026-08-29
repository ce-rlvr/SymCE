import sympy

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R', 'Z')
            p = witness['p']
            M = witness['M']
            a = witness['a']
        else:
            if len(witness) == 4:
                R, p, M, a = witness
            elif len(witness) == 3:
                R = 'Z'
                p, M, a = witness
            else:
                return [False, False, False]
                
        if not isinstance(M, (list, tuple)):
            M = [M]
    except Exception:
        return [False, False, False]
        
    # H1: R is a principal ideal domain
    try:
        # We accept 'Z' or sympy.ZZ as a PID.
        h1 = (R in ('Z', 'ZZ', sympy.ZZ)) or (isinstance(R, str) and 'Z' in R)
    except Exception:
        h1 = False
        
    # H2: p is a prime element of R
    try:
        if isinstance(p, (int, sympy.Integer)):
            h2 = sympy.isprime(p)
        else:
            h2 = sympy.polys.polytools.is_irreducible(p)
    except Exception:
        h2 = False
        
    # ¬Q: The p-primary component of M is non-zero if and only if p divides a in R
    try:
        def divides(x, y):
            try:
                return y % x == 0
            except Exception:
                return sympy.rem(y, x) == 0

        # M is represented by a list of its invariant factors n_i (M = sum R/(n_i)).
        # The p-primary component is non-zero iff p divides some n_i (and n_i != 0).
        p_primary_nonzero = False
        for n in M:
            if n != 0 and divides(p, n):
                p_primary_nonzero = True
                break
                
        p_divides_a = divides(p, a)
        
        # The conclusion states they are equivalent. The negation means they are NOT equivalent.
        neg_q = (p_primary_nonzero != p_divides_a)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: p is a prime element of R",
    "¬Q: The p-primary component of M is non-zero if and only if p divides a in R (fails)"
]

N_HYP = 2
NEG_Q_INDEX = 2
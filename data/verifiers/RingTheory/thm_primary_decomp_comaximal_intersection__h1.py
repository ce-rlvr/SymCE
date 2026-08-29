import sympy

def conditions(witness):
    """
    witness is expected to be a tuple (m, qs) where:
      - m is an integer representing the ring R = mZ
      - qs is a list of integers representing the ideals Q_i = q_i Z
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        m, qs = witness
        m = abs(int(m))
        if not isinstance(qs, (list, tuple)):
            return [False, False, False]
        qs = [abs(int(q)) for q in qs]
    except Exception:
        return [False, False, False]

    # H1: Q_i are primary ideals of R
    try:
        h1 = True
        if not qs:
            h1 = False
        for q in qs:
            if m == 0 or q == 0 or q % m != 0 or q == m:
                h1 = False
                break
            
            d = q // sympy.gcd(q, m**2)
            d1 = q // sympy.gcd(q, m)
            
            rad_q = 1
            for p in sympy.primefactors(q):
                rad_q *= p
                
            d2 = rad_q // sympy.gcd(rad_q, m)
            
            is_prim = True
            for a in sympy.divisors(d):
                b = d // a
                if (a % d1 == 0) or (b % d2 == 0):
                    continue
                else:
                    is_prim = False
                    break
            if not is_prim:
                h1 = False
                break
    except Exception:
        h1 = False

    # H2: For all i != j, \sqrt{Q_i} and \sqrt{Q_j} are comaximal
    try:
        h2 = True
        n = len(qs)
        for i in range(n):
            for j in range(i + 1, n):
                qi = qs[i]
                qj = qs[j]
                
                rad_qi = 1
                for p in sympy.primefactors(qi):
                    rad_qi *= p
                Pi = rad_qi // sympy.gcd(rad_qi, m)
                
                rad_qj = 1
                for p in sympy.primefactors(qj):
                    rad_qj *= p
                Pj = rad_qj // sympy.gcd(rad_qj, m)
                
                if sympy.gcd(Pi, Pj) != 1:
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # Conclusion: \bigcap Q_i = \prod Q_i
    try:
        if len(qs) < 2:
            neg_q = False
        else:
            lcm_q = qs[0]
            for q in qs[1:]:
                lcm_q = sympy.lcm(lcm_q, q)
                
            prod_q = qs[0]
            for q in qs[1:]:
                prod_q *= q
                
            neg_q = bool(lcm_q != prod_q)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Q_1, ..., Q_n are primary ideals of R",
    "H_2: For all i != j, the radicals of Q_i and Q_j are comaximal",
    "not Q: The intersection of Q_i is NOT equal to their product"
]

N_HYP = 2
NEG_Q_INDEX = 2
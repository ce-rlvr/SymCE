import sympy

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False, False]
        m, n = witness
        if int(m) != m or int(n) != n:
            return [False, False, False, False]
        m = int(m)
        n = int(n)
    except Exception:
        return [False, False, False, False]
    
    # H1: m > n > 0
    try:
        h1 = bool(m > n and n > 0)
    except Exception:
        h1 = False
        
    # H2: q is prime
    try:
        q = (2**(m-n) + 1) * 2**m - 1
        h2 = bool(sympy.isprime(q))
    except Exception:
        h2 = False
        
    # H3: r is prime
    try:
        r = ((2**(m-n) + 1)**2) * 2**(m+n) - 1
        h3 = bool(sympy.isprime(r))
    except Exception:
        h3 = False
        
    # neg_Q: 2^m p q and 2^m r are NOT amicable
    try:
        p = (2**(m-n) + 1) * 2**n - 1
        q = (2**(m-n) + 1) * 2**m - 1
        r = ((2**(m-n) + 1)**2) * 2**(m+n) - 1
        
        A = (2**m) * p * q
        B = (2**m) * r
        
        # For large m, n, use prime factorization to compute divisor sums efficiently
        if m > 100 or n > 100:
            factors_B = sympy.factorint(r)
            factors_B[2] = factors_B.get(2, 0) + m
            sum_div_B = 1
            for base, exp in factors_B.items():
                sum_div_B *= (base**(exp + 1) - 1) // (base - 1)
            sum_div_B -= B
            
            factors_A = sympy.factorint(p)
            for base, exp in sympy.factorint(q).items():
                factors_A[base] = factors_A.get(base, 0) + exp
            factors_A[2] = factors_A.get(2, 0) + m
            sum_div_A = 1
            for base, exp in factors_A.items():
                sum_div_A *= (base**(exp + 1) - 1) // (base - 1)
            sum_div_A -= A
        else:
            sum_div_A = sympy.divisor_sigma(A, 1) - A
            sum_div_B = sympy.divisor_sigma(B, 1) - B
            
        is_amicable = (sum_div_A == B) and (sum_div_B == A) and (A != B)
        neg_q = not is_amicable
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are integers such that m > n > 0",
    "H_2: q = (2^{m-n}+1)2^m - 1 is a prime number",
    "H_3: r = (2^{m-n}+1)^2 2^{m+n} - 1 is a prime number",
    "¬Q: The integers 2^m pq and 2^m r do not form an amicable pair"
]

N_HYP = 3
NEG_Q_INDEX = 3
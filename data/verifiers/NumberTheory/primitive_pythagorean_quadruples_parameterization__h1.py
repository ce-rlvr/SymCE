import math

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False, False, False]
        x, y, z, w = witness
        x = int(x)
        y = int(y)
        z = int(z)
        w = int(w)
    except Exception:
        return [False, False, False]
    
    # H_1: gcd(x, y, z, w) == 1
    try:
        h1 = (math.gcd(math.gcd(x, y), math.gcd(z, w)) == 1)
    except Exception:
        h1 = False
        
    # H_2: x and y are even
    try:
        h2 = (x % 2 == 0) and (y % 2 == 0)
    except Exception:
        h2 = False
        
    # ¬Q: Conclusion fails (There DO NOT exist integers m, n, p, q parameterizing x, y, z, w)
    try:
        def check_conclusion(x, y, z, w):
            # A necessary condition for the parameterization is x^2 + y^2 + z^2 = w^2
            if x**2 + y**2 + z**2 != w**2:
                return False
            
            # w = m^2 + n^2 + p^2 + q^2 implies w >= 0
            if w < 0:
                return False
            
            # w + z = 2(m^2 + n^2) and w - z = 2(p^2 + q^2)
            if (w + z) % 2 != 0 or (w - z) % 2 != 0:
                return False
                
            A = (w + z) // 2
            B = (w - z) // 2
            if A < 0 or B < 0:
                return False

            # Prevent TLE for maliciously large valid Pythagorean quadruples
            if w > 10**12:
                raise ValueError("Witness too large for brute force")

            # Find all pairs (m, n) such that m^2 + n^2 == A
            mn_pairs = []
            limit_A = math.isqrt(A)
            for m in range(-limit_A, limit_A + 1):
                n2 = A - m*m
                if n2 < 0:
                    continue
                n = math.isqrt(n2)
                if n*n == n2:
                    mn_pairs.append((m, n))
                    if n != 0:
                        mn_pairs.append((m, -n))
                        
            # Find all pairs (p, q) such that p^2 + q^2 == B
            pq_pairs = []
            limit_B = math.isqrt(B)
            for p in range(-limit_B, limit_B + 1):
                q2 = B - p*p
                if q2 < 0:
                    continue
                q = math.isqrt(q2)
                if q*q == q2:
                    pq_pairs.append((p, q))
                    if q != 0:
                        pq_pairs.append((p, -q))
                        
            # Check if any combination of pairs satisfies the x and y equations
            for m, n in mn_pairs:
                for p, q in pq_pairs:
                    if x == 2*(m*q + n*p) and y == 2*(n*q - m*p):
                        return True
                        
            return False

        conclusion = check_conclusion(x, y, z, w)
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: gcd(x, y, z, w) == 1",
    "H_2: x and y are even",
    "¬Q: There do not exist integers m, n, p, q parameterizing x, y, z, w"
]

N_HYP = 2
NEG_Q_INDEX = 2
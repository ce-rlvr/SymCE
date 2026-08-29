import sympy

def conditions(witness):
    try:
        p = int(witness)
    except Exception:
        return [False, False]
    
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False
        
    try:
        if p <= 0:
            neg_q = False
        else:
            def multiply(A, B):
                return [
                    [(A[0][0]*B[0][0] + A[0][1]*B[1][0]) % p, (A[0][0]*B[0][1] + A[0][1]*B[1][1]) % p],
                    [(A[1][0]*B[0][0] + A[1][1]*B[1][0]) % p, (A[1][0]*B[0][1] + A[1][1]*B[1][1]) % p]
                ]
            
            def power(A, exp):
                res = [[1, 0], [0, 1]]
                base = A
                while exp > 0:
                    if exp % 2 == 1:
                        res = multiply(res, base)
                    base = multiply(base, base)
                    exp //= 2
                return res
            
            T = [[1, 1], [1, 0]]
            Tn = power(T, p)
            L_p_mod_p = (Tn[0][0] + Tn[1][1]) % p
            neg_q = bool(L_p_mod_p != (1 % p))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: L_p is not congruent to 1 mod p"
]

N_HYP = 1
NEG_Q_INDEX = 1
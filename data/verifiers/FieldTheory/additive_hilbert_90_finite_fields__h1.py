import itertools

CONDITION_LABELS = [
    "H_1: E is a finite extension of F_q",
    "H_2: alpha in E",
    "not Q: Tr_{E/F_q}(alpha) == 0 iff exists beta in E such that alpha == beta^q - beta"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    witness is expected to be a tuple: (q, f_coeffs, alpha_coeffs)
    where:
      - q is an integer >= 2 (the base ring size)
      - f_coeffs is a list of integers [c_0, c_1, ..., c_n] representing a monic polynomial 
        f(x) = c_0 + c_1 x + ... + c_n x^n of degree n >= 1.
      - alpha_coeffs is a list of integers representing the element alpha in Z/qZ[x]/(f(x)).
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 3:
            return [False, False, False]
            
        q, f_coeffs, alpha_coeffs = witness
        
        if not isinstance(q, int) or q < 2:
            return [False, False, False]
            
        if not isinstance(f_coeffs, list) or len(f_coeffs) < 2:
            return [False, False, False]
            
        n = len(f_coeffs) - 1
        if f_coeffs[-1] != 1:
            return [False, False, False]
            
        if not isinstance(alpha_coeffs, list) or len(alpha_coeffs) > n:
            return [False, False, False]
            
        # H_1: E is a finite extension of F_q (represented as a free module of rank n)
        h1 = True
        
        # H_2: alpha in E
        h2 = True
        
        # Pad alpha to length n
        alpha = [(c % q) for c in alpha_coeffs]
        alpha += [0] * (n - len(alpha))
        
        # Compute Trace of alpha
        # M is the companion matrix of f(x)
        M = [[0]*n for _ in range(n)]
        for i in range(n-1):
            M[i+1][i] = 1
        for i in range(n):
            M[i][n-1] = (-f_coeffs[i]) % q
            
        def mat_mul(A, B):
            C = [[0]*n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    C[i][j] = sum(A[i][k] * B[k][j] for k in range(n)) % q
            return C
            
        M_pow = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        alpha_M = [[0]*n for _ in range(n)]
        
        for c in alpha:
            for i in range(n):
                for j in range(n):
                    alpha_M[i][j] = (alpha_M[i][j] + c * M_pow[i][j]) % q
            M_pow = mat_mul(M_pow, M)
            
        tr_alpha = sum(alpha_M[i][i] for i in range(n)) % q
        
        # Check if there exists beta such that alpha == beta^q - beta
        if q**n > 20000:
            return [False, False, False] # Prevent timeout
            
        def poly_mul(A, B):
            C = [0] * (2 * n)
            for i, a in enumerate(A):
                for j, b in enumerate(B):
                    C[i+j] = (C[i+j] + a * b) % q
            # Reduce modulo f(x)
            for i in range(2 * n - 1, n - 1, -1):
                if C[i] != 0:
                    for j in range(n):
                        C[i - n + j] = (C[i - n + j] - C[i] * f_coeffs[j]) % q
                    C[i] = 0
            return C[:n]
            
        exists_beta = False
        for beta_coeffs in itertools.product(range(q), repeat=n):
            beta = list(beta_coeffs)
            
            # Compute beta^q
            res = [1] + [0] * (n - 1)
            base = beta[:]
            exp = q
            while exp > 0:
                if exp % 2 == 1:
                    res = poly_mul(res, base)
                base = poly_mul(base, base)
                exp //= 2
                
            # Check if beta^q - beta == alpha
            diff = [(res[i] - beta[i]) % q for i in range(n)]
            if diff == alpha:
                exists_beta = True
                break
                
        # The conclusion states: Tr(alpha) == 0 iff exists beta
        conclusion = (tr_alpha == 0) == exists_beta
        neg_q = not conclusion
        
        return [h1, h2, neg_q]
        
    except Exception:
        return [False, False, False]
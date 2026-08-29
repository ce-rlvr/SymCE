import sympy as sp

x = sp.Symbol('x')

def poly_pow_mod(base, exp, mod_poly, domain, x):
    res = sp.Poly(1, x, domain=domain)
    base = base % mod_poly
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % mod_poly
        base = (base * base) % mod_poly
        exp //= 2
    return res

def rank_over_domain(matrix, domain):
    rows = len(matrix)
    if rows == 0:
        return 0
    cols = len(matrix[0])
    
    M = [[elem for elem in row] for row in matrix]
    
    rank = 0
    for c in range(cols):
        pivot = -1
        for r in range(rank, rows):
            if M[r][c] != domain.zero:
                pivot = r
                break
        if pivot != -1:
            M[rank], M[pivot] = M[pivot], M[rank]
            inv = domain.one / M[rank][c]
            for j in range(c, cols):
                M[rank][j] = M[rank][j] * inv
            for r in range(rows):
                if r != rank and M[r][c] != domain.zero:
                    factor = M[r][c]
                    for j in range(c, cols):
                        M[r][j] = M[r][j] - factor * M[rank][j]
            rank += 1
    return rank

def compute_min_poly_degree(alpha_poly, mod_poly, domain, n, x):
    vecs = []
    curr = sp.Poly(1, x, domain=domain)
    for m in range(n + 1):
        coeffs = curr.all_coeffs()
        coeffs = [domain.zero] * (n - len(coeffs)) + coeffs
        vecs.append(coeffs)
        
        if rank_over_domain(vecs, domain) < m + 1:
            return m
            
        curr = (curr * alpha_poly) % mod_poly
    return n

def conditions(witness):
    try:
        if isinstance(witness, dict):
            q = int(witness['q'])
            n = int(witness['n'])
            d = int(witness['d'])
            min_poly_coeffs = witness['min_poly']
            alpha_coeffs = witness['alpha']
            p = witness.get('p', None)
        else:
            q = int(witness.q)
            n = int(witness.n)
            d = int(witness.d)
            min_poly_coeffs = witness.min_poly
            alpha_coeffs = witness.alpha
            p = getattr(witness, 'p', None)
            
        if p is not None:
            domain = sp.GF(p)
        else:
            domain = sp.QQ
            
        min_poly = sp.Poly(min_poly_coeffs, x, domain=domain)
        alpha_poly = sp.Poly(alpha_coeffs, x, domain=domain)
        alpha_poly = alpha_poly % min_poly
        
        # H1: F_{q^n} is an extension field of degree n over F_q
        h1 = min_poly.is_irreducible and min_poly.degree() == n
        
        # H2: \alpha is an element of F_{q^n}
        h2 = True
        
        # H3: d is the smallest positive integer such that \alpha^{q^d} = \alpha
        h3 = False
        if d > 0:
            is_smallest = True
            for k in range(1, d):
                val = poly_pow_mod(alpha_poly, q**k, min_poly, domain, x)
                if val == alpha_poly:
                    is_smallest = False
                    break
            if is_smallest:
                val_d = poly_pow_mod(alpha_poly, q**d, min_poly, domain, x)
                if val_d == alpha_poly:
                    h3 = True
                    
        # Conclusion: The degree of the minimal polynomial of \alpha over F_q is equal to d
        deg_min_poly = compute_min_poly_degree(alpha_poly, min_poly, domain, n, x)
        neg_q = (deg_min_poly != d)
        
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: F_{q^n} is an extension field of degree n over F_q",
    "H_2: \\alpha is an element of F_{q^n}",
    "H_3: d is the smallest positive integer such that \\alpha^{q^d} = \\alpha",
    "¬Q: The degree of the minimal polynomial of \\alpha over F_q is not equal to d"
]

N_HYP = 3
NEG_Q_INDEX = 3
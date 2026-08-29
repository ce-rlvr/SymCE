import sympy as sp
import itertools

# Top-level setup: named object bindings
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def get_minpoly(M, x):
    if M.shape[0] == 0:
        return sp.Integer(1)
        
    if hasattr(M, 'minimal_polynomial'):
        try:
            res = M.minimal_polynomial(x)
            if res is not None:
                return res
        except Exception:
            pass
    if hasattr(M, 'minpoly'):
        try:
            res = M.minpoly(x)
            if res is not None:
                return res
        except Exception:
            pass

    # Fallback to computing from characteristic polynomial
    char_poly = M.charpoly(x).as_expr()
    factors = sp.factor_list(char_poly)[1]
    
    if not factors:
        return sp.Integer(1)
        
    bases = [f[0] for f in factors]
    max_exps = [f[1] for f in factors]
    
    best_poly = char_poly
    
    ranges = [range(1, e + 1) for e in max_exps]
    combinations = list(itertools.product(*ranges))
    # Sort by degree to find the minimal polynomial
    combinations.sort(key=lambda exps: sum(sp.degree(b, x) * e for b, e in zip(bases, exps)))
    
    for exps in combinations:
        poly_expr = sp.prod([b**e for b, e in zip(bases, exps)])
        poly = sp.Poly(poly_expr, x)
        coeffs = poly.all_coeffs()
        
        n = len(coeffs) - 1
        M_val = sp.zeros(M.shape[0], M.shape[1])
        M_pow = sp.eye(M.shape[0])
        for i in range(n, -1, -1):
            M_val += coeffs[i] * M_pow
            if i > 0:
                M_pow = M_pow * M
                
        is_zero = True
        for val in M_val:
            if val.is_zero:
                continue
            if sp.simplify(val) != 0:
                is_zero = False
                break
        if is_zero:
            best_poly = poly_expr
            break
            
    poly = sp.Poly(best_poly, x)
    LC = poly.LC()
    if LC == 0:
        return best_poly
    return sp.simplify(best_poly / LC)

def poly_lcm(p1, p2, x):
    lcm_expr = sp.lcm(p1, p2)
    poly = sp.Poly(lcm_expr, x)
    LC = poly.LC()
    if LC == 0:
        return lcm_expr
    return sp.simplify(lcm_expr / LC)

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        A, B = witness
        if not hasattr(A, 'shape'):
            A = sp.Matrix(A)
        if not hasattr(B, 'shape'):
            B = sp.Matrix(B)
    except Exception:
        return [False, False, False]
        
    # H_1: A is an n x n matrix and B is an m x m matrix over a field F
    try:
        h1 = hasattr(A, 'shape') and len(A.shape) == 2 and hasattr(B, 'shape') and len(B.shape) == 2
        if h1:
            h1 = (A.shape[0] == A.shape[1]) and (B.shape[0] == B.shape[1])
    except Exception:
        h1 = False
        
    # H_2: A \oplus B is the (n+m) x (n+m) block diagonal matrix with A and B on its main diagonal
    try:
        if h1:
            n = A.shape[0]
            m = B.shape[0]
            AB = sp.diag(A, B)
            h2 = (AB.shape == (n + m, n + m))
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: The minimal polynomial of A \oplus B is NOT the least common multiple of m_A(t) and m_B(t)
    try:
        if h1 and h2:
            x = sp.Dummy('t')
            mA = get_minpoly(A, x)
            mB = get_minpoly(B, x)
            mAB = get_minpoly(AB, x)
            
            lcm_AB = poly_lcm(mA, mB, x)
            
            diff = sp.expand(mAB - lcm_AB)
            neg_q = (diff != 0) and (diff.is_zero is not True)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix and B is an m x m matrix over a field F",
    "H_2: A \\oplus B is the (n+m) x (n+m) block diagonal matrix with A and B on its main diagonal",
    "¬Q: The minimal polynomial of A \\oplus B is NOT the least common multiple of m_A(t) and m_B(t)"
]

N_HYP = 2
NEG_Q_INDEX = 2
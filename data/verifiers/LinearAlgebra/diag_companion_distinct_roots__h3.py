import sympy
from sympy import Matrix, eye, zeros, Poly, gcd, diff
from sympy.abc import x

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # Extract p and C from witness
    p_expr = None
    C = None
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            p_expr, C = witness
        elif isinstance(witness, dict) and 'p' in witness and 'C' in witness:
            p_expr = witness['p']
            C = witness['C']
        else:
            C = sympy.Matrix(witness)
            p_expr = C.charpoly(x).as_expr()
    except Exception:
        return [False, False, False]

    # H_1: p(x) is a monic polynomial of degree n >= 1
    h1 = False
    gen = x
    try:
        if isinstance(p_expr, sympy.Poly):
            gen = p_expr.gen
            poly_p = p_expr
            p_expr = p_expr.as_expr()
        else:
            p_expr = sympy.sympify(p_expr)
            free_symbols = p_expr.free_symbols
            if len(free_symbols) == 1:
                gen = list(free_symbols)[0]
            poly_p = Poly(p_expr, gen)
        
        if poly_p.is_monic and poly_p.degree() >= 1:
            h1 = True
    except Exception:
        h1 = False

    # H_2: C is the n x n companion matrix of p(x)
    h2 = False
    try:
        if h1:
            C = sympy.Matrix(C)
            n = poly_p.degree()
            if C.shape == (n, n):
                coeffs = poly_p.all_coeffs()
                a = coeffs[1:]
                a_rev = list(reversed(a))
                
                C1 = sympy.zeros(n, n)
                for i in range(n-1): C1[i+1, i] = 1
                for i in range(n): C1[i, n-1] = -a_rev[i]
                    
                C2 = sympy.zeros(n, n)
                for i in range(n-1): C2[i, i+1] = 1
                for i in range(n): C2[n-1, i] = -a_rev[i]
                    
                C3 = sympy.zeros(n, n)
                for i in range(n-1): C3[i+1, i] = 1
                for i in range(n): C3[0, i] = -a[i]
                    
                C4 = sympy.zeros(n, n)
                for i in range(n-1): C4[i, i+1] = 1
                for i in range(n): C4[i, 0] = -a[i]
                    
                if C == C1 or C == C2 or C == C3 or C == C4:
                    h2 = True
    except Exception:
        h2 = False

    # ¬Q: C is not diagonalizable over the splitting field K
    # A companion matrix is diagonalizable over the splitting field iff 
    # its minimal polynomial (which is p(x)) has distinct roots.
    # Thus, it is NOT diagonalizable iff p(x) has repeated roots (gcd(p, p') != 1).
    neg_q = False
    try:
        if h1:
            p_diff = sympy.diff(p_expr, gen)
            g = sympy.gcd(p_expr, p_diff)
            poly_g = Poly(g, gen)
            if poly_g.degree() > 0:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p(x) is a monic polynomial of degree n >= 1",
    "H_2: C is the n x n companion matrix of p(x)",
    "¬Q: C is not diagonalizable over the splitting field K"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy as sp
from sympy.ntheory import factorint
import itertools

# Top-level setup
x, y = sp.symbols('x y')

def evaluate_points(q, M):
    f = factorint(q)
    p, k = list(f.items())[0]
    
    if k == 1:
        points = 0
        for x_val in range(p):
            for y_val in range(p):
                val = (M[0][0]*x_val*x_val + M[0][1]*x_val*y_val + M[0][2]*x_val +
                       M[1][0]*y_val*x_val + M[1][1]*y_val*y_val + M[1][2]*y_val +
                       M[2][0]*x_val + M[2][1]*y_val + M[2][2])
                if val % p == 0:
                    points += 1
        return points
    else:
        X = sp.Symbol('X')
        domain_str = 'GF(%d)' % p
        
        irr = None
        for coeffs in itertools.product(range(p), repeat=k):
            expr = X**k
            for i, c in enumerate(coeffs):
                expr += c * X**(k - 1 - i)
            poly = sp.Poly(expr, X, domain=domain_str)
            if poly.is_irreducible:
                irr = poly
                break
                
        elements = list(itertools.product(range(p), repeat=k))
        
        def to_poly(tup):
            expr = 0
            for i, c in enumerate(tup):
                expr += c * X**(k - 1 - i)
            return sp.Poly(expr, X, domain=domain_str)
            
        elements_poly = [to_poly(tup) for tup in elements]
        M_poly = [[sp.Poly(M[i][j], X, domain=domain_str) for j in range(3)] for i in range(3)]
        
        points = 0
        for px in elements_poly:
            for py in elements_poly:
                xx = (px * px).rem(irr)
                xy = (px * py).rem(irr)
                yy = (py * py).rem(irr)
                
                t1 = (M_poly[0][0] * xx).rem(irr)
                t2 = (M_poly[0][1] * xy).rem(irr)
                t3 = (M_poly[0][2] * px).rem(irr)
                t4 = (M_poly[1][0] * xy).rem(irr)
                t5 = (M_poly[1][1] * yy).rem(irr)
                t6 = (M_poly[1][2] * py).rem(irr)
                t7 = (M_poly[2][0] * px).rem(irr)
                t8 = (M_poly[2][1] * py).rem(irr)
                t9 = M_poly[2][2]
                
                res = t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8 + t9
                if res.is_zero:
                    points += 1
        return points

def conditions(witness):
    try:
        q, C_obj = witness
    except Exception:
        return [False, False, False]
        
    # H1: F is a finite field of odd order q
    try:
        if not isinstance(q, int) or q < 3 or q % 2 == 0:
            h1 = False
        else:
            f = factorint(q)
            h1 = len(f) == 1
    except Exception:
        h1 = False
        
    # H2: The conic C is non-degenerate (symmetric matrix, non-zero det)
    try:
        if not h1:
            h2 = False
            M_list = None
        else:
            f = factorint(q)
            p = list(f.keys())[0]
            
            M_list = None
            if isinstance(C_obj, (list, tuple)) and len(C_obj) == 3:
                if isinstance(C_obj[0], (list, tuple)) and len(C_obj[0]) == 3:
                    M_list = [list(row) for row in C_obj]
            if hasattr(C_obj, 'tolist'):
                M_list = C_obj.tolist()
                
            if M_list is None and isinstance(C_obj, sp.Expr):
                poly = sp.Poly(C_obj, x, y)
                M_list = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                inv2 = (p + 1) // 2
                for monom, coeff in poly.terms():
                    deg_x, deg_y = monom
                    if deg_x + deg_y > 2:
                        raise ValueError("Degree > 2")
                    c = int(coeff) % p
                    if deg_x == 2 and deg_y == 0:
                        M_list[0][0] = c
                    elif deg_x == 0 and deg_y == 2:
                        M_list[1][1] = c
                    elif deg_x == 1 and deg_y == 1:
                        M_list[0][1] = M_list[1][0] = (c * inv2) % p
                    elif deg_x == 1 and deg_y == 0:
                        M_list[0][2] = M_list[2][0] = (c * inv2) % p
                    elif deg_x == 0 and deg_y == 1:
                        M_list[1][2] = M_list[2][1] = (c * inv2) % p
                    elif deg_x == 0 and deg_y == 0:
                        M_list[2][2] = c
            
            if M_list is None or len(M_list) != 3 or any(len(row) != 3 for row in M_list):
                h2 = False
            else:
                for i in range(3):
                    for j in range(3):
                        M_list[i][j] = int(M_list[i][j]) % p
                        
                sym = True
                for i in range(3):
                    for j in range(3):
                        if M_list[i][j] != M_list[j][i]:
                            sym = False
                
                det = sp.Matrix(M_list).det()
                if sym and (det % p != 0):
                    h2 = True
                else:
                    h2 = False
    except Exception:
        h2 = False
        M_list = None
        
    # neg_Q: The number of F-rational points is NOT exactly q + 1
    try:
        if not h1 or not h2 or M_list is None:
            neg_q = False
        else:
            pts = evaluate_points(q, M_list)
            neg_q = (pts != q + 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finite field of odd order q",
    "H_2: The conic C is non-degenerate (symmetric matrix has non-zero determinant)",
    "¬Q: The number of F-rational points on the conic C is not exactly q + 1"
]

N_HYP = 2
NEG_Q_INDEX = 2
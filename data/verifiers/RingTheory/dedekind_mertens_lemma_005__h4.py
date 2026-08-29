import sympy
from sympy import Poly, Expr, groebner, Rational, Integer
from sympy.abc import x, a, b, c, d, y, z

# Top-level setup
def mul_ideals(A, B):
    return [i * j for i in A for j in B]

def pow_ideal(A, m):
    if m == 0:
        return [1]
    res = A
    for _ in range(m - 1):
        res = mul_ideals(res, A)
    return res

def ideals_equal(A, B, vars):
    A = [i for i in A if i != 0]
    B = [i for i in B if i != 0]
    
    if not A and not B: return True
    if not A or not B: return False
    
    if not vars:
        gcd_A = A[0]
        for a_elem in A[1:]:
            gcd_A = sympy.gcd(gcd_A, a_elem)
        gcd_B = B[0]
        for b_elem in B[1:]:
            gcd_B = sympy.gcd(gcd_B, b_elem)
        return abs(gcd_A) == abs(gcd_B)
        
    try:
        gb_A = groebner(A, *vars)
        for b_elem in B:
            if gb_A.reduce(b_elem)[1] != 0:
                return False
                
        gb_B = groebner(B, *vars)
        for a_elem in A:
            if gb_B.reduce(a_elem)[1] != 0:
                return False
                
        return True
    except Exception:
        return None

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                f, g, m = witness
            elif len(witness) == 2:
                f, g = witness
                m = 0
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        if isinstance(m, sympy.Integer):
            m = int(m)
        if not isinstance(m, int) or m < 0:
            return [False, False, False, False]
            
        f = sympy.sympify(f)
        g = sympy.sympify(g)
        if not isinstance(f, Expr) or not isinstance(g, Expr):
            return [False, False, False, False]
            
    except Exception:
        return [False, False, False, False]

    # H_1: R is a commutative ring
    h1 = True

    # H_2: f and g are non-zero polynomials
    try:
        vars_list = list((f.free_symbols | g.free_symbols) - {x})
        if vars_list:
            is_poly_f = f.is_polynomial(*(vars_list + [x]))
            is_poly_g = g.is_polynomial(*(vars_list + [x]))
        else:
            is_poly_f = f.is_polynomial(x)
            is_poly_g = g.is_polynomial(x)
            
        poly_f = Poly(f, x)
        poly_g = Poly(g, x)
        h2 = (is_poly_f == True) and (is_poly_g == True) and not poly_f.is_zero and not poly_g.is_zero
    except Exception:
        h2 = False

    # H_3: c(f) and c(g) are the content ideals of f and g in R
    h3 = True

    # neg_Q: c(f)^{m+1} c(g) != c(f)^m c(fg)
    try:
        cf = poly_f.coeffs()
        cg = poly_g.coeffs()
        cfg = Poly((f * g).expand(), x).coeffs()
        
        lhs = mul_ideals(pow_ideal(cf, m + 1), cg)
        rhs = mul_ideals(pow_ideal(cf, m), cfg)
        
        eq = ideals_equal(lhs, rhs, vars_list)
        if eq is None:
            neg_q = False
        else:
            neg_q = not eq
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: f and g are non-zero polynomials",
    "H_3: c(f) and c(g) are the content ideals of f and g in R",
    "¬Q: c(f)**(m+1) c(g) != c(f)**m c(fg)"
]

N_HYP = 3
NEG_Q_INDEX = 3
import sympy

x, y, z = sympy.symbols('x y z')

CONDITION_LABELS = [
    "H_1: F is a finite field of odd order q",
    "H_2: C is a projective conic curve defined by a homogeneous polynomial of degree 2 in three variables over F",
    "¬Q: The number of F-rational points on the conic C is not exactly q + 1"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        q, poly = witness
    except Exception:
        return [False, False, False]
    
    # H_1: F is a finite field of odd order q
    # We restrict to prime fields for simplicity and require q < 1000 to ensure fast evaluation.
    try:
        h1 = isinstance(q, int) and q % 2 == 1 and sympy.isprime(q) and q < 1000
    except Exception:
        h1 = False
        
    # H_2: C is a projective conic curve defined by a homogeneous polynomial of degree 2 in three variables over F
    try:
        if h1:
            p_mod = sympy.Poly(poly, x, y, z, modulus=q)
            if p_mod.is_zero:
                h2 = False
            else:
                # Check if every term in the polynomial mod q has a total degree of exactly 2
                h2 = all(sum(monom) == 2 for monom, coeff in p_mod.terms())
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: The number of F-rational points on the conic C is NOT exactly q + 1
    try:
        if h1 and h2:
            coeffs = p_mod.terms()
            
            def eval_pt(xv, yv, zv):
                val = 0
                for monom, c in coeffs:
                    dx, dy, dz = monom
                    val = (val + int(c) * (xv**dx) * (yv**dy) * (zv**dz)) % q
                return val == 0

            count = 0
            
            # Points of the form (x, y, 1)
            for i in range(q):
                for j in range(q):
                    if eval_pt(i, j, 1): 
                        count += 1
                        
            # Points of the form (x, 1, 0)
            for i in range(q):
                if eval_pt(i, 1, 0): 
                    count += 1
                    
            # Point (1, 0, 0)
            if eval_pt(1, 0, 0): 
                count += 1
            
            neg_q = (count != q + 1)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]
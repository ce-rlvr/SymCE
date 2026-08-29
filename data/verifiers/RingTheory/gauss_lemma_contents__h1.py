import math
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard algebraic objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def add(x, y):
    return (x[0] + y[0], x[1] + y[1])

def mul(x, y, D):
    return (x[0]*y[0] - D * x[1]*y[1], x[0]*y[1] + x[1]*y[0])

def norm(x, D):
    return x[0]**2 + D * x[1]**2

def divides(y, x, D):
    Ny = norm(y, D)
    if Ny == 0:
        return x == (0, 0)
    a, b = x
    c, d = y
    return (a*c + D * b*d) % Ny == 0 and (b*c - a*d) % Ny == 0

def get_divisors(x, D):
    Nx = norm(x, D)
    if Nx == 0:
        return set()
    divs = set()
    max_c = int(math.isqrt(Nx)) + 1
    max_d = int(math.isqrt(Nx // D)) + 1
    for c in range(-max_c, max_c + 1):
        for d in range(-max_d, max_d + 1):
            y = (c, d)
            Ny = norm(y, D)
            if Ny > 0 and Nx % Ny == 0:
                if divides(y, x, D):
                    divs.add(y)
    return divs

def get_common_divisors(coeffs, D):
    coeffs = [c for c in coeffs if c != (0, 0)]
    if not coeffs:
        return set()
    common = get_divisors(coeffs[0], D)
    for c in coeffs[1:]:
        common = common.intersection(get_divisors(c, D))
    return common

def get_gcds(coeffs, D):
    common = get_common_divisors(coeffs, D)
    gcds = set()
    for d in common:
        if all(divides(c, d, D) for c in common):
            gcds.add(d)
    return gcds

def poly_mul(f, g, D):
    deg_f = len(f) - 1
    deg_g = len(g) - 1
    res = [(0, 0)] * (deg_f + deg_g + 1)
    for i in range(len(f)):
        for j in range(len(g)):
            term = mul(f[i], g[j], D)
            res[i+j] = add(res[i+j], term)
    return res

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to Gauss's Lemma for Polynomial Contents.
    The witness is expected to be a dictionary specifying an imaginary quadratic 
    ring Z[sqrt(-D)] and two polynomials f and g.
    
    Format:
    {
        "D": int (positive, e.g., 5 for Z[sqrt(-5)]),
        "f": [(a0, b0), (a1, b1), ...], # coefficients a + b*sqrt(-D)
        "g": [(c0, d0), (c1, d1), ...]
    }
    """
    try:
        if not isinstance(witness, dict):
            return [False, False]
        
        D = witness.get('D')
        f = witness.get('f')
        g = witness.get('g')
        
        if not (isinstance(D, int) and D > 0):
            return [False, False]
            
        if not (isinstance(f, list) and isinstance(g, list)):
            return [False, False]
            
        def is_valid_poly(poly):
            return all(isinstance(c, tuple) and len(c) == 2 and 
                       isinstance(c[0], int) and isinstance(c[1], int) for c in poly)
                       
        if not (is_valid_poly(f) and is_valid_poly(g)):
            return [False, False]
            
        def is_nonzero(poly):
            return any(c != (0, 0) for c in poly)
            
        # Hypothesis 1: f and g are non-zero polynomials
        h1 = is_nonzero(f) and is_nonzero(g)
        
        # Conclusion: The content of fg is associate to the product of the contents of f and g
        neg_q = False
        try:
            gcds_f = get_gcds(f, D)
            gcds_g = get_gcds(g, D)
            
            # If contents don't exist, the conclusion is undefined (hence fails to hold)
            if not gcds_f or not gcds_g:
                neg_q = True
            else:
                fg = poly_mul(f, g, D)
                gcds_fg = get_gcds(fg, D)
                
                if not gcds_fg:
                    neg_q = True
                else:
                    c_f = next(iter(gcds_f))
                    c_g = next(iter(gcds_g))
                    c_fg = next(iter(gcds_fg))
                    
                    prod = mul(c_f, c_g, D)
                    
                    # Check if prod and c_fg are associate
                    are_associate = divides(prod, c_fg, D) and divides(c_fg, prod, D)
                    neg_q = not are_associate
        except Exception:
            neg_q = False
            
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: f and g are non-zero polynomials",
    "¬Q: The content of the product fg is not associate to the product of the contents of f and g"
]

N_HYP = 1
NEG_Q_INDEX = 1
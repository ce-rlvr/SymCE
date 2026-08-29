import sympy
import math
import itertools
from sympy.abc import x, y, z, t

def my_log(v):
    if v <= 1e-100:
        return -230.0
    return math.log(v)

def gaussian_integral(expr, syms, limit=8, pts=200):
    n = len(syms)
    if n == 0:
        try:
            val = float(expr)
            if math.isnan(val):
                return float('nan')
            return val
        except Exception:
            return float('nan')
            
    step = 2 * limit / pts
    grid_1d = [-limit + (i + 0.5) * step for i in range(pts)]
    
    try:
        f_num = sympy.lambdify(syms, expr, modules=[{'log': my_log}, 'math'])
    except Exception:
        return float('nan')
        
    total = 0.0
    for pt in itertools.product(grid_1d, repeat=n):
        try:
            val = float(f_num(*pt))
            if math.isnan(val):
                return float('nan')
            weight = math.exp(-sum(v*v for v in pt)/2) / (math.sqrt(2*math.pi)**n)
            total += val * weight
        except Exception:
            return float('nan')
            
    return total * (step**n)

def get_integral(expr, syms, scale=1.0):
    n = len(syms)
    if n == 1:
        limit = 8 * scale
        pts = int(200 * scale)
    elif n == 2:
        limit = 6 * scale
        pts = int(40 * scale)
    else:
        limit = 5 * scale
        pts = int(12 * scale)
    return gaussian_integral(expr, syms, limit, pts)

def is_in_L2(expr, syms):
    int1 = get_integral(expr, syms, scale=1.0)
    int2 = get_integral(expr, syms, scale=1.5)
    
    if math.isnan(int1) or math.isnan(int2):
        return False
        
    if int2 > int1 * 1.4 + 1e-2:
        return False
        
    return True

def check_H1(witness):
    if not isinstance(witness, sympy.Expr) and not isinstance(witness, (int, float)):
        return False
    try:
        f = sympy.sympify(witness)
        syms = list(f.free_symbols)
        for s in syms:
            sympy.diff(f, s)
        return True
    except Exception:
        return False

def check_H2(witness):
    try:
        f = sympy.sympify(witness)
        syms = list(f.free_symbols)
        
        if not is_in_L2(f**2, syms):
            return False
            
        grad_sq = sympy.S(0)
        for s in syms:
            grad_sq += sympy.diff(f, s)**2
            
        if not is_in_L2(grad_sq, syms):
            return False
            
        return True
    except Exception:
        return False

def check_neg_Q(witness):
    try:
        f = sympy.sympify(witness)
        syms = list(f.free_symbols)
        
        norm_sq = get_integral(f**2, syms, scale=1.0)
        if math.isnan(norm_sq):
            return True
            
        if norm_sq == 0.0:
            return True
            
        lhs_expr = f**2 * sympy.log(f**2 / norm_sq)
        lhs_val = get_integral(lhs_expr, syms, scale=1.0)
        
        if math.isnan(lhs_val):
            return True
            
        grad_sq = sympy.S(0)
        for s in syms:
            grad_sq += sympy.diff(f, s)**2
            
        rhs_val = 2 * get_integral(grad_sq, syms, scale=1.0)
        
        if math.isnan(rhs_val):
            return True
            
        if lhs_val > rhs_val + 1e-5:
            return True
            
        return False
    except Exception:
        return True

def conditions(witness):
    return [check_H1(witness), check_H2(witness), check_neg_Q(witness)]

CONDITION_LABELS = [
    "H_1: f is a weakly differentiable function",
    "H_2: f and its weak gradient are in L^2(gamma)",
    "¬Q: The Gaussian Logarithmic Sobolev Inequality fails"
]

N_HYP = 2
NEG_Q_INDEX = 2
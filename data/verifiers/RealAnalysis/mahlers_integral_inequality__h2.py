import sympy
from sympy.abc import x
import math

def complex_log(z):
    if abs(z) == 0:
        return complex(-float('inf'), 0)
    return complex(math.log(abs(z)), math.atan2(z.imag, z.real))

def complex_exp(z):
    try:
        r = math.exp(z.real)
        return complex(r * math.cos(z.imag), r * math.sin(z.imag))
    except OverflowError:
        return complex(float('inf'), 0)

def eval_exp_int_log(expr, a, b, n=2000):
    try:
        expr = sympy.sympify(expr)
        free_syms = list(expr.free_symbols)
        
        if not free_syms:
            val = complex(expr.evalf())
            if abs(val) < 1e-15:
                val = complex(1e-15, 0)
            return val
            
        sym = free_syms[0]
        
        f_num = sympy.lambdify(sym, expr, modules=['math'])
        dx = (b - a) / n
        integral_val = 0j
        for i in range(n):
            xi = a + (i + 0.5) * dx
            val = complex(f_num(xi))
            if abs(val) < 1e-15:
                val = complex(1e-15, 0)
            integral_val += complex_log(val)
        integral_val *= dx
        integral_val /= (b - a)
        return complex_exp(integral_val)
    except Exception:
        try:
            expr = sympy.sympify(expr)
            free_syms = list(expr.free_symbols)
            
            dx = (b - a) / n
            integral_val = 0j
            for i in range(n):
                xi = a + (i + 0.5) * dx
                subs_dict = {s: xi for s in free_syms}
                val = complex(expr.subs(subs_dict).evalf())
                if abs(val) < 1e-15:
                    val = complex(1e-15, 0)
                integral_val += complex_log(val)
            integral_val *= dx
            integral_val /= (b - a)
            return complex_exp(integral_val)
        except Exception:
            return None

def check_H1(a, b):
    try:
        a_val = float(sympy.N(a))
        b_val = float(sympy.N(b))
        return a_val < b_val
    except Exception:
        return False

def check_H2(g, a, b, n=1000):
    try:
        a_val = float(sympy.N(a))
        b_val = float(sympy.N(b))
        if a_val >= b_val:
            return False
        
        g = sympy.sympify(g)
        free_syms = list(g.free_symbols)
        
        if not free_syms:
            val = float(sympy.N(g))
            return val > 0 and not math.isinf(val) and not math.isnan(val)
            
        sym = free_syms[0]
        
        try:
            g_num = sympy.lambdify(sym, g, modules=['math'])
            dx = (b_val - a_val) / n
            for i in range(n + 1):
                xi = a_val + i * dx
                val = float(g_num(xi))
                if val <= 0 or math.isinf(val) or math.isnan(val):
                    return False
            return True
        except Exception:
            dx = (b_val - a_val) / n
            for i in range(n + 1):
                xi = a_val + i * dx
                subs_dict = {s: xi for s in free_syms}
                val = float(sympy.N(g.subs(subs_dict)))
                if val <= 0 or math.isinf(val) or math.isnan(val):
                    return False
            return True
    except Exception:
        return False

def check_neg_Q(a, b, f, g):
    try:
        a_val = float(sympy.N(a))
        b_val = float(sympy.N(b))
        
        LHS_c = eval_exp_int_log(f + g, a_val, b_val)
        RHS_f = eval_exp_int_log(f, a_val, b_val)
        RHS_g = eval_exp_int_log(g, a_val, b_val)
        
        if LHS_c is None or RHS_f is None or RHS_g is None:
            return False
            
        RHS_c = RHS_f + RHS_g
        
        if abs(LHS_c.imag) > 1e-5 or abs(RHS_c.imag) > 1e-5:
            return True
            
        LHS_real = LHS_c.real
        RHS_real = RHS_c.real
        
        return LHS_real < RHS_real - 1e-7
    except Exception:
        return False

def conditions(witness):
    if not isinstance(witness, (tuple, list)) or len(witness) != 4:
        return [False, False, False]
    
    a, b, f, g = witness
    
    h1 = check_H1(a, b)
    h2 = check_H2(g, a, b)
    neg_q = check_neg_Q(a, b, f, g)
    
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are real numbers with a < b",
    "H_2: g is a strictly positive continuous function on the interval a to b",
    "not Q: Mahler inequality fails for f and g"
]

N_HYP = 2
NEG_Q_INDEX = 2
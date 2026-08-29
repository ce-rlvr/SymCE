import sympy
import math
import itertools
import functools
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: (x_n) converges to x in the norm topology",
    "H_2: (y_n) converges to y in the norm topology",
    "¬Q: <x_n, y_n> does not converge to <x, y>"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    n = sympy.Symbol('n', integer=True, positive=True)
    
    h1, h2, neg_q = False, False, False
    
    try:
        norm_x = None
        norm_y = None
        ip_n = None
        ip_limit = None
        
        if isinstance(witness, tuple) and len(witness) == 4:
            norm_x, norm_y, ip_n, ip_limit = witness
        elif isinstance(witness, dict):
            if 'norm_x_n_minus_x' in witness:
                norm_x = witness.get('norm_x_n_minus_x')
                norm_y = witness.get('norm_y_n_minus_y')
                ip_n = witness.get('inner_product_x_n_y_n')
                ip_limit = witness.get('inner_product_x_y')
            elif 'x_n' in witness:
                x_n = witness['x_n']
                x = witness['x']
                y_n = witness['y_n']
                y = witness['y']
                norm = witness['norm']
                ip = witness['inner_product']
                
                x_n_val = x_n(n) if callable(x_n) else x_n
                y_n_val = y_n(n) if callable(y_n) else y_n
                x_val = x() if callable(x) else x
                y_val = y() if callable(y) else y
                
                norm_x = norm(x_n_val - x_val)
                norm_y = norm(y_n_val - y_val)
                ip_n = ip(x_n_val, y_n_val)
                ip_limit = ip(x_val, y_val)
        else:
            norm_x = getattr(witness, 'norm_x_n_minus_x', None)
            norm_y = getattr(witness, 'norm_y_n_minus_y', None)
            ip_n = getattr(witness, 'inner_product_x_n_y_n', None)
            ip_limit = getattr(witness, 'inner_product_x_y', None)
            
        if callable(norm_x): norm_x = norm_x(n)
        if callable(norm_y): norm_y = norm_y(n)
        if callable(ip_n): ip_n = ip_n(n)
        if callable(ip_limit): ip_limit = ip_limit()
        
        if norm_x is not None:
            try:
                lim_x = sympy.limit(norm_x, n, sympy.oo)
                h1 = (sympy.simplify(lim_x) == 0)
            except Exception:
                h1 = False
                
        if norm_y is not None:
            try:
                lim_y = sympy.limit(norm_y, n, sympy.oo)
                h2 = (sympy.simplify(lim_y) == 0)
            except Exception:
                h2 = False
                
        if ip_n is not None and ip_limit is not None:
            try:
                lim_ip = sympy.limit(ip_n, n, sympy.oo)
                diff = sympy.simplify(lim_ip - ip_limit)
                neg_q = (diff != 0)
            except Exception:
                neg_q = True
                
    except Exception:
        pass
        
    return [bool(h1), bool(h2), bool(neg_q)]
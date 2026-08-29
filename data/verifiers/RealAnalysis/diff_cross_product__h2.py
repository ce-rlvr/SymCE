import sympy as sp
from sympy import Matrix, eye, zeros
import math
import itertools
import functools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        vars = witness.get('vars')
        f = witness.get('f')
        g = witness.get('g')
        a = witness.get('a')
        
        if vars is None or f is None or g is None or a is None:
            return [False, False, False]
            
        if not isinstance(f, Matrix) or f.shape != (3, 1):
            return [False, False, False]
        if not isinstance(g, Matrix) or g.shape != (3, 1):
            return [False, False, False]
        if len(vars) < 1 or len(vars) != len(a):
            return [False, False, False]
            
        subs_dict = dict(zip(vars, a))
        
        def is_valid_real(val):
            if val.has(sp.nan) or val.has(sp.zoo) or val.has(sp.oo) or val.has(-sp.oo) or val.has(sp.I):
                return False
            if val.is_real is False:
                return False
            return True

        # H1: U is an open subset of R^n
        # We assume U is R^n or an open neighborhood of a where the functions are defined.
        h1 = True
        
        # H2: g is differentiable at a
        Jg = g.jacobian(vars)
        Jg_a = Jg.subs(subs_dict)
        h2 = True
        for val in Jg_a:
            if not is_valid_real(val):
                h2 = False
                break
                
        g_a = g.subs(subs_dict)
        for val in g_a:
            if not is_valid_real(val):
                h2 = False
                break
                
        # Conclusion: h is differentiable at a, and Dh(a)(v) = Df(a)(v) x g(a) + f(a) x Dg(a)(v)
        h_func = f.cross(g)
        Jh = h_func.jacobian(vars)
        Jh_a = Jh.subs(subs_dict)
        
        h_diff = True
        for val in Jh_a:
            if not is_valid_real(val):
                h_diff = False
                break
                
        Jf = f.jacobian(vars)
        Jf_a = Jf.subs(subs_dict)
        f_diff = True
        for val in Jf_a:
            if not is_valid_real(val):
                f_diff = False
                break
                
        f_a = f.subs(subs_dict)
        for val in f_a:
            if not is_valid_real(val):
                f_diff = False
                break
        
        neg_q = False
        if not h_diff:
            neg_q = True
        elif not f_diff:
            # If f is not differentiable, the formula involving Df(a) is invalid
            neg_q = True
        else:
            formula_holds = True
            for i in range(len(vars)):
                col_Dh = Jh_a[:, i]
                col_Df = Jf_a[:, i]
                col_Dg = Jg_a[:, i]
                
                expected_col = col_Df.cross(g_a) + f_a.cross(col_Dg)
                
                for j in range(3):
                    diff = sp.simplify(col_Dh[j] - expected_col[j])
                    if diff != 0:
                        formula_holds = False
                        break
                if not formula_holds:
                    break
            
            if not formula_holds:
                neg_q = True
                
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: U is an open subset of R^n",
    "H_2: g is differentiable at a",
    "¬Q: The cross product function h(x) = f(x) x g(x) is not differentiable at a, or its derivative formula fails"
]

N_HYP = 2
NEG_Q_INDEX = 2
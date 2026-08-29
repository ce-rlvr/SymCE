import sympy as sp
from sympy.calculus.util import continuous_domain

# Top-level setup: named object bindings that the witness expression may reference
x, t = sp.symbols('x t', real=True)

def is_continuous_2d(f, a, b, c, d):
    try:
        a_sym, b_sym = sp.sympify(a), sp.sympify(b)
        c_sym, d_sym = sp.sympify(c), sp.sympify(d)
        
        if float(a_sym) >= float(b_sym) or float(c_sym) >= float(d_sym):
            return False
            
        # 1D continuity checks
        for j in range(5):
            tv = c_sym + (d_sym - c_sym) * sp.Rational(j, 4)
            fx = f.subs(t, tv)
            dom_x = continuous_domain(fx, x, sp.Interval(a_sym, b_sym))
            if sp.Interval(a_sym, b_sym).is_subset(dom_x) != True:
                return False
                
        for i in range(5):
            xv = a_sym + (b_sym - a_sym) * sp.Rational(i, 4)
            ft = f.subs(x, xv)
            dom_t = continuous_domain(ft, t, sp.Interval(c_sym, d_sym))
            if sp.Interval(c_sym, d_sym).is_subset(dom_t) != True:
                return False
                
        # 2D grid check for joint continuity and jump discontinuities
        n_grid = 10
        for i in range(n_grid + 1):
            for j in range(n_grid + 1):
                xv = float(a_sym + (b_sym - a_sym) * i / float(n_grid))
                tv = float(c_sym + (d_sym - c_sym) * j / float(n_grid))
                
                val = float(f.subs({x: xv, t: tv}).evalf())
                
                hx = 1e-5
                ht = 1e-5
                xv_near = min(float(b_sym), xv + hx)
                tv_near = min(float(d_sym), tv + ht)
                
                val_near = float(f.subs({x: xv_near, t: tv_near}).evalf())
                if abs(val - val_near) > 1e-1:
                    return False
                    
        return True
    except Exception:
        return False

def conclusion_fails(f, a, b, c, d):
    try:
        a_sym, b_sym = sp.sympify(a), sp.sympify(b)
        c_sym, d_sym = sp.sympify(c), sp.sympify(d)
        
        F = sp.integrate(f, (t, c_sym, d_sym))
        if not F.has(sp.Integral):
            dF = F.diff(x)
            try:
                dom = continuous_domain(dF, x, sp.Interval.open(a_sym, b_sym))
                if sp.Interval.open(a_sym, b_sym).is_subset(dom) == False:
                    return True # Differentiability fails
            except Exception:
                pass
            
            dfdx = f.diff(x)
            int_dfdx = sp.integrate(dfdx, (t, c_sym, d_sym))
            if not int_dfdx.has(sp.Integral):
                if sp.simplify(dF - int_dfdx) == 0:
                    return False
                
                for i in range(1, 10):
                    xv = float(a_sym + (b_sym - a_sym) * i / 10.0)
                    val1 = float(dF.subs(x, xv).evalf())
                    val2 = float(int_dfdx.subs(x, xv).evalf())
                    if abs(val1 - val2) > 1e-5:
                        return True
                return False
            
        # Numerical fallback using midpoint rule
        dfdx = f.diff(x)
        for i in range(1, 10):
            xv = float(a_sym + (b_sym - a_sym) * i / 10.0)
            
            h = 1e-5
            def eval_f(xv_val, tv_val):
                return float(f.subs({x: xv_val, t: tv_val}).evalf())
            
            n = 50
            dt = float(d_sym - c_sym) / n
            c_fl = float(c_sym)
            
            I_plus = 0.0
            I_minus = 0.0
            for j in range(n):
                tv = c_fl + (j + 0.5) * dt
                I_plus += eval_f(xv + h, tv)
                I_minus += eval_f(xv - h, tv)
            I_plus *= dt
            I_minus *= dt
            
            num_dF = (I_plus - I_minus) / (2 * h)
            
            def eval_dfdx(tv_val):
                return float(dfdx.subs({x: xv, t: tv_val}).evalf())
            
            try:
                num_int_dfdx = 0.0
                for j in range(n):
                    tv = c_fl + (j + 0.5) * dt
                    num_int_dfdx += eval_dfdx(tv)
                num_int_dfdx *= dt
            except Exception:
                return True # If partial derivative is not integrable, conclusion fails
                
            if abs(num_dF - num_int_dfdx) > 1e-2:
                return True
                
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            a = witness.get('a')
            b = witness.get('b')
            c = witness.get('c')
            d = witness.get('d')
        else:
            f, a, b, c, d = witness
            
        if callable(f):
            f = f(x, t)
        elif isinstance(f, str):
            f = sp.sympify(f, locals={'x': x, 't': t})
        else:
            f = sp.sympify(f)
            
        h1 = is_continuous_2d(f, a, b, c, d)
        neg_q = conclusion_fails(f, a, b, c, d)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = ["H_1: f is continuous on the given domain", "¬Q: F is not differentiable or derivative does not match integral of df/dx"]
N_HYP = 1
NEG_Q_INDEX = 1
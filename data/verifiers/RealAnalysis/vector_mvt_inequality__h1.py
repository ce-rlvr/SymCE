import sympy
import math

# Top-level setup
t = sympy.Symbol('t', real=True)

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def get_transition_points(expr):
    points = set()
    if hasattr(expr, 'args'):
        for arg in expr.args:
            points.update(get_transition_points(arg))
            
    if isinstance(expr, (sympy.Eq, sympy.Ne, sympy.Gt, sympy.Lt, sympy.Ge, sympy.Le)):
        try:
            roots = sympy.solve(expr.lhs - expr.rhs, t)
            if isinstance(roots, list):
                for r in roots:
                    if hasattr(r, 'is_real') and r.is_real:
                        points.add(float(r))
                    elif getattr(r, 'is_real', None) is None:
                        try:
                            points.add(float(r))
                        except Exception:
                            pass
        except Exception:
            pass
    elif isinstance(expr, sympy.Abs):
        try:
            roots = sympy.solve(expr.args[0], t)
            if isinstance(roots, list):
                for r in roots:
                    if hasattr(r, 'is_real') and r.is_real:
                        points.add(float(r))
                    elif getattr(r, 'is_real', None) is None:
                        try:
                            points.add(float(r))
                        except Exception:
                            pass
        except Exception:
            pass
    return points

def check_H1(witness):
    try:
        f, a, b = witness
        a = float(a)
        b = float(b)
        if a >= b:
            return False
            
        if not isinstance(f, sympy.Matrix):
            return False
            
        if f.shape[0] != 1 and f.shape[1] != 1:
            return False
            
        # Check for transition points in (a, b)
        trans_points = set()
        for j in range(len(f)):
            trans_points.update(get_transition_points(f[j]))
                
        for c in trans_points:
            if a < c < b:
                # Check if differentiable at c
                eps_diff = 1e-6
                for j in range(len(f)):
                    f_expr = f[j]
                    f_c = complex(f_expr.subs(t, c).evalf()).real
                    f_c_plus = complex(f_expr.subs(t, c + eps_diff).evalf()).real
                    f_c_minus = complex(f_expr.subs(t, c - eps_diff).evalf()).real
                    der_plus = (f_c_plus - f_c) / eps_diff
                    der_minus = (f_c - f_c_minus) / eps_diff
                    if abs(der_plus - der_minus) > 1e-2 * max(1, abs(der_plus)):
                        return False
                        
        # Also check the integral of derivative to catch any other jumps or kinks
        eps = (b - a) * 1e-4
        a_inner = a + eps
        b_inner = b - eps
        
        df = f.diff(t)
        
        # Simpson's 1/3 rule
        n_points = 500 # must be even
        dt = (b_inner - a_inner) / n_points
        
        integral_val = [0.0] * len(f)
        
        for i in range(n_points + 1):
            c = a_inner + i * dt
            df_c = df.subs(t, c)
            weight = 1.0 if (i == 0 or i == n_points) else (4.0 if i % 2 == 1 else 2.0)
            for j in range(len(f)):
                val = complex(df_c[j].evalf())
                if abs(val.imag) > 1e-7 or math.isnan(val.real) or math.isinf(val.real):
                    return False
                integral_val[j] += weight * val.real
                
        for j in range(len(f)):
            integral_val[j] *= dt / 3.0
                
        f_b_inner = f.subs(t, b_inner)
        f_a_inner = f.subs(t, a_inner)
        diff_val = f_b_inner - f_a_inner
        
        for j in range(len(f)):
            val = complex(diff_val[j].evalf()).real
            if abs(val - integral_val[j]) > 1e-4 * max(1, abs(val)):
                return False
                
        return True
    except Exception:
        return False

def check_neg_Q(witness):
    try:
        f, a, b = witness
        a = float(a)
        b = float(b)
        if a >= b:
            return False
            
        f_a = f.subs(t, a)
        f_b = f.subs(t, b)
        
        diff_vec = f_b - f_a
        LHS = complex(diff_vec.norm().evalf()).real
        
        if math.isnan(LHS) or math.isinf(LHS):
            return False
            
        df = f.diff(t)
        
        n_points = 500
        dt = (b - a) / (n_points + 1)
        
        for i in range(1, n_points + 1):
            c = a + i * dt
            df_c = df.subs(t, c)
            RHS = complex(df_c.norm().evalf()).real * (b - a)
            
            if math.isnan(RHS) or math.isinf(RHS):
                return False
                
            if LHS <= RHS + 1e-7:
                return False
                
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 3:
            return [False, False]
    except Exception:
        return [False, False]
        
    h1 = check_H1(witness)
    neg_q = check_neg_Q(witness)
    return [h1, neg_q]

CONDITION_LABELS: list[str] = [
    "H_1: f is differentiable on (a, b)",
    "¬Q: For all c in (a, b), ||f(b) - f(a)|| > ||f'(c)|| (b - a)"
]

N_HYP: int = 1
NEG_Q_INDEX: int = 1
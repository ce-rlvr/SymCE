import sympy as sp
import math

# Top-level setup for witness expressions
x, y, z = sp.symbols('x y z')
t = sp.Symbol('t', real=True)

def check_H1(witness):
    """
    Check if the witness provides valid dimensions and real points a, b.
    This serves as a proxy for U being an open set in R^n containing a and b.
    """
    try:
        f, vars, a, b = witness
        if not isinstance(vars, (list, tuple)):
            return False
        if not isinstance(a, (list, tuple)) or not isinstance(b, (list, tuple)):
            return False
        if len(vars) != len(a) or len(vars) != len(b):
            return False
        for pt in (a, b):
            for coord in pt:
                if not isinstance(coord, (int, float, sp.Basic, str)):
                    return False
                if not sp.sympify(coord).is_real:
                    return False
        return True
    except Exception:
        return False

def check_H2(witness):
    """
    Check if the line segment connecting a and b is contained in U.
    We verify this by checking if f is defined and real-valued at 101 points along the segment.
    """
    try:
        f, vars, a, b = witness
        c = [sp.sympify(a[i]) + t * (sp.sympify(b[i]) - sp.sympify(a[i])) for i in range(len(vars))]
        
        if isinstance(f, (list, tuple, sp.Matrix)):
            f_list = list(f)
        else:
            f_list = [f]
            
        for t_val in [i / 100.0 for i in range(101)]:
            for expr in f_list:
                val = sp.sympify(expr).subs(zip(vars, [cv.subs(t, t_val) for cv in c]))
                val_c = complex(val)
                if math.isnan(val_c.real) or math.isinf(val_c.real):
                    return False
                if abs(val_c.imag) > 1e-9:
                    return False
        return True
    except Exception:
        return False

def check_neg_Q(witness):
    """
    Check if the conclusion FAILS.
    The conclusion is: There exists c in (a, b) such that f(b) - f(a) = \nabla f(c) \cdot (b - a).
    We return True if NO such c exists.
    """
    try:
        f, vars, a, b = witness
        
        # If a and b are the same point, the open segment is empty, so no such c exists.
        is_same = True
        for i in range(len(vars)):
            val_a = float(sp.sympify(a[i]))
            val_b = float(sp.sympify(b[i]))
            if abs(val_a - val_b) > 1e-9:
                is_same = False
                break
        if is_same:
            return True
            
        c = [sp.sympify(a[i]) + t * (sp.sympify(b[i]) - sp.sympify(a[i])) for i in range(len(vars))]
        
        if isinstance(f, (list, tuple, sp.Matrix)):
            f_list = list(f)
        else:
            f_list = [f]
            
        targets = []
        for expr in f_list:
            val_b = sp.sympify(expr).subs(zip(vars, b))
            val_a = sp.sympify(expr).subs(zip(vars, a))
            targets.append(val_b - val_a)
            
        g_list = []
        for expr in f_list:
            expr = sp.sympify(expr)
            g = 0
            for i, v in enumerate(vars):
                df_dv = sp.diff(expr, v)
                df_dv_c = df_dv.subs(zip(vars, c))
                g += df_dv_c * (sp.sympify(b[i]) - sp.sympify(a[i]))
            g_list.append(g)
            
        equations = [g_list[i] - targets[i] for i in range(len(f_list))]
        
        try:
            sols = sp.solve(equations, t, dict=True)
        except Exception:
            sols = []
            
        if isinstance(sols, list):
            if len(sols) == 1 and not sols[0]:
                # Identity equation (e.g. 0 = 0), all t are solutions
                return False
            for sol in sols:
                if t in sol:
                    val = sol[t]
                    try:
                        val_c = complex(val)
                        if abs(val_c.imag) < 1e-9:
                            val_f = val_c.real
                            if 0 < val_f < 1:
                                # Found a valid c in the open segment (0, 1)
                                return False
                    except Exception:
                        pass
            # No solution found in (0, 1)
            return True
        else:
            # If solve returns a ConditionSet or something else, we assume no simple solution exists
            return True
    except Exception:
        return False

def conditions(witness):
    return [check_H1(witness), check_H2(witness), check_neg_Q(witness)]

CONDITION_LABELS = [
    "H_1: U is an open set in R^n (witness provides valid dimensions and real points)",
    "H_2: The line segment connecting a and b is contained in U (f is defined and real on the segment)",
    "¬Q: There is no point c on the open segment such that f(b) - f(a) = \\nabla f(c) \\cdot (b - a)"
]

N_HYP = 2
NEG_Q_INDEX = 2
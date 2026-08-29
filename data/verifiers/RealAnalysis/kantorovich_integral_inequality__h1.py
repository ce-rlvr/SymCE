import sympy
import sympy.abc
import math

x = sympy.abc.x

CONDITION_LABELS = [
    "H_1: a < b",
    "H_2: f is bounded by m and M on the interval",
    "not Q: the inequality fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        f = witness['f']
        a = witness['a']
        b = witness['b']
        m = witness['m']
        M = witness['M']
    except (KeyError, TypeError):
        return [False, False, False]
        
    var = witness.get('x', x)
    
    # H1: a < b
    try:
        h1 = float(a) < float(b)
    except Exception:
        h1 = False
        
    # H2: 0 < m <= f(x) <= M for all x in the interval
    h2 = False
    try:
        m_f = float(m)
        M_f = float(M)
        if m_f > 0 and m_f <= M_f:
            a_f = float(a)
            b_f = float(b)
            
            try:
                if hasattr(f, 'subs'):
                    f_lam = sympy.lambdify(var, f, 'math')
                    f_lam(a_f)  # Test evaluation
                else:
                    f_lam = lambda val: float(f)
            except Exception:
                f_lam = lambda val: float(f.subs(var, val)) if hasattr(f, 'subs') else float(f)
                
            h2 = True
            if a_f < b_f:
                # Check 1000 points in the interval
                for i in range(1001):
                    val = a_f + i * (b_f - a_f) / 1000.0
                    f_val = float(f_lam(val))
                    if not (m_f - 1e-7 <= f_val <= M_f + 1e-7):
                        h2 = False
                        break
            else:
                h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: (int_a^b f(x) dx) (int_a^b 1/f(x) dx) > (m+M)^2 / (4mM) * (b-a)^2
    neg_q = False
    try:
        # Attempt symbolic integration first
        int_f = sympy.integrate(f, (var, a, b))
        int_1_f = sympy.integrate(1/f, (var, a, b))
        
        if isinstance(int_f, sympy.Integral) or isinstance(int_1_f, sympy.Integral):
            raise ValueError("Unevaluated integral")
            
        lhs = int_f * int_1_f
        rhs = ((m + M)**2 / (4 * m * M)) * (b - a)**2
        
        try:
            diff = sympy.simplify(lhs - rhs)
            if diff.is_positive:
                neg_q = True
        except Exception:
            pass
            
        if not neg_q:
            lhs_f = float(lhs)
            rhs_f = float(rhs)
            if lhs_f > rhs_f + 1e-12:
                neg_q = True
                
    except Exception:
        # Fallback to numerical integration if symbolic fails
        try:
            a_f = float(a)
            b_f = float(b)
            m_f = float(m)
            M_f = float(M)
            
            try:
                if hasattr(f, 'subs'):
                    f_lam = sympy.lambdify(var, f, 'math')
                    f_lam(a_f)
                else:
                    f_lam = lambda val: float(f)
            except Exception:
                f_lam = lambda val: float(f.subs(var, val)) if hasattr(f, 'subs') else float(f)
                
            n_steps = 10000
            dx = (b_f - a_f) / n_steps
            sum_f = 0.0
            sum_1_f = 0.0
            for i in range(n_steps):
                val = a_f + (i + 0.5) * dx
                f_val = float(f_lam(val))
                sum_f += f_val
                sum_1_f += 1.0 / f_val
                
            int_f_num = sum_f * dx
            int_1_f_num = sum_1_f * dx
            lhs_num = int_f_num * int_1_f_num
            rhs_num = ((m_f + M_f)**2 / (4 * m_f * M_f)) * (b_f - a_f)**2
            
            if lhs_num > rhs_num + 1e-7:
                neg_q = True
        except Exception:
            neg_q = False
            
    return [h1, h2, neg_q]
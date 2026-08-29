import sympy
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: The gradient vector grad f(a) is not the zero vector",
    "¬Q: The directional derivative D_u f(a) does not attain its maximum uniquely at u = grad f(a) / ||grad f(a)||"
]
N_HYP = 1
NEG_Q_INDEX = 1

def evaluate_f(f, vars, pt):
    if callable(f):
        return f(*pt)
    else:
        subs_dict = {var: pt[j] for j, var in enumerate(vars)}
        return f.subs(subs_dict)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness['f']
            vars = witness['vars']
            a = witness['a']
            v = witness.get('v', None)
        else:
            if len(witness) == 4:
                f, vars, a, v = witness
            else:
                f, vars, a = witness
                v = None
                
        t = sympy.Symbol('t', positive=True)
        f_a = evaluate_f(f, vars, a)
        
        # H1: grad f(a) != 0
        g = []
        for i in range(len(vars)):
            pt_right = [a[j] if j != i else a[j] + t for j in range(len(vars))]
            f_right = evaluate_f(f, vars, pt_right)
            lim_right = sympy.limit((f_right - f_a)/t, t, 0, dir='+')
            
            pt_left = [a[j] if j != i else a[j] - t for j in range(len(vars))]
            f_left = evaluate_f(f, vars, pt_left)
            lim_left = sympy.limit((f_left - f_a)/(-t), t, 0, dir='+')
            
            if lim_right in (sympy.oo, -sympy.oo, sympy.nan, sympy.zoo) or \
               lim_left in (sympy.oo, -sympy.oo, sympy.nan, sympy.zoo):
                raise ValueError("Gradient does not exist")
                
            diff_lim = sympy.simplify(lim_right - lim_left)
            try:
                if abs(float(diff_lim)) > 1e-7:
                    raise ValueError("Gradient does not exist")
            except Exception as e:
                if isinstance(e, ValueError):
                    raise
                if diff_lim != 0:
                    raise ValueError("Gradient does not exist")
            g.append(lim_right)
            
        h1 = False
        for c in g:
            try:
                if abs(float(c)) > 1e-7:
                    h1 = True
                    break
            except Exception:
                if sympy.simplify(c) != 0:
                    h1 = True
                    break
                    
        neg_q = False
        if h1:
            norm_g = sympy.sqrt(sum(c**2 for c in g))
            ugrad = [sympy.simplify(c / norm_g) for c in g]
            
            try:
                pt_ugrad = [a[j] + t * ugrad[j] for j in range(len(vars))]
                f_ugrad = evaluate_f(f, vars, pt_ugrad)
                D_ugrad = sympy.limit((f_ugrad - f_a)/t, t, 0, dir='+')
            except Exception:
                D_ugrad = None

            def check_direction(d):
                is_diff = False
                for i in range(len(d)):
                    diff_val = sympy.simplify(d[i] - ugrad[i])
                    try:
                        if abs(float(diff_val)) > 1e-7:
                            is_diff = True
                            break
                    except Exception:
                        if diff_val != 0:
                            is_diff = True
                            break
                if not is_diff:
                    return False
                
                try:
                    pt_d = [a[j] + t * d[j] for j in range(len(vars))]
                    f_d = evaluate_f(f, vars, pt_d)
                    D_d = sympy.limit((f_d - f_a)/t, t, 0, dir='+')
                except Exception:
                    return False
                    
                if D_ugrad is None or (hasattr(D_ugrad, 'has') and D_ugrad.has(sympy.I)) or \
                   D_ugrad in (sympy.nan, sympy.zoo):
                    return True
                if D_d in (sympy.nan, sympy.zoo):
                    return False
                if D_d == sympy.oo and D_ugrad != sympy.oo:
                    return True
                if D_d == sympy.oo and D_ugrad == sympy.oo:
                    return True
                if D_d == -sympy.oo and D_ugrad == -sympy.oo:
                    return True
                if D_d not in (sympy.oo, -sympy.oo) and D_ugrad not in (sympy.oo, -sympy.oo):
                    diff_D = sympy.simplify(D_d - D_ugrad)
                    try:
                        if float(diff_D) >= -1e-7:
                            return True
                    except Exception:
                        try:
                            if bool(diff_D >= 0):
                                return True
                        except TypeError:
                            pass
                return False

            if v is not None:
                norm_v = sympy.simplify(sympy.sqrt(sum(c**2 for c in v)))
                try:
                    is_unit = abs(float(norm_v) - 1.0) < 1e-7
                except Exception:
                    is_unit = sympy.simplify(norm_v - 1) == 0
                if is_unit:
                    neg_q = check_direction(v)
            else:
                if D_ugrad is None or (hasattr(D_ugrad, 'has') and D_ugrad.has(sympy.I)) or \
                   D_ugrad in (sympy.nan, sympy.zoo):
                    neg_q = True
                elif len(vars) == 2:
                    dirs = [
                        (1, 0), (0, 1), (-1, 0), (0, -1),
                        (1/sympy.sqrt(2), 1/sympy.sqrt(2)),
                        (-1/sympy.sqrt(2), 1/sympy.sqrt(2)),
                        (1/sympy.sqrt(2), -1/sympy.sqrt(2)),
                        (-1/sympy.sqrt(2), -1/sympy.sqrt(2))
                    ]
                    for d in dirs:
                        if check_direction(d):
                            neg_q = True
                            break
                            
    except Exception:
        h1 = False
        neg_q = False
        
    return [bool(h1), bool(neg_q)]
import sympy
import math

# Top-level setup for witness expressions
n = sympy.Symbol('n', integer=True)
x = sympy.Symbol('x', real=True)
R = sympy.S.Reals
Interval = sympy.Interval

CONDITION_LABELS = [
    "H_1: X and Y are metric spaces",
    "H_2: {f_n} is a sequence of continuous functions from X to Y",
    "¬Q: The family of functions {f_n} is not equicontinuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    domain = None
    f = None
    
    h1_ok = False
    h2_ok = False
    neg_q_ok = False
    
    is_fast_eval = True
    
    # Parse the witness
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            dom, func = witness
            if hasattr(dom, 'inf') and hasattr(dom, 'sup'):
                a, b = float(dom.inf), float(dom.sup)
                h1_ok = True
            elif isinstance(dom, (tuple, list)) and len(dom) == 2:
                a, b = float(dom[0]), float(dom[1])
                h1_ok = True
            
            if callable(func):
                f = func
            elif hasattr(func, 'subs'):
                try:
                    f_math = sympy.lambdify((n, x), func, modules='math')
                    f_math(1, a + 0.5 * (b - a))
                    f = f_math
                except Exception:
                    f = sympy.lambdify((n, x), func, modules='sympy')
                    is_fast_eval = False
        elif callable(witness):
            a, b = 0.0, 1.0
            h1_ok = True
            f = witness
        elif hasattr(witness, 'subs'):
            a, b = 0.0, 1.0
            h1_ok = True
            try:
                f_math = sympy.lambdify((n, x), witness, modules='math')
                f_math(1, 0.5)
                f = f_math
            except Exception:
                f = sympy.lambdify((n, x), witness, modules='sympy')
                is_fast_eval = False
    except Exception:
        pass

    if not h1_ok or f is None:
        return [False, False, False]
        
    if math.isinf(a): a = -10.0
    if math.isinf(b): b = 10.0
    
    # Check H2: {f_n} is a sequence of continuous functions
    try:
        is_continuous = True
        for n_val in [1, 2, 3]:
            for pt in [a + i * (b - a) / 10 for i in range(1, 10)]:
                try:
                    pt2 = pt + 1e-5
                    if pt2 > b: 
                        pt2 = pt - 1e-5
                    v1 = float(f(n_val, pt))
                    v2 = float(f(n_val, pt2))
                    if abs(v1 - v2) > 1e-2:
                        is_continuous = False
                        break
                except Exception:
                    is_continuous = False
                    break
            if not is_continuous:
                break
        h2_ok = is_continuous
    except Exception:
        h2_ok = False

    # Check neg_Q: The family {f_n} is NOT equicontinuous on X
    try:
        epsilons = [1.0, 0.5, 0.1, 0.05]
        deltas = [0.1, 0.01, 0.001, 0.0001, 1e-5]
        
        if is_fast_eval:
            ns_to_test = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 50000, 100000, 1000000]
            xs_base = [a + i * (b - a) / 2000 for i in range(2001)]
        else:
            ns_to_test = [1, 2, 5, 10, 50, 100, 500, 1000]
            xs_base = [a + i * (b - a) / 100 for i in range(101)]
            
        xs_base += [a + 1e-6, a + 1e-5, a + 1e-4, b - 1e-4, b - 1e-5, b - 1e-6]
        
        for eps in epsilons:
            eps_fails = True
            for delta in deltas:
                found_for_delta = False
                
                for n_val in ns_to_test:
                    xs_n = list(xs_base)
                    xs_n.append(b - delta * 0.9)
                    xs_n.append(a)
                    if n_val > 0:
                        xs_n.extend([a + 1/n_val, a + 2/n_val, a + 0.5/n_val])
                        xs_n.extend([b - 1/n_val, b - 2/n_val, b - 0.5/n_val])
                        sq_n = math.sqrt(n_val)
                        xs_n.extend([a + 1/sq_n, a + 2/sq_n, a + 0.5/sq_n])
                    
                    xs_n = [xv for xv in xs_n if a <= xv <= b]
                    xs_pairs = [(xv, xv + delta * 0.9) for xv in xs_n if xv + delta * 0.9 <= b]
                    
                    for x1, x2 in xs_pairs:
                        try:
                            v1 = float(f(n_val, x1))
                            v2 = float(f(n_val, x2))
                            if abs(v1 - v2) >= eps:
                                found_for_delta = True
                                break
                        except Exception:
                            continue
                            
                    if found_for_delta:
                        break
                        
                if not found_for_delta:
                    eps_fails = False
                    break
                    
            if eps_fails:
                neg_q_ok = True
                break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]
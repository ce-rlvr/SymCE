import sympy as sp
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z, t, n, k = sp.symbols('x y z t n k')

def get_callable_and_domain(witness):
    def parse_domain(d):
        if d is None:
            return (-10.0, 10.0)
        if hasattr(d, 'start') and hasattr(d, 'end'):
            return (float(d.start), float(d.end))
        if isinstance(d, (list, tuple)) and len(d) == 2:
            return (float(d[0]), float(d[1]))
        return (-10.0, 10.0)

    if isinstance(witness, dict):
        if 'f' in witness and 'x' in witness:
            f_expr = witness['f']
            x_sym = witness['x']
            domain = parse_domain(witness.get('domain'))
            
            if 'n' in witness:
                n_sym = witness['n']
                f_lam = sp.lambdify((n_sym, x_sym), f_expr, modules='math')
                def f_callable(n_val, x_val):
                    return float(f_lam(n_val, x_val))
                n_list = witness.get('n_list', list(range(1, 20)))
            else:
                f_lam = sp.lambdify(x_sym, f_expr, modules='math')
                def f_callable(n_val, x_val):
                    return float(f_lam(x_val))
                n_list = [1]
            return f_callable, n_list, domain
            
        elif 'f_callable' in witness:
            f_callable = witness['f_callable']
            try:
                f_callable(1, 0.5)
                f_call = f_callable
                n_list = witness.get('n_list', list(range(1, 20)))
            except TypeError:
                def f_call(n_val, x_val):
                    return float(f_callable(x_val))
                n_list = [1]
            domain = parse_domain(witness.get('domain'))
            return f_call, n_list, domain
            
    if isinstance(witness, sp.Expr):
        free_syms = list(witness.free_symbols)
        if len(free_syms) == 1:
            x_sym = free_syms[0]
            f_lam = sp.lambdify(x_sym, witness, modules='math')
            def f_callable(n_val, x_val):
                return float(f_lam(x_val))
            return f_callable, [1], (-10.0, 10.0)
        elif len(free_syms) >= 2:
            int_names = ['n', 'k', 'm', 'i', 'j']
            n_sym = next((s for s in free_syms if s.name in int_names), free_syms[0])
            x_sym = next((s for s in free_syms if s != n_sym), free_syms[1])
            f_lam = sp.lambdify((n_sym, x_sym), witness, modules='math')
            def f_callable(n_val, x_val):
                return float(f_lam(n_val, x_val))
            return f_callable, list(range(1, 20)), (-10.0, 10.0)
            
    if isinstance(witness, list) and all(isinstance(w, sp.Expr) for w in witness):
        free_syms = set()
        for expr in witness:
            free_syms.update(expr.free_symbols)
        if len(free_syms) == 1:
            x_sym = list(free_syms)[0]
            lams = [sp.lambdify(x_sym, expr, modules='math') for expr in witness]
            def f_callable(n_val, x_val):
                return float(lams[n_val](x_val))
            return f_callable, list(range(len(witness))), (-10.0, 10.0)
            
    if isinstance(witness, list) and all(callable(w) for w in witness):
        def f_callable(n_val, x_val):
            return float(witness[n_val](x_val))
        return f_callable, list(range(len(witness))), (-10.0, 10.0)
            
    if callable(witness):
        try:
            witness(1, 0.5)
            f_call = witness
            n_list = list(range(1, 20))
        except TypeError:
            def f_call(n_val, x_val):
                return float(witness(x_val))
            n_list = [1]
        return f_call, n_list, (-10.0, 10.0)
            
    return None, None, None

def is_equicontinuous(f_callable, n_list, domain, positive_part=False):
    a, b = domain
    if a is None or a == -float('inf'): a = -10.0
    if b is None or b == float('inf'): b = 10.0
    
    test_points = [a + (b - a) * i / 20.0 for i in range(1, 20)]
    deltas = [0.1, 0.01, 0.001, 0.0001]
    
    extended_n = list(n_list) + [100, 1000, 10000, 100000]
    
    success_count = 0
    
    for x in test_points:
        vars_for_deltas = []
        for delta in deltas:
            max_var = 0.0
            for n in extended_n:
                for y in [x - delta, x + delta]:
                    if y < a or y > b: continue
                    try:
                        v_x = f_callable(n, x)
                        v_y = f_callable(n, y)
                        if not (math.isfinite(v_x) and math.isfinite(v_y)):
                            continue
                        if positive_part:
                            v_x = max(v_x, 0.0)
                            v_y = max(v_y, 0.0)
                        var = abs(v_x - v_y)
                        if var > max_var:
                            max_var = var
                        success_count += 1
                    except Exception:
                        pass
            vars_for_deltas.append(max_var)
        
        if vars_for_deltas and vars_for_deltas[-1] > 0.05:
            return False
            
    if success_count == 0:
        return False
        
    return True

def conditions(witness) -> list[bool]:
    H1 = False
    H2 = False
    neg_Q = False
    
    try:
        f_callable, n_list, domain = get_callable_and_domain(witness)
        if f_callable is not None:
            H1 = is_equicontinuous(f_callable, n_list, domain, positive_part=False)
            H2 = True  # Definition of F+ is trivially satisfied by construction
            Q = is_equicontinuous(f_callable, n_list, domain, positive_part=True)
            neg_Q = not Q
    except Exception:
        pass
        
    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: F is an equicontinuous family of real-valued functions on X",
    "H_2: F^+ is the family of functions defined by f^+(x) = max(f(x), 0)",
    "¬Q: The family F^+ is not equicontinuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy as sp
import math
import itertools

# Top-level setup: named object bindings that the witness expression may reference
x, y, z = sp.symbols('x y z', real=True)

CONDITION_LABELS = [
    "H_1: U is an open, connected set",
    "H_2: f is a twice continuously differentiable function",
    "H_3: f attains a local or global maximum at some interior point x0",
    "¬Q: f is not constant throughout U"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample.
    The witness should be a tuple (f, x0) where:
      - f is a sympy expression representing the function f: U -> R
      - x0 is a dictionary mapping variables to their values at the maximum point
    """
    try:
        f = sp.sympify(witness[0])
        x0 = witness[1]
        
        if not isinstance(x0, dict):
            return [False, False, False, False]
            
        vars = list(x0.keys())
        
        # Ensure all free symbols in f are assigned a value in x0
        if not f.free_symbols.issubset(set(vars)):
            return [False, False, False, False]
            
        # H_1: U is an open, connected set.
        # We assume U is an open connected neighborhood around x0.
        # We verify that f is defined and real at x0.
        try:
            v0 = f.subs(x0)
            float(v0)
            h1 = True
        except Exception:
            h1 = False
            
        # H_2: f is a twice continuously differentiable function.
        # We verify that all second partial derivatives exist and are finite at x0.
        try:
            h2 = True
            for v1 in vars:
                for v2 in vars:
                    d2f = sp.diff(f, v1, v2)
                    val = d2f.subs(x0)
                    try:
                        v_float = float(val)
                        if math.isnan(v_float) or math.isinf(v_float):
                            h2 = False
                            break
                    except Exception:
                        h2 = False
                        break
                if not h2:
                    break
        except Exception:
            h2 = False
            
        # H_3: f attains a local or global maximum at some interior point x0.
        try:
            h3 = True
            # Necessary condition: Gradient must be zero at x0
            for v in vars:
                df = sp.diff(f, v)
                val = df.subs(x0)
                eq_zero = val.equals(0)
                if eq_zero is False:
                    h3 = False
                    break
                elif eq_zero is None:
                    try:
                        if abs(float(val)) > 1e-9:
                            h3 = False
                            break
                    except Exception:
                        h3 = False
                        break
            
            # Sufficient condition: Check a small neighborhood around x0
            if h3:
                is_local_max = False
                v0_exact = f.subs(x0)
                # Test multiple scales of perturbations to handle flat or steep functions
                eps_list = [sp.Rational(1, 10**i) for i in range(1, 6)]
                for eps in eps_list:
                    perturbations = [[-eps, 0, eps] for _ in vars]
                    all_le = True
                    for p in itertools.product(*perturbations):
                        if all(dp == 0 for dp in p):
                            continue
                        test_point = {v: x0[v] + p[i] for i, v in enumerate(vars)}
                        v_test = f.subs(test_point)
                        diff = sp.simplify(v_test - v0_exact)
                        
                        if diff.is_positive:
                            all_le = False
                            break
                        elif diff.is_positive is None:
                            try:
                                if float(diff) > 1e-14:
                                    all_le = False
                                    break
                            except Exception:
                                all_le = False
                                break
                    if all_le:
                        is_local_max = True
                        break
                if not is_local_max:
                    h3 = False
        except Exception:
            h3 = False
            
        # ¬Q: f is not constant throughout U.
        try:
            is_const = True
            for v in f.free_symbols:
                df = sp.diff(f, v)
                if not df.equals(0):
                    is_const = False
                    break
            neg_q = not is_const
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]
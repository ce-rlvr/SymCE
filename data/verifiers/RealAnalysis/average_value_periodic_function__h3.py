import sympy
import math

# Top-level setup
x = sympy.Symbol('x', real=True)

def conditions(witness):
    try:
        # Witness can be a dictionary or a tuple (f, T, A)
        if isinstance(witness, dict):
            f = witness.get('f')
            T = witness.get('T')
            A = witness.get('A')
        else:
            f, T, A = witness
            
        if callable(f):
            f = f(x)
            
        f = sympy.sympify(f)
        T = sympy.sympify(T)
        A = sympy.sympify(A)
        
        free_symbols = f.free_symbols
        if len(free_symbols) == 1:
            var = list(free_symbols)[0]
        elif len(free_symbols) == 0:
            var = x
        else:
            var = x
            if var not in free_symbols:
                return [False, False, False]
                
    except Exception:
        return [False, False, False]

    # H_1: The function f is continuous
    try:
        T_val = float(T.evalf())
        h1 = True
        
        # Try rigorous singularity check first
        try:
            from sympy.calculus.singularities import singularities
            from sympy import S
            sings = singularities(f, var, S.Reals)
            if not sings.is_empty:
                h1 = False
        except Exception:
            pass
            
        # Fallback/supplementary check via sampling
        if h1:
            for i in range(1000):
                val = f.subs(var, T_val * i / 999.0).evalf()
                if not val.is_real or not val.is_finite or abs(val) > 1e6:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: The function f is periodic with period T > 0
    try:
        h2 = False
        if T_val > 0:
            # Algebraic check
            diff = sympy.simplify(f.subs(var, var + T) - f)
            if diff == 0:
                h2 = True
            else:
                # Numerical check
                h2 = True
                for i in range(20):
                    test_pt = T_val * i / 19.0
                    v1 = float(f.subs(var, test_pt).evalf())
                    v2 = float(f.subs(var, test_pt + T_val).evalf())
                    if abs(v1 - v2) > 1e-5:
                        h2 = False
                        break
    except Exception:
        h2 = False

    # ¬Q: There does not exist c in [0, T] such that f(c) = A
    try:
        A_val = float(A.evalf())
        N_samples = 1000
        min_val = float('inf')
        max_val = float('-inf')
        
        # Sample the function to find its approximate range on [0, T]
        for i in range(N_samples + 1):
            val = float(f.subs(var, T_val * i / N_samples).evalf())
            if val < min_val: min_val = val
            if val > max_val: max_val = val
            
        # If A is strictly outside the range of f, then f(c) = A has no solution
        if A_val < min_val - 1e-4 or A_val > max_val + 1e-4:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The function f is continuous",
    "H_2: The function f is periodic with period T > 0",
    "¬Q: There does not exist c in the interval from 0 to T such that f(c) = A"
]

N_HYP = 2
NEG_Q_INDEX = 2
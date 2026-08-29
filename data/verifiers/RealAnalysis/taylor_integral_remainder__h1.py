import sympy as sp
import math

# Top-level setup
x, t = sp.symbols('x t')

CONDITION_LABELS = [
    "H_1: f is n+1 times continuously differentiable",
    "¬Q: Taylor theorem conclusion fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    witness is expected to be a tuple (f, a, b, n) or a dictionary with these keys.
    f: SymPy expression
    a, b: interval endpoints (real numbers)
    n: integer
    """
    try:
        if isinstance(witness, dict):
            f = sp.sympify(witness.get('f', 'x'))
            a = sp.sympify(witness.get('a', 0))
            b = sp.sympify(witness.get('b', 1))
            n = sp.sympify(witness.get('n', -1))
        else:
            f, a, b, n = [sp.sympify(v) for v in witness]
    except Exception:
        return [False, False]

    free_symbols = f.free_symbols
    if len(free_symbols) == 1:
        var = list(free_symbols)[0]
    elif len(free_symbols) == 0:
        var = sp.Symbol('x')
    else:
        if sp.Symbol('x') in free_symbols:
            var = sp.Symbol('x')
        elif sp.Symbol('t') in free_symbols:
            var = sp.Symbol('t')
        else:
            var = list(free_symbols)[0]

    # H_1: f is n+1 times continuously differentiable
    h1 = False
    try:
        if sp.S(n + 1).is_integer and n + 1 >= 0:
            deriv = sp.diff(f, var, int(n + 1))
            h1 = True
            a_val = float(a)
            b_val = float(b)
            # Check continuity heuristically by evaluating at a few points
            pts = [a_val, b_val, (a_val + b_val) / 2, a_val + (b_val - a_val) / 4, b_val - (b_val - a_val) / 4]
            for pt in pts:
                val = float(deriv.subs(var, pt))
                if not math.isfinite(val):
                    h1 = False
                    break
    except Exception:
        h1 = False

    # neg_Q: Conclusion fails
    neg_q = False
    try:
        LHS = f.subs(var, b)
        
        sum_val = 0
        if n >= 0:
            for k in range(int(n) + 1):
                term = sp.diff(f, var, k).subs(var, a) / sp.factorial(k) * (b - a)**k
                sum_val += term
                
        n_fact = sp.factorial(n)
        if n_fact in (sp.zoo, sp.oo, sp.nan) or (n.is_real and n < 0 and n.is_integer):
            integral_val = 0
        else:
            dummy = sp.Symbol('dummy_t', real=True)
            integrand = sp.diff(f, var, int(n + 1)).subs(var, dummy) / n_fact * (b - dummy)**n
            integral_val = sp.integrate(integrand, (dummy, a, b))
            
        RHS = sum_val + integral_val
        
        diff_val = sp.simplify(LHS - RHS)
        if diff_val == 0:
            neg_q = False
        else:
            try:
                if abs(float(diff_val)) < 1e-9:
                    neg_q = False
                else:
                    neg_q = True
            except Exception:
                neg_q = True
    except Exception:
        neg_q = True

    return [h1, neg_q]
import sympy as sp
import math

# Top-level setup
x = sp.Symbol('x', real=True)

class LCG:
    """Simple Linear Congruential Generator for deterministic pseudo-random numbers."""
    def __init__(self, seed=42):
        self.state = seed

    def random(self):
        # LCG parameters from POSIX drand48
        self.state = (25214903917 * self.state + 11) & ((1 << 48) - 1)
        return self.state / (1 << 48)

    def uniform(self, a, b):
        return a + (b - a) * self.random()

def is_not_differentiable_numerically(eval_f, x0):
    try:
        h_vals = [1e-4, 1e-6, 1e-8]
        diffs = []
        for h in h_vals:
            v_plus = eval_f(x0 + h)
            v_center = eval_f(x0)
            v_minus = eval_f(x0 - h)
            der_right = (v_plus - v_center) / h
            der_left = (v_center - v_minus) / h
            diffs.append(abs(der_right - der_left))
        # If the difference between left and right derivative approximations
        # remains large and doesn't shrink significantly, it's likely not differentiable.
        if diffs[-1] > 1e-4 and diffs[-1] >= diffs[0] * 0.5:
            return True
    except Exception:
        pass
    return False

def check_neg_conclusion(f, var, a, b, L):
    df = f.diff(var)
    
    try:
        f_lam = sp.lambdify(var, f, modules=['math'])
    except Exception:
        f_lam = lambda x_val: float(f.subs(var, x_val))
        
    def eval_f(x_val):
        try:
            return float(f_lam(x_val))
        except Exception:
            return float(f.subs(var, x_val))
            
    try:
        df_lam = sp.lambdify(var, df, modules=['math'])
    except Exception:
        df_lam = lambda x_val: float(df.subs(var, x_val))
        
    def eval_df(x_val):
        try:
            return float(df_lam(x_val))
        except Exception:
            return float(df.subs(var, x_val))
            
    suspicious_points = set()
    
    def add_roots(expr):
        try:
            roots = sp.solve(expr, var)
            for r in roots:
                try:
                    r_float = float(r)
                    if a < r_float < b:
                        suspicious_points.add(r_float)
                except Exception:
                    pass
        except Exception:
            pass

    # Find points where f might not be differentiable
    for node in f.find(sp.Abs):
        add_roots(node.args[0])
        
    for node in f.find(sp.Piecewise):
        for expr, cond in node.args:
            if isinstance(cond, sp.Rel):
                lhs, rhs = cond.args
                add_roots(lhs - rhs)
                
    for node in f.find(sp.Pow):
        base, exp = node.args
        if exp == sp.Rational(1, 2) or exp == 0.5:
            add_roots(base)
            
    for node in f.find(sp.Min) | f.find(sp.Max):
        args = node.args
        for i in range(len(args)):
            for j in range(i + 1, len(args)):
                add_roots(args[i] - args[j])
                
    # 1. Check suspicious points for non-differentiability or derivative bound violation
    for x0 in suspicious_points:
        try:
            x0_rat = sp.Rational(str(x0))
            L_left = df.limit(var, x0_rat, dir='-')
            L_right = df.limit(var, x0_rat, dir='+')
            if L_left != L_right:
                return True
            if abs(float(L_left)) > L + 1e-5 or abs(float(L_right)) > L + 1e-5:
                return True
        except Exception:
            if is_not_differentiable_numerically(eval_f, x0):
                return True

    rng = LCG(1337)
    
    # 2. Check a few random points for non-differentiability just in case
    for _ in range(20):
        x0 = rng.uniform(float(a), float(b))
        if is_not_differentiable_numerically(eval_f, x0):
            return True

    # 3. Dense grid check for derivative bound
    for _ in range(1000):
        x0 = rng.uniform(float(a), float(b))
        try:
            der = eval_df(x0)
            if abs(der) > L + 1e-5:
                return True
        except Exception:
            pass
            
    return False

def check_lipschitz(f, var, a, b, L):
    rng = LCG(42)
    try:
        f_lam = sp.lambdify(var, f, modules=['math'])
    except Exception:
        f_lam = lambda x_val: float(f.subs(var, x_val))
        
    def eval_f(x_val):
        try:
            return float(f_lam(x_val))
        except Exception:
            return float(f.subs(var, x_val))
            
    # Check random pairs
    for _ in range(2000):
        x1 = rng.uniform(float(a), float(b))
        x2 = rng.uniform(float(a), float(b))
        if x1 == x2:
            continue
        try:
            y1 = eval_f(x1)
            y2 = eval_f(x2)
            if abs(y1 - y2) > L * abs(x1 - x2) + 1e-4:
                return False
        except Exception:
            return False
            
    # Check close pairs to catch discontinuities
    for _ in range(1000):
        x1 = rng.uniform(float(a), float(b))
        x2 = x1 + rng.uniform(-1e-5, 1e-5)
        if x2 <= a or x2 >= b or x1 == x2:
            continue
        try:
            y1 = eval_f(x1)
            y2 = eval_f(x2)
            if abs(y1 - y2) > L * abs(x1 - x2) + 1e-4:
                return False
        except Exception:
            return False
            
    return True

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f = witness['f']
            a = witness['a']
            b = witness['b']
            L = witness['L']
        else:
            f, a, b, L = witness
            
        a = float(a)
        b = float(b)
        L = float(L)
        
        if a >= b:
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        if callable(f):
            var = sp.Symbol('x')
            f = sp.sympify(f(var))
        else:
            f = sp.sympify(f)
            free_syms = f.free_symbols
            if free_syms:
                var = list(free_syms)[0]
            else:
                var = sp.Symbol('x')
    except Exception:
        var = sp.Symbol('x')
        try:
            f = sp.sympify(f)
        except Exception:
            return [False, False]
            
    try:
        h1_ok = check_lipschitz(f, var, a, b, L)
    except Exception:
        h1_ok = False
        
    try:
        neg_q_ok = check_neg_conclusion(f, var, a, b, L)
    except Exception:
        neg_q_ok = False
        
    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: f is Lipschitz continuous on (a, b) with constant L",
    "¬Q: There exists x in (a, b) where f'(x) does not exist or |f'(x)| > L"
]

N_HYP = 1
NEG_Q_INDEX = 1
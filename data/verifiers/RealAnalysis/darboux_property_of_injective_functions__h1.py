import sympy
import math

# Top-level setup
x = sympy.Symbol('x')

def safe_eval(f, X):
    Y = []
    for val in X:
        y = float(f(val))
        if math.isnan(y) or math.isinf(y):
            raise ValueError("Invalid value")
        Y.append(y)
    return Y

def has_ivp(f, a, b):
    N = 1000
    X = [a + i*(b-a)/N for i in range(N+1)]
    try:
        Y = safe_eval(f, X)
    except Exception:
        return False
    total_range = max(Y) - min(Y)
    if total_range == 0: return True
    
    sorted_Y = sorted(Y)
    gaps = [(sorted_Y[i+1] - sorted_Y[i], sorted_Y[i], sorted_Y[i+1]) for i in range(len(sorted_Y)-1)]
    gaps.sort(reverse=True, key=lambda item: item[0])
    
    for gap_size, y_A, y_B in gaps[:10]:
        if gap_size < 1e-4 * total_range:
            break
            
        straddling_intervals = []
        for i in range(N):
            if (Y[i] <= y_A and Y[i+1] >= y_B) or (Y[i] >= y_B and Y[i+1] <= y_A):
                straddling_intervals.append((X[i], X[i+1]))
                
        gap_filled = False
        for x0, x1 in straddling_intervals:
            curr_x0, curr_x1 = x0, x1
            for _ in range(5):
                x_new = [curr_x0 + j*(curr_x1-curr_x0)/10 for j in range(11)]
                try:
                    y_new = safe_eval(f, x_new)
                except Exception:
                    return False
                
                margin = 0.1 * gap_size
                inside = [y for y in y_new if y_A + margin < y < y_B - margin]
                if inside:
                    gap_filled = True
                    break
                    
                found_straddle = False
                for k in range(10):
                    if (y_new[k] <= y_A and y_new[k+1] >= y_B) or (y_new[k] >= y_B and y_new[k+1] <= y_A):
                        curr_x0, curr_x1 = x_new[k], x_new[k+1]
                        found_straddle = True
                        break
                if not found_straddle:
                    break
            if gap_filled:
                break
                
        if not gap_filled:
            return False
            
    return True

def is_injective(f, a, b):
    N = 500
    X = [a + i*(b-a)/N for i in range(N+1)]
    try:
        Y = safe_eval(f, X)
    except Exception:
        return False
    total_range = max(Y) - min(Y)
    if total_range == 0:
        return False
    for i in range(N+1):
        for j in range(i+2, N+1):
            if abs(X[i] - X[j]) > 1e-2 * (b-a):
                if abs(Y[i] - Y[j]) < 1e-9 * total_range:
                    return False
    return True

def is_continuous(f, a, b):
    N = 1000
    X = [a + i*(b-a)/N for i in range(N+1)]
    try:
        Y = safe_eval(f, X)
    except Exception:
        return False
    total_range = max(Y) - min(Y)
    if total_range == 0: return True
    
    for i in range(N):
        if abs(Y[i+1] - Y[i]) > 5e-3 * total_range:
            x0, x1 = X[i], X[i+1]
            gap_persists = True
            for _ in range(5):
                x_new = [x0 + j*(x1-x0)/10 for j in range(11)]
                try:
                    y_new = safe_eval(f, x_new)
                except Exception:
                    return False
                gaps = [abs(y_new[j+1] - y_new[j]) for j in range(10)]
                max_gap = max(gaps)
                if max_gap < 2e-3 * total_range:
                    gap_persists = False
                    break
                max_idx = gaps.index(max_gap)
                x0, x1 = x_new[max_idx], x_new[max_idx+1]
            if gap_persists:
                return False
    return True

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            f_in, a, b = witness
            if isinstance(f_in, sympy.Expr):
                syms = list(f_in.free_symbols)
                var = syms[0] if syms else x
                f = sympy.lambdify(var, f_in, 'math')
            elif callable(f_in):
                f = f_in
            else:
                return [False, False, False]
            
            a = float(a)
            b = float(b)
            if a >= b:
                return [False, False, False]
                
            ivp = has_ivp(f, a, b)
            inj = is_injective(f, a, b)
            cont = is_continuous(f, a, b)
            
            return [bool(ivp), bool(inj), not bool(cont)]
    except Exception:
        pass
    return [False, False, False]

CONDITION_LABELS = [
    "H_1: f satisfies the intermediate value property",
    "H_2: f is injective",
    "not_Q: f is not continuous"
]
N_HYP = 2
NEG_Q_INDEX = 2
import sympy as sp
import math

# Top-level setup
x, n = sp.symbols('x n', real=True)

CONDITION_LABELS = ["H_1: f_n is strictly increasing", "H_2: f_n converges uniformly to f", "not Q: inverse functions do not converge uniformly"]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f_n_expr = witness['f_n']
            f_expr = witness['f']
            a = float(witness['a'])
            b = float(witness['b'])
        else:
            f_n_expr, f_expr, a, b = witness
            a = float(a)
            b = float(b)
            
        if isinstance(f_n_expr, str):
            f_n_expr = sp.sympify(f_n_expr)
        if isinstance(f_expr, str):
            f_expr = sp.sympify(f_expr)
            
        _f_n_num = sp.lambdify((n, x), f_n_expr, 'math')
        f_n_num = lambda nv, xv: float(_f_n_num(nv, xv))
        
        _f_num = sp.lambdify(x, f_expr, 'math')
        f_num = lambda xv: float(_f_num(xv))
        
        # H_1: (f_n) is strictly increasing
        h1 = True
        for n_val in [1, 2, 5, 10, 100]:
            grid = [a + i*(b-a)/100 for i in range(101)]
            for i in range(100):
                try:
                    if f_n_num(n_val, grid[i]) >= f_n_num(n_val, grid[i+1]):
                        h1 = False
                        break
                except Exception:
                    h1 = False
                    break
            if not h1:
                break
                
        # H_2: (f_n) converges uniformly to f
        h2 = True
        grid = [a + i*(b-a)/100 for i in range(101)]
        max_diffs = []
        for n_val in [10, 100, 1000, 10000]:
            try:
                diffs = [abs(f_n_num(n_val, xv) - f_num(xv)) for xv in grid]
                max_diffs.append(max(diffs))
            except Exception:
                h2 = False
                break
        if h2:
            if max_diffs[-1] > 0.1 or (len(max_diffs) > 1 and max_diffs[-1] >= max_diffs[0] and max_diffs[-1] > 1e-5):
                h2 = False
                
        # neg_Q
        neg_q = False
        f_strictly_inc = True
        for i in range(100):
            try:
                if f_num(grid[i]) >= f_num(grid[i+1]):
                    f_strictly_inc = False
                    break
            except Exception:
                f_strictly_inc = False
                break
                
        if not f_strictly_inc:
            neg_q = True
        else:
            domain_fails = False
            try:
                for n_val in [10, 20, 50, 100, 1000]:
                    val_a = f_n_num(n_val, a) - f_num(a)
                    val_b = f_num(b) - f_n_num(n_val, b)
                    if val_a > 1e-8 or val_b > 1e-8:
                        domain_fails = True
                        break
            except Exception:
                pass
                
            if domain_fails:
                neg_q = True
            else:
                max_inv_diffs = []
                for n_val in [10, 50, 100, 1000]:
                    diffs = []
                    for i in range(51):
                        try:
                            y = f_num(a) + i*(f_num(b)-f_num(a))/50
                            low, high = a, b
                            for _ in range(50):
                                mid = (low + high) / 2
                                if f_n_num(n_val, mid) < y:
                                    low = mid
                                else:
                                    high = mid
                            x_n = (low + high) / 2
                            
                            low_f, high_f = a, b
                            for _ in range(50):
                                mid = (low_f + high_f) / 2
                                if f_num(mid) < y:
                                    low_f = mid
                                else:
                                    high_f = mid
                            x_val = (low_f + high_f) / 2
                            
                            diffs.append(abs(x_n - x_val))
                        except Exception:
                            diffs.append(1.0)
                    max_inv_diffs.append(max(diffs))
                    
                if max_inv_diffs[-1] > 0.05 or (len(max_inv_diffs) > 1 and max_inv_diffs[-1] >= max_inv_diffs[0] and max_inv_diffs[-1] > 1e-4):
                    neg_q = True
                    
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]
import sympy as sp
import math

# Top-level setup
x = sp.Symbol('x', real=True)
n = sp.Symbol('n', integer=True, positive=True)

def get_grid(domain):
    grid = []
    try:
        if isinstance(domain, sp.FiniteSet):
            return [float(arg) for arg in domain.args]
            
        if domain.start != -sp.oo and domain.end != sp.oo:
            start = float(domain.start)
            end = float(domain.end)
            grid = [start + j * (end - start) / 100.0 for j in range(101)]
            grid += [start + 10**(-k) for k in range(1, 8)]
            grid += [end - 10**(-k) for k in range(1, 8)]
        elif domain.start != -sp.oo:
            start = float(domain.start)
            grid = [start + j * 1.0 for j in range(100)] + [start + j * 10.0 for j in range(100)]
            grid += [start + 10**(-k) for k in range(1, 8)]
        elif domain.end != sp.oo:
            end = float(domain.end)
            grid = [end - j * 1.0 for j in range(100)] + [end - j * 10.0 for j in range(100)]
            grid += [end - 10**(-k) for k in range(1, 8)]
        else:
            grid = [j * 1.0 for j in range(-100, 101)] + [j * 10.0 for j in range(-100, 101)]
    except:
        pass
    return grid

def check_H2(f_n, domain, delta):
    try:
        if float(delta) <= 0:
            return False
            
        cps = []
        try:
            deriv = sp.diff(f_n, x)
            cps = sp.solve(deriv, x)
        except:
            pass
            
        for i in [1, 2, 3, 10, 100]:
            expr = f_n.subs(n, i)
            vals = []
            
            for cp_gen in cps:
                try:
                    cp = cp_gen.subs(n, i)
                    if cp.is_real:
                        cp_val = float(cp)
                        if domain.contains(cp_val):
                            vals.append(float(expr.subs(x, cp_val)))
                except:
                    pass
                    
            try:
                if domain.start != -sp.oo:
                    vals.append(float(expr.subs(x, domain.start)))
                else:
                    try:
                        vals.append(float(expr.subs(x, -1e10)))
                    except OverflowError:
                        pass
            except:
                pass
                
            try:
                if domain.end != sp.oo:
                    vals.append(float(expr.subs(x, domain.end)))
                else:
                    try:
                        vals.append(float(expr.subs(x, 1e10)))
                    except OverflowError:
                        pass
            except:
                pass
                
            try:
                f_num = sp.lambdify(x, expr, 'math')
                grid = get_grid(domain)
                for pt in grid:
                    try:
                        vals.append(float(f_num(pt)))
                    except:
                        pass
            except:
                pass
                
            if not vals:
                return False
                
            min_val = min(vals)
            if min_val < float(delta) - 1e-5:
                return False
                
        return True
    except:
        return False

def check_neg_Q(f_n, f, domain):
    try:
        expr_gen = f_n / f
        cps = []
        try:
            deriv = sp.diff(expr_gen, x)
            cps = sp.solve(deriv, x)
        except:
            pass
            
        S_n_list = []
        for i in [10, 100, 1000, 10000, 100000]:
            expr = expr_gen.subs(n, i)
            vals = []
            
            for cp_gen in cps:
                try:
                    cp = cp_gen.subs(n, i)
                    if cp.is_real:
                        cp_val = float(cp)
                        if domain.contains(cp_val):
                            vals.append(float(expr.subs(x, cp_val)))
                except:
                    pass
            
            try:
                if domain.start != -sp.oo:
                    vals.append(float(expr.subs(x, domain.start)))
                else:
                    try:
                        vals.append(float(expr.subs(x, -1e10)))
                    except OverflowError:
                        vals.append(float('inf'))
            except:
                pass
            
            try:
                if domain.end != sp.oo:
                    vals.append(float(expr.subs(x, domain.end)))
                else:
                    try:
                        vals.append(float(expr.subs(x, 1e10)))
                    except OverflowError:
                        vals.append(float('inf'))
            except:
                pass
            
            try:
                f_num = sp.lambdify(x, expr, 'math')
                grid = get_grid(domain)
                for pt in grid:
                    try:
                        vals.append(float(f_num(pt)))
                    except:
                        pass
            except:
                pass
            
            max_diff = 0
            for val in vals:
                if val <= 0:
                    max_diff = float('inf')
                    break
                diff = abs(math.log(val))
                if diff > max_diff:
                    max_diff = diff
            
            S_n_list.append(max_diff)
            
        if S_n_list[-1] == float('inf'):
            return True
            
        if S_n_list[-1] > 0.01:
            if S_n_list[-1] >= 0.9 * S_n_list[-2]:
                return True
                
        return False
    except:
        return False

def conditions(witness) -> list[bool]:
    try:
        f_n, f, domain, delta = witness
    except Exception:
        return [False, False, False]
        
    def check_H1():
        try:
            grid = get_grid(domain)
            if not grid:
                return False
            expr = f_n.subs({n: 1, x: grid[0]})
            val = float(expr)
            return math.isfinite(val) or math.isinf(val)
        except Exception:
            return False
            
    def check_H2_func():
        return check_H2(f_n, domain, delta)
        
    def check_neg_Q_func():
        return check_neg_Q(f_n, f, domain)
        
    return [check_H1(), check_H2_func(), check_neg_Q_func()]

CONDITION_LABELS = [
    "H_1: (f_n) is a sequence of real-valued functions on E",
    "H_2: f_n(x) >= delta > 0 for all n and x in E",
    "¬Q: ln(f_n) does not converge uniformly to ln(f) on E"
]

N_HYP = 2
NEG_Q_INDEX = 2
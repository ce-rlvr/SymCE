import sympy
import math

# Top-level setup
x = sympy.Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: f is a real-valued function",
    "¬Q: f is NOT Lipschitz continuous on R with Lipschitz constant L"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        # The witness can be a tuple (f, L) or just an expression f
        if isinstance(witness, tuple) and len(witness) == 2:
            f_sym, L_val = witness
        else:
            f_sym = witness
            L_val = None
            
        h1 = False
        if isinstance(f_sym, sympy.Expr):
            h1 = True
            # Check if f is defined and real-valued everywhere on R
            try:
                domain = sympy.calculus.util.continuous_domain(f_sym, x, sympy.S.Reals)
                if domain != sympy.S.Reals:
                    h1 = False
            except Exception:
                # Fallback if continuous_domain fails
                try:
                    for x0 in [-1.5, -0.5, 0.0, 0.5, 1.5]:
                        val = f_sym.subs(x, x0).evalf()
                        if not val.is_real:
                            h1 = False
                            break
                except Exception:
                    pass
                
        if not h1:
            return [False, False]
            
        f_lam = sympy.lambdify(x, f_sym, modules=['math', 'sympy'])
        neg_q = False
        
        if L_val is not None:
            try:
                L_val = float(L_val)
            except Exception:
                return [h1, False]
                
            # Check for Lipschitz violation: |f(x) - f(y)| > L * |x - y|
            for i in range(200):
                # Deterministic pseudo-random points
                u1 = (math.sin(i * 12.3456) * 4321.1234) % 1.0
                x0 = -100 + 200 * u1
                u2 = (math.cos(i * 65.4321) * 1234.4321) % 1.0
                y0 = x0 - 1 + 2 * u2
                if x0 == y0: 
                    continue
                try:
                    fx = float(f_lam(x0))
                    fy = float(f_lam(y0))
                    if abs(fx - fy) > L_val * abs(x0 - y0) + 1e-7:
                        neg_q = True
                        break
                except Exception:
                    pass
                    
            # Check derivative if violation not found yet
            if not neg_q:
                try:
                    df = sympy.diff(f_sym, x)
                    df_lam = sympy.lambdify(x, df, modules=['math', 'sympy'])
                    for i in range(200):
                        u1 = (math.sin(i * 12.3456) * 4321.1234) % 1.0
                        x0 = -100 + 200 * u1
                        try:
                            val = float(df_lam(x0))
                            if abs(val) > L_val + 1e-7:
                                neg_q = True
                                break
                        except Exception:
                            pass
                except Exception:
                    pass
        else:
            # If L is not provided, we must show f is NOT Lipschitz for ANY L.
            # This means the derivative is unbounded.
            try:
                df = sympy.diff(f_sym, x)
                df_lam = sympy.lambdify(x, df, modules=['math', 'sympy'])
                
                # Check large x values
                for x0 in [1e6, -1e6, 1e9, -1e9, 100.0, -100.0, 10.0, -10.0]:
                    try:
                        val = float(df_lam(x0))
                        if abs(val) > 1e4:
                            neg_q = True
                            break
                    except Exception:
                        pass
                        
                # Check near 0
                if not neg_q:
                    for x0 in [1e-5, -1e-5, 1e-9, -1e-9]:
                        try:
                            val = float(df_lam(x0))
                            if abs(val) > 1e4:
                                neg_q = True
                                break
                        except Exception:
                            pass
                            
                # Check pseudo-random points
                if not neg_q:
                    for i in range(200):
                        u1 = (math.sin(i * 12.3456) * 4321.1234) % 1.0
                        x0 = -100 + 200 * u1
                        try:
                            val = float(df_lam(x0))
                            if abs(val) > 1e4:
                                neg_q = True
                                break
                        except Exception:
                            pass
            except Exception:
                pass
                
        return [h1, neg_q]
    except Exception:
        return [False, False]
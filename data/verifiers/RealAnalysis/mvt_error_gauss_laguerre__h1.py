import sympy as sp
from sympy.abc import x
import math
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.polys.orthopolys import laguerre_poly

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        f, n = witness
    except Exception:
        return [False, False, False]
        
    # H1: I_n(f) is the n-point Gauss-Laguerre quadrature approximation
    try:
        if not isinstance(n, int) or n < 1:
            h1 = False
        else:
            # Verify f is a valid sympy expression
            f.subs(x, 1)
            h1 = True
    except Exception:
        h1 = False

    # H2: The integral converges
    try:
        integral_val = sp.integrate(sp.exp(-x) * f, (x, 0, sp.oo))
        if integral_val.has(sp.oo, -sp.oo, sp.nan, sp.zoo):
            h2 = False
        elif integral_val.is_finite is False:
            h2 = False
        else:
            try:
                val_float = float(integral_val.evalf())
                if math.isnan(val_float) or math.isinf(val_float):
                    h2 = False
                else:
                    h2 = True
                    integral_val = val_float
            except Exception:
                num_int = sp.Integral(sp.exp(-x) * f, (x, 0, sp.oo)).evalf()
                val_float = float(num_int)
                if math.isnan(val_float) or math.isinf(val_float):
                    h2 = False
                else:
                    h2 = True
                    integral_val = val_float
    except Exception:
        try:
            num_int = sp.Integral(sp.exp(-x) * f, (x, 0, sp.oo)).evalf()
            val_float = float(num_int)
            if math.isnan(val_float) or math.isinf(val_float):
                h2 = False
            else:
                h2 = True
                integral_val = val_float
        except Exception:
            h2 = False

    # neg_Q: There is NO c in (0, oo) such that Error == (n!)^2 / (2n)! * f^(2n)(c)
    try:
        L_n = laguerre_poly(n, x)
        L_n_plus_1 = laguerre_poly(n+1, x)
        
        roots = sp.roots(L_n, x)
        if len(roots) == n:
            nodes = list(roots.keys())
        else:
            nodes = [sp.re(root) for root in sp.nroots(L_n)]
            
        I_n = 0
        for node in nodes:
            w = node / ( (n+1)**2 * L_n_plus_1.subs(x, node)**2 )
            term = w * f.subs(x, node)
            I_n += float(sp.re(term.evalf()))
            
        error_val = integral_val - I_n
        coeff = (sp.factorial(n)**2) / sp.factorial(2*n)
        target_val = float(error_val / coeff)
        
        f_2n = sp.diff(f, x, 2*n).doit()
        
        exact_no_sol = False
        try:
            sols = sp.solve(f_2n - target_val, x)
            if isinstance(sols, list):
                if len(sols) == 0:
                    exact_no_sol = True
                else:
                    has_valid = False
                    for s in sols:
                        try:
                            if s.is_real and s > 0:
                                has_valid = True
                                break
                        except Exception:
                            pass
                    if has_valid:
                        neg_q = False
                        return [h1, h2, neg_q]
                    else:
                        exact_no_sol = True
        except Exception:
            pass

        f_2n_vals = []
        pts = [0.05, 0.1, 0.5, 0.9, 1.1, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 7.0, 10.0, 15.0, 20.0]
        for pt in pts:
            v = None
            try:
                v_sym = f_2n.subs(x, pt).evalf()
                if v_sym.is_real:
                    v = float(v_sym)
            except Exception:
                pass
            
            if v is None and n == 1:
                try:
                    h_step = 1e-4
                    v_num = (f.subs(x, pt+h_step) - 2*f.subs(x, pt) + f.subs(x, pt-h_step)) / (h_step**2)
                    v = float(v_num.evalf())
                except Exception:
                    pass
                    
            if v is not None:
                f_2n_vals.append(v)
                
        if exact_no_sol:
            neg_q = True
        elif f_2n_vals:
            min_val = min(f_2n_vals)
            max_val = max(f_2n_vals)
            if max_val - min_val < 1e-5:
                if abs(target_val - min_val) > 1e-4:
                    neg_q = True
                else:
                    neg_q = False
            else:
                if target_val > max_val + 1e-2 or target_val < min_val - 1e-2:
                    neg_q = True
                else:
                    neg_q = False
        else:
            neg_q = False
            
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I_n(f) is the n-point Gauss-Laguerre quadrature approximation",
    "H_2: The integral converges",
    "¬Q: There is no c in (0, oo) satisfying the error formula"
]

N_HYP = 2
NEG_Q_INDEX = 2
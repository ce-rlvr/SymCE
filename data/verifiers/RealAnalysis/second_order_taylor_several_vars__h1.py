import sympy as sp
import math

# Top-level setup for the verifier
x, y, z = sp.symbols('x y z', real=True)
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: f is a twice continuously differentiable function",
    "H_2: a and a+h are points in U such that the line segment connecting them lies entirely in U",
    "¬Q: There does not exist a point c on the open line segment between a and a+h such that the Taylor equation holds"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f = witness['f']
            vars = witness['vars']
            a = witness['a']
            h = witness['h']
        else:
            f, vars, a, h = witness
    except Exception:
        return [False, False, False]
        
    # H_1: f is twice continuously differentiable
    try:
        f_sym = sp.sympify(f)
        grad = [sp.diff(f_sym, v) for v in vars]
        hessian = [[sp.diff(g, v) for v in vars] for g in grad]
        h1_ok = True
    except Exception:
        h1_ok = False
        
    # H_2: a and a+h are in U, and the line segment lies entirely in U
    try:
        h2_ok = True
        # Check at endpoints and midpoint to ensure no singularities on the segment
        for t_val in [0, 0.5, 1]:
            pt = [sp.sympify(a_i) + t_val * sp.sympify(h_i) for a_i, h_i in zip(a, h)]
            subs_dict = dict(zip(vars, pt))
            
            val = f_sym.subs(subs_dict)
            if val.has(sp.oo, -sp.oo, sp.nan, sp.zoo) or val.is_real is False:
                h2_ok = False
                break
                
            for g in grad:
                g_val = g.subs(subs_dict)
                if g_val.has(sp.oo, -sp.oo, sp.nan, sp.zoo) or g_val.is_real is False:
                    h2_ok = False
                    break
            if not h2_ok: break
            
            for row in hessian:
                for h_ij in row:
                    h_val = h_ij.subs(subs_dict)
                    if h_val.has(sp.oo, -sp.oo, sp.nan, sp.zoo) or h_val.is_real is False:
                        h2_ok = False
                        break
                if not h2_ok: break
    except Exception:
        h2_ok = False
        
    # ¬Q: The conclusion fails at the witness
    try:
        neg_q = False
        
        # If h is the zero vector, the open line segment between a and a+h is empty.
        # Thus, there DOES NOT EXIST any point c on the open line segment.
        is_h_zero = True
        for h_i in h:
            val = sp.sympify(h_i)
            if not (val.is_zero or (val.is_number and abs(float(val.evalf())) < 1e-12)):
                is_h_zero = False
                break
                
        if is_h_zero:
            neg_q = True
        else:
            t = sp.Symbol('t', real=True)
            c = [sp.sympify(a_i) + t * sp.sympify(h_i) for a_i, h_i in zip(a, h)]
            subs_c = dict(zip(vars, c))
            
            subs_a = dict(zip(vars, a))
            subs_ah = dict(zip(vars, [sp.sympify(a_i) + sp.sympify(h_i) for a_i, h_i in zip(a, h)]))
            
            f_a = f_sym.subs(subs_a)
            f_ah = f_sym.subs(subs_ah)
            
            grad_a = [g.subs(subs_a) for g in grad]
            grad_dot_h = sum(g * sp.sympify(h_i) for g, h_i in zip(grad_a, h))
            
            h_T_H_h = 0
            for i in range(len(vars)):
                for j in range(len(vars)):
                    H_ij_c = hessian[i][j].subs(subs_c)
                    h_T_H_h += sp.sympify(h[i]) * H_ij_c * sp.sympify(h[j])
                    
            # E(t) = f(a) + grad(f)(a)*h + 1/2 * h^T * H_f(a+th) * h - f(a+h)
            E = f_a + grad_dot_h + sp.Rational(1, 2) * h_T_H_h - f_ah
            E_simp = sp.simplify(E)
            
            if E_simp == 0 or (E_simp.is_number and abs(float(E_simp.evalf())) < 1e-12):
                neg_q = False
            else:
                is_identically_zero = True
                for test_t in [0.123, 0.456, 0.789]:
                    try:
                        if abs(float(E_simp.subs(t, test_t).evalf())) > 1e-9:
                            is_identically_zero = False
                            break
                    except Exception:
                        is_identically_zero = False
                        break
                        
                if is_identically_zero:
                    neg_q = False
                else:
                    found_c = False
                    try:
                        sols = sp.solve(E_simp, t)
                        if isinstance(sols, list):
                            for sol in sols:
                                try:
                                    sol_val = float(sp.re(sol.evalf()))
                                    im_val = float(sp.im(sol.evalf()))
                                    if abs(im_val) < 1e-9 and 0 < sol_val < 1:
                                        found_c = True
                                        break
                                except Exception:
                                    pass
                        elif isinstance(sols, sp.Expr):
                            try:
                                sol_val = float(sp.re(sols.evalf()))
                                im_val = float(sp.im(sols.evalf()))
                                if abs(im_val) < 1e-9 and 0 < sol_val < 1:
                                    found_c = True
                            except Exception:
                                pass
                    except Exception:
                        pass
                    
                    if not found_c:
                        for guess in [0.1, 0.25, 0.5, 0.75, 0.9]:
                            try:
                                sol_val = float(sp.nsolve(E_simp, t, guess))
                                if 0 < sol_val < 1:
                                    val_at_sol = float(E_simp.subs(t, sol_val).evalf())
                                    if abs(val_at_sol) < 1e-7:
                                        found_c = True
                                        break
                            except Exception:
                                pass
                                
                    if not found_c:
                        neg_q = True
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, neg_q]
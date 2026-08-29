import sympy as sp
import math

CONDITION_LABELS = [
    "H_1: f is a proper, lower semicontinuous, convex function",
    "H_2: lambda > 0",
    "H_3: y1 and y2 are the proximal operators of x1 and x2",
    "¬Q: The proximal operator is not globally 1-Lipschitz (dist(y1, y2) > dist(x1, x2))"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        dim = int(witness['dim'])
        p = float(witness['p'])
        lambda_val = float(witness['lambda_val'])
        x1 = tuple(witness['x1'])
        x2 = tuple(witness['x2'])
        y1 = tuple(witness['y1'])
        y2 = tuple(witness['y2'])
        f_expr = witness['f_expr']
        
        y_syms = sp.symbols(f'y0:{dim}')
        x_syms = sp.symbols(f'x0:{dim}')
        
    except Exception:
        return [False, False, False, False]

    # H1: f is a proper, lower semicontinuous, convex function
    try:
        hessian = sp.hessian(f_expr, y_syms)
        
        def is_psd(matrix, point):
            sub_dict = dict(zip(y_syms, point))
            num_mat = matrix.subs(sub_dict)
            if dim == 2:
                trace = float(sp.re(num_mat.trace()))
                det = float(sp.re(num_mat.det()))
                return trace >= -1e-5 and det >= -1e-5
            else:
                evals = num_mat.eigenvals()
                return all(float(sp.re(ev)) >= -1e-5 for ev in evals)

        is_constant = all(hessian[i, j].is_constant() for i in range(dim) for j in range(dim))
        if is_constant:
            h1_ok = is_psd(hessian, y1)
        else:
            h1_ok = is_psd(hessian, y1) and is_psd(hessian, y2) and is_psd(hessian, tuple([0]*dim))
    except Exception:
        h1_ok = False

    # H2: lambda > 0
    try:
        h2_ok = lambda_val > 0
    except Exception:
        h2_ok = False

    # H3: y1 and y2 are the proximal operators of x1 and x2
    try:
        if p % 2 == 0:
            norm_p_sq = (sum((x_syms[i] - y_syms[i])**int(p) for i in range(dim)))**(2/p)
        else:
            norm_p_sq = (sum(sp.Abs(x_syms[i] - y_syms[i])**p for i in range(dim)))**(2/p)
            
        obj = f_expr + (1 / (2 * lambda_val)) * norm_p_sq
        grad_obj = [sp.diff(obj, yi) for yi in y_syms]
        
        def grad_norm(x_val, y_val):
            sub_dict = dict(zip(x_syms, x_val))
            sub_dict.update(dict(zip(y_syms, y_val)))
            g_val = [float(sp.re(g.subs(sub_dict))) for g in grad_obj]
            return math.sqrt(sum(gv**2 for gv in g_val))
            
        gn1 = grad_norm(x1, y1)
        gn2 = grad_norm(x2, y2)
        
        # A zero gradient is necessary and sufficient for the global minimum of a strictly convex objective
        h3_ok = (gn1 < 1e-4) and (gn2 < 1e-4)
    except Exception:
        h3_ok = False

    # ¬Q: The proximal operator is not globally 1-Lipschitz
    try:
        def norm_p(v):
            return sum(abs(vi)**p for vi in v)**(1/p)
            
        dist_x = norm_p([x1[i] - x2[i] for i in range(dim)])
        dist_y = norm_p([y1[i] - y2[i] for i in range(dim)])
        
        neg_q_ok = dist_y > dist_x + 1e-5
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]
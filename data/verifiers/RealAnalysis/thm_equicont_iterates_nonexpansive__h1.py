import sympy as sp
from sympy.abc import x
import math

# Top-level setup for potential witness expressions
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: f is a non-expansive mapping",
    "¬Q: The sequence of iterated functions {f^n} is not equicontinuous"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            domain, f = witness
            witness = f

        if isinstance(witness, str):
            witness = sp.sympify(witness)

        if isinstance(witness, sp.Expr):
            f = witness
            df = sp.diff(f, x)
            
            try:
                f_lam = sp.lambdify(x, f, 'math')
                df_lam = sp.lambdify(x, df, 'math')
            except Exception:
                f_lam = lambda val: float(f.subs(x, val))
                df_lam = lambda val: float(df.subs(x, val))
            
            pts = [i * 0.1 for i in range(-100, 101)]
            
            h1 = False
            success_count = 0
            is_non_exp = True
            for pt in pts:
                try:
                    val = df_lam(pt)
                    success_count += 1
                    if abs(val) > 1.000001:
                        is_non_exp = False
                        break
                except Exception:
                    pass
            if success_count > 0 and is_non_exp:
                h1 = True
                    
            neg_q = False
            for pt in pts:
                try:
                    val = pt
                    df_prod = 1.0
                    for _ in range(100):
                        df_val = df_lam(val)
                        df_prod *= df_val
                        val = f_lam(val)
                        if abs(df_prod) > 1000:
                            neg_q = True
                            break
                    if neg_q:
                        break
                except Exception:
                    pass

        elif isinstance(witness, sp.Matrix):
            A = witness
            ATA = A.T * A
            ata_eigenvals = ATA.eigenvals()
            max_ata_ev = max([abs(ev) for ev in ata_eigenvals.keys()])
            norm_A = math.sqrt(float(max_ata_ev))
            
            h1 = bool(norm_A <= 1.000001)
            
            A_100 = A**100
            max_elem = max([abs(elem) for elem in A_100])
            neg_q = bool(max_elem > 1000)

        elif callable(witness):
            pts = [i * 0.1 for i in range(-100, 101)]
            
            h1 = False
            success_count = 0
            is_non_exp = True
            for i in range(len(pts)):
                for j in range(i+1, len(pts)):
                    try:
                        diff_y = abs(witness(pts[i]) - witness(pts[j]))
                        diff_x = abs(pts[i] - pts[j])
                        success_count += 1
                        if diff_y > diff_x + 1e-7:
                            is_non_exp = False
                            break
                    except Exception:
                        pass
                if not is_non_exp:
                    break
            if success_count > 0 and is_non_exp:
                h1 = True
                    
            neg_q = False
            for pt in pts:
                try:
                    val = pt
                    df_prod = 1.0
                    for _ in range(100):
                        h_step = 1e-5
                        df = (witness(val + h_step) - witness(val - h_step)) / (2 * h_step)
                        df_prod *= df
                        val = witness(val)
                        if abs(df_prod) > 1000:
                            neg_q = True
                            break
                    if neg_q:
                        break
                except Exception:
                    pass
                    
        elif isinstance(witness, dict):
            h1 = bool(witness.get("is_non_expansive", False))
            neg_q = not bool(witness.get("is_equicontinuous", True))
            
    except Exception:
        pass

    return [h1, neg_q]
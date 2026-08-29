import sympy
from sympy.abc import x
import math

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: f is differentiable on the interval",
    "¬Q: f inverse does not exist or is not Lipschitz continuous"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 4:
            return [False, False]
        f, a, b, c = witness
    except Exception:
        return [False, False]
        
    # H1: f is differentiable on the interval
    try:
        a_sym = sympy.sympify(a)
        b_sym = sympy.sympify(b)
        if float(a_sym) >= float(b_sym):
            h1 = False
        else:
            df = sympy.diff(f, x)
            try:
                from sympy.calculus.util import continuous_domain
                dom = continuous_domain(df, x, sympy.Interval(a_sym, b_sym))
                h1 = (dom == sympy.Interval(a_sym, b_sym))
            except Exception:
                # Fallback if continuous_domain fails
                h1 = True
                df_lam = sympy.lambdify(x, df, modules=['math', 'sympy'])
                for i in range(101):
                    p = float(a_sym) + i * (float(b_sym) - float(a_sym)) / 100.0
                    try:
                        v = df_lam(p)
                        if math.isnan(float(v)) or math.isinf(float(v)):
                            h1 = False
                            break
                    except Exception:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # neg_Q: f^-1 does not exist OR is not Lipschitz with constant 1/c
    try:
        c_float = float(c)
        if c_float <= 0:
            neg_q = True
        else:
            neg_q = False
            f_lam = sympy.lambdify(x, f, modules=['math', 'sympy'])
            df_lam = sympy.lambdify(x, df, modules=['math', 'sympy'])
            
            a_float = float(a)
            b_float = float(b)
            
            # 1. Dense grid check for derivative
            n_pts = 2000
            if n_pts > 1:
                step = (b_float - a_float) / (n_pts - 1)
                for i in range(n_pts):
                    p = a_float + i * step
                    try:
                        dval = df_lam(p)
                        if isinstance(dval, complex):
                            if abs(dval.imag) > 1e-9:
                                continue
                            dval = dval.real
                        if abs(float(dval)) < c_float - 1e-9:
                            neg_q = True
                            break
                    except Exception:
                        pass
            
            # 2. Pairwise check
            if not neg_q:
                n_pts_small = 200
                if n_pts_small > 1:
                    step_small = (b_float - a_float) / (n_pts_small - 1)
                    pts = [a_float + i * step_small for i in range(n_pts_small)]
                    vals = []
                    for p in pts:
                        try:
                            val = f_lam(p)
                            if isinstance(val, complex):
                                if abs(val.imag) > 1e-9:
                                    continue
                                val = val.real
                            vals.append((p, float(val)))
                        except Exception:
                            pass
                    
                    for i in range(len(vals)):
                        if neg_q: break
                        for j in range(i + 1, len(vals)):
                            u, fu = vals[i]
                            v, fv = vals[j]
                            if c_float * abs(u - v) > abs(fu - fv) + 1e-7:
                                neg_q = True
                                break
    except Exception:
        neg_q = False

    return [h1, neg_q]
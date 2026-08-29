import sympy
from sympy import Symbol, Abs, oo, limit
import math

# Top-level setup
x = Symbol('x', real=True)
L = Symbol('L', real=True, nonnegative=True)
A = Symbol('A', real=True, nonnegative=True)

CONDITION_LABELS = [
    "H_1: f is a function from R to R",
    "¬Q: f does not have linear growth (violates |f(x)| <= A + L|x|)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # Parse witness into a sympy expression
        if not isinstance(witness, sympy.Expr):
            if callable(witness):
                f = witness(x)
            else:
                f = sympy.sympify(witness)
        else:
            f = witness
            
        # Substitute any free symbols other than 'x' with 1 to evaluate properly
        if isinstance(f, sympy.Expr):
            for sym in f.free_symbols:
                if sym.name != 'x':
                    f = f.subs(sym, 1)
                    
        # H_1: Check if f evaluates to finite real numbers for real inputs
        h1_ok = True
        for v in [0, 1, -1, 2.5, -3.14]:
            val = f.subs(x, v).evalf()
            if not val.is_real or not val.is_finite:
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        if h1_ok:
            # ¬Q: Check if f has superlinear growth (limsup |f(x)|/|x| = oo)
            
            # 1. Try analytical limits first
            try:
                L1 = limit(Abs(f) / Abs(x), x, oo)
                if L1 == oo or (hasattr(L1, 'max') and L1.max == oo):
                    neg_q_ok = True
            except Exception:
                pass
            
            if not neg_q_ok:
                try:
                    L2 = limit(Abs(f) / Abs(x), x, -oo)
                    if L2 == oo or (hasattr(L2, 'max') and L2.max == oo):
                        neg_q_ok = True
                except Exception:
                    pass
            
            # 2. Numerical fallback for superlinear growth
            if not neg_q_ok:
                ratios_pos = []
                ratios_neg = []
                # Evaluate at increasing magnitudes
                for k in range(3, 8):
                    base = 10**k
                    max_val_pos = -1.0
                    max_val_neg = -1.0
                    # Take the maximum ratio over a small window to handle oscillating functions
                    for offset in range(10):
                        v = base + offset
                        try:
                            val_pos = float(Abs(f.subs(x, v)) / v)
                            if val_pos > max_val_pos:
                                max_val_pos = val_pos
                        except Exception:
                            pass
                        try:
                            val_neg = float(Abs(f.subs(x, -v)) / v)
                            if val_neg > max_val_neg:
                                max_val_neg = val_neg
                        except Exception:
                            pass
                    if max_val_pos >= 0:
                        ratios_pos.append(max_val_pos)
                    if max_val_neg >= 0:
                        ratios_neg.append(max_val_neg)
                
                # If the ratio |f(x)|/|x| is strictly and significantly increasing, it's superlinear
                if len(ratios_pos) >= 4:
                    diffs = [ratios_pos[i+1] - ratios_pos[i] for i in range(len(ratios_pos)-1)]
                    if all(d > 0.5 for d in diffs):
                        neg_q_ok = True
                
                if not neg_q_ok and len(ratios_neg) >= 4:
                    diffs = [ratios_neg[i+1] - ratios_neg[i] for i in range(len(ratios_neg)-1)]
                    if all(d > 0.5 for d in diffs):
                        neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]
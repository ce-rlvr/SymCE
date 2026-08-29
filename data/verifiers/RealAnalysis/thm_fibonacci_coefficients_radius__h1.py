import sympy as sp
from sympy.abc import n, x
import math

# Top-level setup
# (No specific named objects required for this real analysis theorem)

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, str):
            witness = sp.sympify(witness)
            
        phi = sp.Rational(1, 2) + sp.sqrt(5)/2
        phi_val = float((1/phi).evalf())
        
        if isinstance(witness, tuple) and len(witness) == 2:
            F_n, R = witness
            h1 = True
            try:
                diff = sp.simplify(R - 1/phi)
                is_eq = (diff == 0) or (abs(float(diff.evalf())) < 1e-7)
            except Exception:
                is_eq = False
            if not is_eq:
                neg_q = True

        elif isinstance(witness, sp.Expr) and len(witness.free_symbols) == 1:
            sym = list(witness.free_symbols)[0]
            h1 = True
            if str(sym) in ['x', 'y', 'z', 't']:
                try:
                    poles = sp.solve(sp.denom(sp.cancel(witness)), sym)
                    if poles:
                        R = min([abs(complex(p.evalf())) for p in poles])
                        is_eq = abs(R - phi_val) < 1e-7
                    else:
                        is_eq = False
                except Exception:
                    is_eq = False
                if not is_eq:
                    neg_q = True
            else:
                F_n = witness
                F_n_plus_1 = F_n.subs(sym, sym+1)
                ratio = sp.Abs(F_n / F_n_plus_1)
                try:
                    R = sp.limit(ratio, sym, sp.oo)
                    if R.has(sp.oo, sp.zoo, sp.nan, sp.AccumBounds):
                        is_eq = False
                    else:
                        diff = sp.simplify(R - 1/phi)
                        is_eq = (diff == 0) or (abs(float(diff.evalf())) < 1e-7)
                except Exception:
                    try:
                        r_val = float(ratio.subs(sym, 1000).evalf())
                        is_eq = abs(r_val - phi_val) < 1e-5
                    except Exception:
                        is_eq = False
                if not is_eq:
                    neg_q = True

        elif isinstance(witness, sp.Expr) and len(witness.free_symbols) == 0:
            h1 = True
            try:
                val = float(witness.evalf())
                R = sp.oo if val == 0 else 1
                is_eq = abs(float(R) - phi_val) < 1e-7 if R != sp.oo else False
            except Exception:
                is_eq = False
            if not is_eq:
                neg_q = True

        elif callable(witness):
            h1 = True
            try:
                F_n = witness(n)
                if isinstance(F_n, sp.Expr) and n in F_n.free_symbols:
                    F_n_plus_1 = F_n.subs(n, n+1)
                    ratio = sp.Abs(F_n / F_n_plus_1)
                    R = sp.limit(ratio, n, sp.oo)
                    if R.has(sp.oo, sp.zoo, sp.nan, sp.AccumBounds):
                        is_eq = False
                    else:
                        diff = sp.simplify(R - 1/phi)
                        is_eq = (diff == 0) or (abs(float(diff.evalf())) < 1e-7)
                else:
                    raise ValueError
            except Exception:
                try:
                    F_1000 = float(sp.Abs(witness(1000)))
                    F_1001 = float(sp.Abs(witness(1001)))
                    if F_1001 == 0:
                        is_eq = False
                    else:
                        r_val = F_1000 / F_1001
                        is_eq = abs(r_val - phi_val) < 1e-5
                except Exception:
                    is_eq = False
            if not is_eq:
                neg_q = True

        elif isinstance(witness, (int, float, sp.Number)):
            h1 = True
            R = sp.oo if witness == 0 else 1
            is_eq = abs(float(R) - phi_val) < 1e-7 if R != sp.oo else False
            if not is_eq:
                neg_q = True

        elif isinstance(witness, list):
            h1 = True
            is_eq = False
            if not is_eq:
                neg_q = True

    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A power series is given by sum_{n=0}^infty F_n x^n",
    "¬Q: The radius of convergence of the power series is not 1/phi"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
import math

# Top-level setup
n = sympy.Symbol('n', integer=True)
x = sympy.Symbol('x')

def conditions(witness):
    h1_ok = False
    try:
        if isinstance(witness, sympy.Expr):
            syms = witness.free_symbols
            sym = n
            if len(syms) == 1:
                sym = list(syms)[0]
            elif len(syms) > 1 and n in syms:
                sym = n
            elif len(syms) > 1:
                sym = list(syms)[0]
                
            v0 = witness.subs(sym, 0)
            if abs(float(v0)) < 1e-7:
                h1_ok = True
                for i in [1, 2, 3, 10, 100, 1000]:
                    vi = witness.subs(sym, i)
                    if abs(float(vi) - math.log(i)) > 1e-7:
                        h1_ok = False
                        break
        elif callable(witness):
            v0 = witness(0)
            if abs(float(v0)) < 1e-7:
                h1_ok = True
                for i in [1, 2, 3, 10, 100, 1000]:
                    vi = witness(i)
                    if abs(float(vi) - math.log(i)) > 1e-7:
                        h1_ok = False
                        break
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        if isinstance(witness, sympy.Expr):
            syms = witness.free_symbols
            sym = n
            if len(syms) == 1:
                sym = list(syms)[0]
            elif len(syms) > 1 and n in syms:
                sym = n
            elif len(syms) > 1:
                sym = list(syms)[0]

            k = sympy.Symbol('k', integer=True, positive=True)
            ak = witness.subs(sym, k)
            akp1 = witness.subs(sym, k+1)
            ratio = sympy.Abs(ak / akp1)
            L = sympy.limit(ratio, k, sympy.oo)
            if L == 1:
                neg_q_ok = False
            elif L.is_number:
                neg_q_ok = float(L) != 1.0
            else:
                raise ValueError("Limit unevaluated")
        elif callable(witness):
            try:
                a1 = float(witness(10000))
                a2 = float(witness(10001))
                n_val = 10000
            except OverflowError:
                a1 = float(witness(100))
                a2 = float(witness(101))
                n_val = 100
            
            if math.isinf(a1) or math.isinf(a2) or math.isnan(a1) or math.isnan(a2):
                neg_q_ok = True
            else:
                if a2 == 0:
                    if a1 == 0:
                        R = float('inf')
                    else:
                        denom = abs(a1) ** (1.0 / n_val)
                        if denom == 0:
                            R = float('inf')
                        else:
                            R = 1.0 / denom
                else:
                    R = abs(a1 / a2)
                
                if abs(R - 1.0) < 1e-2:
                    neg_q_ok = False
                else:
                    neg_q_ok = True
    except Exception:
        try:
            if isinstance(witness, sympy.Expr):
                syms = witness.free_symbols
                sym = n
                if len(syms) == 1:
                    sym = list(syms)[0]
                elif len(syms) > 1 and n in syms:
                    sym = n
                elif len(syms) > 1:
                    sym = list(syms)[0]

                try:
                    a1 = float(witness.subs(sym, 10000))
                    a2 = float(witness.subs(sym, 10001))
                    n_val = 10000
                except OverflowError:
                    a1 = float(witness.subs(sym, 100))
                    a2 = float(witness.subs(sym, 101))
                    n_val = 100

                if math.isinf(a1) or math.isinf(a2) or math.isnan(a1) or math.isnan(a2):
                    neg_q_ok = True
                else:
                    if a2 == 0:
                        if a1 == 0:
                            R = float('inf')
                        else:
                            denom = abs(a1) ** (1.0 / n_val)
                            if denom == 0:
                                R = float('inf')
                            else:
                                R = 1.0 / denom
                    else:
                        R = abs(a1 / a2)
                    
                    if abs(R - 1.0) < 1e-2:
                        neg_q_ok = False
                    else:
                        neg_q_ok = True
            else:
                neg_q_ok = False
        except Exception:
            neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The sequence of coefficients is given by a_n = ln(n) for n >= 1, and a_0 = 0",
    "¬Q: The radius of convergence of the power series is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1
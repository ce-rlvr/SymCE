import sympy
from sympy import mobius, Symbol
import math

# Top-level setup
n = Symbol('n', integer=True)
x = Symbol('x')

def evaluate_witness(witness, i):
    if isinstance(witness, dict):
        return witness.get(i, 0)
    if isinstance(witness, (list, tuple)):
        return witness[i]
    if callable(witness):
        try:
            return witness(i)
        except Exception:
            pass
    if hasattr(witness, 'free_symbols'):
        syms = list(witness.free_symbols)
        if len(syms) == 1:
            return witness.subs(syms[0], i)
        elif len(syms) == 0:
            return witness
    try:
        return witness.subs(n, i)
    except AttributeError:
        return witness

def conditions(witness):
    # H_1: a_n = mobius(n) for all n >= 1
    h1_ok = True
    try:
        for i in range(1, 101):
            val = evaluate_witness(witness, i)
            if float(val) != float(mobius(i)):
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    # neg_Q: The radius of convergence is NOT exactly 1
    neg_q = False
    try:
        vals = []
        for i in range(1, 201):
            try:
                val = evaluate_witness(witness, i)
                vals.append(abs(float(val)))
            except IndexError:
                break
        
        if not vals:
            neg_q = False
        else:
            if all(v == 0 for v in vals):
                R = float('inf')
            elif max(vals) <= 1.0 and sum(1 for v in vals if v >= 0.99) > 10:
                R = 1.0
            elif len(vals) >= 20 and all(v == 0 for v in vals[-20:]):
                R = float('inf')
            else:
                last_vals = [v**(1/i) for i, v in enumerate(vals, 1) if v > 0][-20:]
                if not last_vals:
                    R = float('inf')
                else:
                    est = sum(last_vals) / len(last_vals)
                    if est == 0:
                        R = float('inf')
                    else:
                        R = 1 / est
                    
            if R == float('inf') or abs(R - 1.0) > 0.15:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: a_n = mu(n) for all integers n >= 1",
    "¬Q: The radius of convergence of the power series is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1
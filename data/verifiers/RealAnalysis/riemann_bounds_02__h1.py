import sympy
from sympy import integrate, Abs, Symbol

x = Symbol('x', real=True)
y = Symbol('y', real=True)
z = Symbol('z', real=True)

def conditions(witness):
    try:
        f, a, b = witness
        
        int_f = integrate(f, (x, a, b))
        lhs = Abs(int_f)
        
        int_abs_f = integrate(Abs(f), (x, a, b))
        rhs = int_abs_f
        
        lhs_val = float(lhs.evalf())
        rhs_val = float(rhs.evalf())
        
        neg_q = bool(lhs_val > rhs_val + 1e-9)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: |\\int_a^b f(x) dx| > \\int_a^b |f(x)| dx"
]
N_HYP = 0
NEG_Q_INDEX = 0
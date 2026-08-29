import sympy as sp
from sympy.calculus.util import continuous_domain

# Top-level setup for witness expressions
x, y, z = sp.symbols('x y z', real=True)
sin = sp.sin
cos = sp.cos
exp = sp.exp
log = sp.log
pi = sp.pi
E = sp.E

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    The witness can be a tuple (f, a, b), a dict {'f': f, 'a': a, 'b': b}, or just a function f (with default a=0, b=1).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            f, a, b = witness
        elif isinstance(witness, dict):
            f = witness.get('f', witness)
            a = witness.get('a', 0)
            b = witness.get('b', 1)
        else:
            f = witness
            a = 0
            b = 1
            
        if callable(f):
            try:
                f = f(x)
            except Exception:
                pass
                
        f = sp.sympify(f)
        a = sp.sympify(a)
        b = sp.sympify(b)
        
        free_syms = f.free_symbols
        if len(free_syms) == 1:
            sym = list(free_syms)[0]
            f = f.subs(sym, x)
        elif len(free_syms) > 1:
            return [False, False]
            
    except Exception:
        return [False, False]

    # H_1: f is continuous on the interval
    try:
        if not bool(a < b):
            h1 = False
        else:
            domain = continuous_domain(f, x, sp.Interval(a, b))
            h1 = (domain == sp.Interval(a, b))
    except Exception:
        h1 = False

    # ¬Q: f is not constant
    try:
        val0 = sp.simplify(f.subs(x, a))
        pts = [
            a + (b - a) / 2,
            a + (b - a) / sp.sqrt(2),
            a + (b - a) / sp.E
        ]
        is_const = True
        for pt in pts:
            val_i = sp.simplify(f.subs(x, pt))
            if sp.simplify(val_i - val0) != 0:
                is_const = False
                break
        neg_q = not is_const
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is continuous on the interval",
    "¬Q: f is not constant"
]

N_HYP = 1
NEG_Q_INDEX = 1
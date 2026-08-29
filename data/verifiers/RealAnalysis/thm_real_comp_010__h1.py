import sympy
from sympy import Symbol, Abs, Sum, oo, limit

# Top-level setup: named object bindings that the witness expression may reference.
n = Symbol('n', integer=True, positive=True)
k = Symbol('k', integer=True, positive=True)
x = Symbol('x', real=True)
y = Symbol('y', real=True)

def conditions(witness) -> list[bool]:
    # Determine the sequence expression and its index variable
    try:
        if callable(witness):
            idx = n
            a_n = witness(idx)
        else:
            a_n = witness
            free_syms = a_n.free_symbols
            if n in free_syms:
                idx = n
            elif k in free_syms:
                idx = k
            elif len(free_syms) == 1:
                idx = list(free_syms)[0]
            else:
                idx = n
    except Exception:
        return [False, False]

    # H_1: The limit superior of the sequence |a_{n+1} / a_n| as n \to \infty is strictly less than 1.
    try:
        a_n_plus_1 = a_n.subs(idx, idx + 1)
        ratio = Abs(a_n_plus_1 / a_n)
        L = limit(ratio, idx, oo)
        
        if hasattr(L, 'is_AccumBounds') and L.is_AccumBounds:
            L = L.max
            
        if L is None or L.has(sympy.nan):
            h1_ok = False
        else:
            try:
                h1_ok = bool(L < 1)
            except TypeError:
                h1_ok = False
    except Exception:
        h1_ok = False

    # neg_Q: The infinite series \sum_{n=1}^{\infty} a_n does NOT converge absolutely.
    try:
        abs_a_n = Abs(a_n)
        s = Sum(abs_a_n, (idx, 1, oo))
        conv = s.is_convergent()
        
        # Fallback if sympy cannot directly determine convergence
        if conv is None:
            val = s.doit()
            if val.is_number and val.is_finite is not None:
                conv = bool(val.is_finite)
                
        if conv is None:
            neg_q_ok = False
        else:
            neg_q_ok = not bool(conv)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The limit superior of the sequence |a_{n+1} / a_n| as n to infinity is strictly less than 1",
    "¬Q: The infinite series does not converge absolutely"
]

N_HYP = 1
NEG_Q_INDEX = 1
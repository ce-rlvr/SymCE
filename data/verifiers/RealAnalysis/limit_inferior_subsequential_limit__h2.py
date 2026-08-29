import sympy
from sympy import Symbol, oo

# Top-level setup
n = Symbol('n', integer=True, positive=True)

def conditions(witness):
    # H1: (x_n) is a sequence of real numbers
    try:
        if not isinstance(witness, sympy.Expr):
            h1 = False
        else:
            h1 = True
            free_syms = witness.free_symbols
            if len(free_syms) > 1:
                h1 = False
            elif not free_syms:
                val = witness.evalf()
                if not val.is_real:
                    h1 = False
            else:
                sym = list(free_syms)[0]
                for i in range(1, 6):
                    val = witness.subs(sym, i).evalf()
                    if not val.is_real:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # neg_Q: No subsequence converges to liminf x_n
    # This is true iff liminf x_n is -oo or oo.
    try:
        if not isinstance(witness, sympy.Expr):
            neg_q = False
        else:
            free_syms = witness.free_symbols
            if len(free_syms) > 1:
                neg_q = False
            elif not free_syms:
                neg_q = False
            else:
                sym = list(free_syms)[0]
                L = sympy.limit(witness, sym, oo)
                if L == oo or L == -oo:
                    neg_q = True
                elif hasattr(L, 'min') and L.min == -oo:
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: (x_n) is a sequence of real numbers",
    "¬Q: No subsequence of (x_n) converges to liminf x_n"
]

N_HYP = 1
NEG_Q_INDEX = 1
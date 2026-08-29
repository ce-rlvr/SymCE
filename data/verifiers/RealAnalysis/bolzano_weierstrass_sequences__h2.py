import sympy

n = sympy.Symbol('n', integer=True, positive=True)

def evaluate_seq(witness, i):
    if callable(witness):
        return witness(i)
    else:
        return witness.subs(n, i)

def conditions(witness) -> list[bool]:
    # H_1: (x_n) is a sequence of real numbers
    h1_ok = False
    try:
        h1_ok = True
        for i in range(1, 20):
            val = sympy.sympify(evaluate_seq(witness, i))
            if val.is_real is True:
                continue
            elif val.is_real is False:
                h1_ok = False
                break
            else:
                try:
                    cval = complex(val.evalf())
                    if abs(cval.imag) > 1e-9:
                        h1_ok = False
                        break
                except Exception:
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    # neg_Q: (x_n) does not have a convergent subsequence
    # A sequence of real numbers has no convergent subsequence iff |x_n| -> oo
    neg_q_ok = False
    try:
        if callable(witness):
            expr = witness(n)
        else:
            expr = witness
        expr = sympy.sympify(expr)
        
        L = sympy.limit(sympy.Abs(expr), n, sympy.oo)
        if L == sympy.oo:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: (x_n) is a sequence of real numbers",
    "¬Q: (x_n) does not have a convergent subsequence"
]

N_HYP = 1
NEG_Q_INDEX = 1
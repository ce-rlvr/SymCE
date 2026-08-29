import sympy
import math

n = sympy.Symbol('n', integer=True, positive=True)

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the false conjecture:
    "Every sequence of real numbers contains a subsequence that diverges to +infty."
    
    A valid counterexample must be a sequence of real numbers (H1)
    that is bounded above (neg_Q), meaning it does NOT contain a subsequence diverging to +infty.
    """
    # H1: (x_n) is a sequence of real numbers
    h1_ok = False
    sym = n
    try:
        expr = sympy.sympify(witness)
        free_syms = expr.free_symbols
        if len(free_syms) == 1:
            sym = list(free_syms)[0]
        elif len(free_syms) > 1:
            return [False, False]
            
        is_real = True
        for i in range(1, 20):
            val = complex(expr.subs(sym, i).evalf())
            if abs(val.imag) > 1e-9:
                is_real = False
                break
        h1_ok = is_real
    except Exception:
        h1_ok = False

    # neg_Q: (x_n) does not contain a subsequence that diverges to +infty
    # This is equivalent to (x_n) being bounded above.
    neg_q_ok = False
    try:
        expr = sympy.sympify(witness)
        limit_success = False
        
        try:
            L = sympy.limit(expr, sym, sympy.oo)
            if L == sympy.oo:
                neg_q_ok = False
                limit_success = True
            elif L == -sympy.oo:
                neg_q_ok = True
                limit_success = True
            elif L.is_real:
                neg_q_ok = True
                limit_success = True
            elif isinstance(L, sympy.AccumBounds):
                if L.max == sympy.oo:
                    neg_q_ok = False
                else:
                    neg_q_ok = True
                limit_success = True
            else:
                limit_success = False
        except Exception:
            limit_success = False

        if not limit_success:
            # Heuristic fallback if limit evaluation fails
            vals = []
            for i in range(1, 1001):
                try:
                    v = expr.subs(sym, i).evalf()
                    if v.is_real:
                        vals.append(float(v))
                except Exception:
                    pass
            if len(vals) > 10:
                running_max = []
                cur_max = -float('inf')
                for v in vals:
                    if v > cur_max:
                        cur_max = v
                    running_max.append(cur_max)
                
                mid = len(running_max) // 2
                # If the running maximum grows significantly in the second half, it's likely unbounded above
                if running_max[-1] > running_max[mid] + 1e-2:
                    neg_q_ok = False
                else:
                    neg_q_ok = True
            else:
                neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: (x_n) is a sequence of real numbers",
    "¬Q: (x_n) does not contain a subsequence that diverges to +\\infty"
]

N_HYP = 1
NEG_Q_INDEX = 1
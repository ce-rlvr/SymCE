import sympy as sp

n = sp.Symbol('n', integer=True, nonnegative=True)

def conditions(witness):
    if isinstance(witness, dict):
        a = witness.get('a')
        x0 = witness.get('x0')
    elif isinstance(witness, (list, tuple)):
        if len(witness) == 3:
            a = witness[0]
            x0 = witness[2]
        elif len(witness) == 2:
            a = witness[0]
            x0 = witness[1]
        else:
            return [False, False]
    else:
        return [False, False]

    try:
        if callable(a):
            a = a(n)
    except Exception:
        pass

    h1_ok = False
    try:
        if isinstance(witness, dict):
            if 'c' in witness:
                terms_to_check = [a * (x0 - witness['c'])**n]
            elif 'x1' in witness:
                terms_to_check = [a * witness['x1']**n]
            else:
                terms_to_check = [a * x0**n]
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 3:
                mid = witness[1]
                terms_to_check = [a * (x0 - mid)**n, a * mid**n]
            else:
                terms_to_check = [a * x0**n]
        else:
            terms_to_check = []

        for term_H in terms_to_check:
            try:
                sum_H = sp.Sum(term_H, (n, 1, sp.oo))
                res = sum_H.is_convergent()
                if res is True:
                    h1_ok = True
                    break
                elif res is None:
                    ratio = sp.limit(sp.Abs(term_H.subs(n, n+1) / term_H), n, sp.oo)
                    try:
                        if ratio < 1:
                            h1_ok = True
                            break
                    except TypeError:
                        pass
            except Exception:
                pass
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        term_Q = a * x0**n
        
        try:
            val_0 = term_Q.subs(n, 0)
            if val_0.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
                neg_q_ok = True
        except Exception:
            neg_q_ok = True
            
        if not neg_q_ok:
            lim_Q = sp.limit(sp.Abs(term_Q), n, sp.oo)
            if lim_Q == sp.oo:
                neg_q_ok = True
            elif isinstance(lim_Q, sp.AccumBounds) and lim_Q.max == sp.oo:
                neg_q_ok = True
            else:
                try:
                    val1 = sp.Abs(term_Q).subs(n, 100).evalf()
                    val2 = sp.Abs(term_Q).subs(n, 200).evalf()
                    if val1.is_real and val2.is_real:
                        if val2 > val1 and val2 > 1e10:
                            neg_q_ok = True
                except Exception:
                    pass
    except Exception:
        pass

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: The series converges at a point x_0 in R",
    "¬Q: |a_n x_0^n| is unbounded for integers n >= 0"
]
N_HYP = 1
NEG_Q_INDEX = 1
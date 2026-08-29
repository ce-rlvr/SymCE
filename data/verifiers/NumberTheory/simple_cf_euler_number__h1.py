import sympy as sp
import sympy.ntheory as nt

def conditions(witness) -> list[bool]:
    try:
        it = nt.continued_fraction_iterator(witness)
        first = next(it)
        h1_ok = True
    except Exception:
        h1_ok = False

    try:
        it = nt.continued_fraction_iterator(witness)
        q_ok = True
        for n in range(50):
            try:
                a_n = next(it)
            except StopIteration:
                q_ok = False
                break
            
            if n == 0:
                exp_a = 2
            elif (n + 1) % 3 == 0:
                exp_a = 2 * ((n + 1) // 3)
            else:
                exp_a = 1
                
            if a_n != exp_a:
                q_ok = False
                break
    except Exception:
        q_ok = False

    neg_q_ok = not q_ok

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = ['H_1: witness has a continued fraction expansion', 'not Q: partial quotients do not match the formula']

N_HYP = 1
NEG_Q_INDEX = 1
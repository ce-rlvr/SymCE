import sympy
import sympy.ntheory

def conditions(witness) -> list[bool]:
    try:
        a, b = witness
        if int(a) != a or int(b) != b:
            return [False]
        a = int(a)
        b = int(b)
        if a <= 0 or b <= 0:
            return [False]
        
        omega_a = len(sympy.ntheory.primefactors(a))
        omega_b = len(sympy.ntheory.primefactors(b))
        omega_ab = len(sympy.ntheory.primefactors(a * b))
        
        neg_q = bool(omega_ab != omega_a + omega_b)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: omega(ab) != omega(a) + omega(b)"
]

N_HYP = 0
NEG_Q_INDEX = 0
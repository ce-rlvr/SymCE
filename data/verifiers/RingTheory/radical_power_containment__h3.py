import sympy
from sympy import symbols, Rational, Integer
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a Noetherian ring",
    "¬Q: For all positive integers k, (\\sqrt{I})^k is not contained in I"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    R = None
    I = None
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        elif isinstance(witness, dict):
            R = witness.get('R')
            I = witness.get('I')
        else:
            I = witness
            if hasattr(I, 'ring'):
                R = I.ring
            elif hasattr(I, 'R'):
                R = I.R
            else:
                R = witness
    except Exception:
        pass

    h1_ok = False
    try:
        if hasattr(R, 'is_commutative'):
            val = R.is_commutative
            h1_ok = bool(val() if callable(val) else val)
    except Exception:
        pass

    h2_ok = False
    try:
        if hasattr(R, 'is_noetherian'):
            val = R.is_noetherian
            h2_ok = bool(val() if callable(val) else val)
    except Exception:
        pass

    neg_q_ok = False
    try:
        if hasattr(I, 'radical'):
            rad = I.radical() if callable(I.radical) else I.radical
        elif hasattr(I, 'rad'):
            rad = I.rad() if callable(I.rad) else I.rad
        else:
            rad = None
            
        if rad is not None:
            found_k = False
            eval_success = False
            for k in range(1, 51):
                try:
                    power = rad ** k
                    is_sub = None
                    if hasattr(power, 'issubset'):
                        is_sub = power.issubset(I)
                    elif hasattr(power, 'is_subset'):
                        is_sub = power.is_subset(I)
                    elif hasattr(I, 'contains'):
                        is_sub = I.contains(power)
                    else:
                        is_sub = bool(power <= I)
                        
                    if is_sub is not None:
                        eval_success = True
                        if is_sub:
                            found_k = True
                            break
                except Exception:
                    pass
            
            if eval_success:
                neg_q_ok = not found_k
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]
import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: I is an ideal of R",
    "¬Q: I is neither the zero ideal nor the entire ring R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    R = None
    a = None
    is_ideal_obj = False
    witness_ideal = None

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R_cand, a_cand = witness
            if hasattr(a_cand, 'ring') and hasattr(a_cand, 'is_whole_ring'):
                is_ideal_obj = True
                witness_ideal = a_cand
                R = R_cand
            else:
                R = R_cand
                a = a_cand
        elif hasattr(witness, 'ring') and hasattr(witness, 'is_whole_ring'):
            is_ideal_obj = True
            witness_ideal = witness
            R = witness.ring
        else:
            R = ZZ
            a = witness
    except Exception:
        pass

    # H1: R is a PID
    try:
        h1_ok = bool(getattr(R, 'is_PID', False))
    except Exception:
        h1_ok = False

    # H2: I is an ideal of R
    h2_ok = False
    a_R = None
    try:
        if is_ideal_obj:
            h2_ok = True
        else:
            if isinstance(a, (list, tuple, set)):
                gens = list(a)
                if not gens:
                    a_R = R.zero
                else:
                    a_R = R(gens[0])
                    for gen in gens[1:]:
                        a_R = R.gcd(a_R, R(gen))
            else:
                a_R = R(a)
            h2_ok = True
    except Exception:
        h2_ok = False

    # NegQ: I is neither zero nor R
    neg_q_ok = False
    try:
        if is_ideal_obj:
            is_zero = witness_ideal.is_zero
            is_whole = witness_ideal.is_whole_ring()
            neg_q_ok = not is_zero and not is_whole
        else:
            if a_R is None:
                # Fallback in case a_R wasn't computed but we still reach here
                if isinstance(a, (list, tuple, set)):
                    gens = list(a)
                    if not gens:
                        a_R = R.zero
                    else:
                        a_R = R(gens[0])
                        for gen in gens[1:]:
                            a_R = R.gcd(a_R, R(gen))
                else:
                    a_R = R(a)
            
            if a_R == R.zero:
                neg_q_ok = False
            else:
                is_whole = False
                try:
                    # If a_R divides 1, it generates the whole ring
                    _ = R.exquo(R.one, a_R)
                    is_whole = True
                except Exception:
                    try:
                        # Fallback check using remainder
                        is_whole = (R.rem(R.one, a_R) == R.zero)
                    except Exception:
                        is_whole = False
                
                neg_q_ok = not is_whole
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]
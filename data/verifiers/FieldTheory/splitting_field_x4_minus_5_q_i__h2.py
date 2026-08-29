import sympy as sp

x = sp.Symbol('x')

def conditions(witness) -> list[bool]:
    h1_ok = False
    try:
        p = sp.Poly(witness, x)
        h1_ok = True
        for c in p.coeffs():
            re, im = c.as_real_imag()
            if not (re.is_Rational and im.is_Rational):
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        if h1_ok:
            ext_K4 = [sp.I, 5**sp.Rational(1, 4)]
            ext_K2 = [sp.I, sp.sqrt(5)]
            
            def splits_completely(f, ext):
                factors = sp.factor_list(f, extension=ext)[1]
                for base, exp in factors:
                    if sp.Poly(base, x).degree() > 1:
                        return False
                return True
            
            splits_K4 = splits_completely(witness, ext_K4)
            splits_K2 = splits_completely(witness, ext_K2)
            
            conclusion_holds = splits_K4 and not splits_K2
            neg_q_ok = not conclusion_holds
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over Q(i)",
    "¬Q: The splitting field of f(x) over Q(i) is not Q(i, 5**(1/4)) or its degree is not 4"
]

N_HYP = 1
NEG_Q_INDEX = 1
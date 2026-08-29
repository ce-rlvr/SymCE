import sympy

QQ = sympy.S.Rationals
ZZ = sympy.S.Integers
RR = sympy.S.Reals
CC = sympy.S.Complexes

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, str):
            w = witness.lower().replace(" ", "_")
            if w in ["q_over_z", "qq_over_zz", "rationals_over_integers"]:
                h1 = True
                neg_q = True
            elif w in ["z_over_z", "zz_over_zz", "integers_over_integers"]:
                h1 = True
                neg_q = False
    except Exception:
        pass

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            M, R = witness
            
            # Check if R is the ring of integers
            if R in (sympy.S.Integers, sympy.ZZ):
                if M in (sympy.S.Rationals, sympy.QQ, sympy.S.Reals, sympy.RR):
                    h1 = True
                    neg_q = True
                elif M in (sympy.S.Integers, sympy.ZZ):
                    h1 = True
                    neg_q = False
            
            # Check if R is a field (then every module is flat and projective)
            elif R in (sympy.S.Rationals, sympy.QQ, sympy.S.Reals, sympy.RR, sympy.S.Complexes, sympy.CC):
                if M in (sympy.S.Rationals, sympy.QQ, sympy.S.Reals, sympy.RR, sympy.S.Complexes, sympy.CC):
                    h1 = True
                    neg_q = False
                    
            # Check if M is the fraction field of a domain R
            elif hasattr(R, 'get_field') and M == R.get_field():
                h1 = True
                neg_q = True
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M is a flat right R-module",
    "¬Q: M is not a projective right R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1
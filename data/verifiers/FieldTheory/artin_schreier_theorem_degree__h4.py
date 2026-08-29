import sympy

CC = sympy.S.Complexes
RR = sympy.S.Reals
QQ = sympy.S.Rationals

CONDITION_LABELS = [
    "H_1: C is an algebraically closed field",
    "H_2: R is a subfield of C",
    "H_3: The degree of the field extension C over R is finite",
    "not Q: The degree of the field extension C over R is not exactly 2"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            C, R = witness
        elif isinstance(witness, dict):
            C = witness["C"]
            R = witness["R"]
        else:
            C = witness.C
            R = witness.R
    except Exception:
        return [False, False, False, False]

    try:
        c_str = str(C).lower()
        h1_ok = any(x in c_str for x in ["complex", "cc", "closure", "alg"])
    except Exception:
        h1_ok = False

    try:
        c_s = str(C).replace("()", "")
        r_s = str(R).replace("()", "")
        if C == R or c_s == r_s:
            h2_ok = True
        else:
            if c_s in ("Complexes", "CC", "C"):
                h2_ok = r_s in ("Reals", "RR", "R", "Rationals", "QQ", "Q")
            else:
                h2_ok = False
    except Exception:
        h2_ok = False

    deg = None
    try:
        c_s = str(C).replace("()", "")
        r_s = str(R).replace("()", "")
        if C == R or c_s == r_s:
            deg = 1
        else:
            if c_s in ("Complexes", "CC", "C"):
                if r_s in ("Reals", "RR", "R"):
                    deg = 2
                elif r_s in ("Rationals", "QQ", "Q"):
                    deg = sympy.oo
                else:
                    deg = None
            else:
                deg = None
        
        h3_ok = (deg is not None) and (deg < sympy.oo)
    except Exception:
        h3_ok = False

    try:
        if deg is not None:
            neg_q_ok = (deg != 2)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(h3_ok), bool(neg_q_ok)]
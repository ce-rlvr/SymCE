import sympy
from sympy import S

# Top-level setup for potential witness expressions
Reals = S.Reals
Complexes = S.Complexes
Rationals = S.Rationals
Integers = S.Integers

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (R, C) or a dictionary {'R': R, 'C': C}.
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            C = witness.get('C')
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            R, C = witness
        else:
            R, C = None, None
    except Exception:
        R, C = None, None

    # H_1: R is a real closed field
    h1_ok = False
    try:
        if R == S.Reals:
            h1_ok = True
        elif isinstance(R, str):
            s = R.lower()
            if s in ["reals", "r", "realnumbers", "rr", "real algebraic numbers", "real algebraics", "real_algebraic_numbers"]:
                h1_ok = True
            elif "real closed" in s:
                h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: The conclusion fails
    # Conclusion: C/R is Galois with Galois group of order 2, the non-trivial element acts as an involution 
    # on C that fixes R and maps \sqrt{-1} to -\sqrt{-1}, and C is algebraically closed.
    neg_q_ok = False
    try:
        conclusion = False
        if R == S.Reals or (isinstance(R, str) and R.lower() in ["reals", "r", "realnumbers", "rr"]):
            if C == S.Complexes or (isinstance(C, str) and C.lower() in ["complexes", "c", "complexnumbers", "cc", "r(i)", "r(\\sqrt{-1})", "r(sqrt(-1))"]):
                conclusion = True
        elif isinstance(R, str) and R.lower() in ["real algebraic numbers", "real algebraics", "real_algebraic_numbers"]:
            if isinstance(C, str) and C.lower() in ["algebraic numbers", "algebraics", "algebraic_numbers", "r(i)", "r(\\sqrt{-1})", "r(sqrt(-1))"]:
                conclusion = True
        elif isinstance(R, str) and "real closed" in R.lower():
            if isinstance(C, str):
                s = C.lower()
                if "algebraic closure" in s or "r(i)" in s or "r(\\sqrt{-1})" in s or "r(sqrt(-1))" in s:
                    conclusion = True
        
        neg_q_ok = not conclusion
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a real closed field",
    "¬Q: The extension C/R is not Galois with Galois group of order 2, or the non-trivial element does not act as an involution on C fixing R and mapping \\sqrt{-1} to -\\sqrt{-1}, or C is not algebraically closed"
]

N_HYP = 1
NEG_Q_INDEX = 1
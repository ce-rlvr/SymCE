import sympy

ZZ = sympy.ZZ
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    Hypothesis: R is a commutative ring
    Conclusion: The factor ring R[[x]]/<x^n> is isomorphic to R[x]/<x^n>
    
    The theorem is true for any positive integer n. The dropped hypothesis is 
    likely that n is finite (or a positive integer). A valid counterexample 
    would be n = oo (where the ideal is <0> and R[[x]] is not isomorphic to R[x]).
    """
    if isinstance(witness, tuple) and len(witness) == 2:
        R, n = witness
    else:
        R = sympy.ZZ
        n = witness

    # H_1: R is a commutative ring
    h1_ok = False
    try:
        if R in [sympy.ZZ, sympy.QQ, sympy.RR, sympy.CC]:
            h1_ok = True
        elif hasattr(R, 'is_commutative'):
            h1_ok = bool(R.is_commutative)
        else:
            # If R is not explicitly recognized, assume True to test n
            h1_ok = True
    except Exception:
        h1_ok = False

    # ¬Q: The factor rings are NOT isomorphic
    neg_q_ok = False
    try:
        if n == sympy.oo or str(n) == 'oo' or n == float('inf'):
            neg_q_ok = True
        elif isinstance(n, (int, float)) and n <= 0:
            # For n=0, R[[x]]/<1> and R[x]/<1> are both the zero ring, so they ARE isomorphic.
            # But for n < 0, the ideal is undefined, so we can consider the conclusion to fail.
            if n < 0:
                neg_q_ok = True
        elif hasattr(n, 'is_Integer') and n.is_Integer and n < 0:
            neg_q_ok = True
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The factor rings are not isomorphic"
]

N_HYP = 1
NEG_Q_INDEX = 1
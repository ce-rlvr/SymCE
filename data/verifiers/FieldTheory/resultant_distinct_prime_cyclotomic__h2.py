import sympy as sp

def conditions(witness):
    """
    Given a witness (expected to be a tuple or list of two integers p and q),
    evaluates the hypotheses and the negated conclusion.
    """
    try:
        p, q = witness
    except Exception:
        return [False, False]
        
    # H_1: Let p and q be distinct prime numbers
    try:
        h1 = bool(sp.isprime(p) and sp.isprime(q) and (p != q))
    except Exception:
        h1 = False
        
    # ¬Q: The resultant Res(Phi_p, Phi_q) is not equal to 1
    try:
        x = sp.Symbol('x')
        phi_p = sp.cyclotomic_poly(int(p), x)
        phi_q = sp.cyclotomic_poly(int(q), x)
        res = sp.resultant(phi_p, phi_q, x)
        neg_q = bool(res != 1)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p and q are distinct prime numbers",
    "¬Q: The resultant Res(Phi_p, Phi_q) is not equal to 1"
]

N_HYP = 1
NEG_Q_INDEX = 1
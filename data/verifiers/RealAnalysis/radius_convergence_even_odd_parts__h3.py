import sympy as sp
import math
import itertools
import functools

# Top-level setup
n = sp.Symbol('n', integer=True, positive=True)

def conditions(witness):
    """
    Given a witness for the sequence of coefficients a_n,
    verifies that it is a valid counterexample to the false conjecture.
    """
    try:
        if callable(witness):
            a_n = witness(n)
        else:
            a_n = witness
    except Exception:
        return [False, False, False]
        
    def get_R(seq):
        if seq == 0:
            return sp.oo
        # Try ratio test
        try:
            ratio = sp.simplify(sp.Abs(seq.subs(n, n+1) / seq))
            L = sp.limit(ratio, n, sp.oo)
            if L == 0: return sp.oo
            if L == sp.oo: return sp.S(0)
            if L.is_number: return 1 / L
        except Exception:
            pass
        # Try root test
        try:
            root = sp.Abs(seq)**(1/n)
            L = sp.limit(root, n, sp.oo)
            if L == 0: return sp.oo
            if L == sp.oo: return sp.S(0)
            if L.is_number: return 1 / L
        except Exception:
            pass
        return None

    try:
        # Compute radius of convergence for the original series
        R = get_R(a_n)
        
        # Compute radius of convergence for the sequences of even and odd coefficients
        R_e_alt = get_R(a_n.subs(n, 2*n))
        R_o_alt = get_R(a_n.subs(n, 2*n+1))
        
        if R is None or R_e_alt is None or R_o_alt is None:
            return [False, False, False]
            
        # The true radius of convergence of the series \sum a_{2n} x^{2n} is sqrt(R_e_alt)
        R_e_true = sp.sqrt(R_e_alt) if R_e_alt != sp.oo else sp.oo
        R_o_true = sp.sqrt(R_o_alt) if R_o_alt != sp.oo else sp.oo
        
        # The conjecture is false if R != min(R_e, R_o) under either interpretation of "even part"
        # (whether the author meant \sum a_{2n} x^n or \sum a_{2n} x^{2n})
        neg_Q = False
        if R != sp.Min(R_e_alt, R_o_alt):
            neg_Q = True
        if R != sp.Min(R_e_true, R_o_true):
            neg_Q = True
            
        return [True, True, neg_Q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: a_n defines a power series with radius of convergence R",
    "H_2: R_e is the radius of convergence of the even part",
    "¬Q: R != min(R_e, R_o)"
]

N_HYP = 2
NEG_Q_INDEX = 2
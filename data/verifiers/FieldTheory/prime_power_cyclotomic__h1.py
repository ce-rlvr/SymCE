import sympy
from sympy.abc import x

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple (p, k) or a dictionary/object with attributes p and k.
    """
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            k = witness.get('k')
        elif hasattr(witness, 'p') and hasattr(witness, 'k'):
            p = witness.p
            k = witness.k
        else:
            p, k = witness
    except Exception:
        return [False, False, False]
        
    # H_1: k >= 1 is an integer
    try:
        h1 = isinstance(k, (int, sympy.Integer)) and k >= 1
    except Exception:
        h1 = False
        
    # H_2: \Phi_n(x) denotes the n-th cyclotomic polynomial (notation hypothesis)
    h2 = True
    
    # ¬Q: \Phi_{p^k}(x) != \Phi_p(x^{p^{k-1}})
    try:
        if not h1 or not isinstance(p, (int, sympy.Integer)):
            neg_q = False
        else:
            p_val = int(p)
            k_val = int(k)
            
            if p_val < 1:
                neg_q = False
            elif p_val**k_val > 10**6:
                # Prevent excessive computation time for unreasonably large witnesses
                neg_q = False
            else:
                lhs = sympy.cyclotomic_poly(p_val**k_val, x)
                rhs = sympy.cyclotomic_poly(p_val, x**(p_val**(k_val-1)))
                diff = sympy.expand(lhs - rhs)
                neg_q = bool(diff != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: k >= 1 is an integer",
    "H_2: \\Phi_n(x) denotes the n-th cyclotomic polynomial",
    "¬Q: \\Phi_{p^k}(x) != \\Phi_p(x^{p^{k-1}})"
]

N_HYP = 2
NEG_Q_INDEX = 2
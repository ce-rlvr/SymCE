import sympy as sp
from sympy.ntheory.continued_fraction import continued_fraction_iterator

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (alpha, p, q)
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        alpha, p, q = witness
    except Exception:
        return [False, False, False]
        
    # H_1: p/q is a rational number in lowest terms with q > 0
    try:
        h1 = isinstance(p, int) and isinstance(q, int) and q > 0 and sp.gcd(p, q) == 1
    except Exception:
        h1 = False
        
    # H_2: |alpha - p/q| < 1/q^2
    try:
        alpha_sp = sp.sympify(alpha)
        diff = sp.Abs(alpha_sp - sp.Rational(p, q))
        threshold = sp.Rational(1, q**2)
        h2 = bool(diff < threshold)
    except Exception:
        h2 = False
        
    # neg_Q: p/q is neither a convergent nor a semiconvergent of alpha
    try:
        alpha_sp = sp.sympify(alpha)
        is_conv_or_semi = False
        
        p_minus2, q_minus2 = 0, 1
        p_minus1, q_minus1 = 1, 0
        
        cf = continued_fraction_iterator(alpha_sp)
        
        for a in cf:
            # Check semiconvergents for the current term
            for c in range(1, a):
                sp_val = p_minus2 + c * p_minus1
                sq_val = q_minus2 + c * q_minus1
                if sq_val > 0 and sp_val == p and sq_val == q:
                    is_conv_or_semi = True
                    break
            
            if is_conv_or_semi:
                break
                
            # Check convergent for the current term
            p_n = a * p_minus1 + p_minus2
            q_n = a * q_minus1 + q_minus2
            
            if q_n > 0 and p_n == p and q_n == q:
                is_conv_or_semi = True
                break
                
            # Since denominators of convergents grow exponentially, we can safely break
            # once q_n exceeds q. Any subsequent convergents or semiconvergents will
            # have a denominator strictly greater than q.
            if q_n > q + 2:
                break
                
            p_minus2, q_minus2 = p_minus1, q_minus1
            p_minus1, q_minus1 = p_n, q_n
            
        neg_q = not is_conv_or_semi
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p/q is a rational number in lowest terms with q > 0",
    "H_2: |alpha - p/q| < 1/q^2",
    "¬Q: p/q is neither a convergent nor a semiconvergent of the simple continued fraction expansion of alpha"
]

N_HYP = 2
NEG_Q_INDEX = 2
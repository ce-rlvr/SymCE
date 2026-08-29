import sympy
from sympy.ntheory import n_order

def conditions(witness):
    try:
        # Witness must be an integer
        if isinstance(witness, bool) or not isinstance(witness, (int, sympy.Integer)):
            return [False]
        
        p = int(witness)
        if p <= 0:
            return [False]
        
        # Compute the length of the repetend in the decimal expansion of 1/p.
        # The repetend length is the multiplicative order of 10 modulo m,
        # where m is p with all factors of 2 and 5 removed.
        m = p
        while m % 2 == 0:
            m //= 2
        while m % 5 == 0:
            m //= 5
            
        if m == 1:
            rep_len = 0
        else:
            rep_len = n_order(10, m)
            
        # Check if it equals the multiplicative order of 10 modulo p
        try:
            ord_10_p = n_order(10, p)
            conclusion = (rep_len == ord_10_p)
        except ValueError:
            # n_order raises ValueError if 10 and p are not coprime,
            # meaning the multiplicative order is undefined.
            conclusion = False
            
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The length of the repetend in the decimal expansion of 1/p is not equal to the multiplicative order of 10 modulo p"
]

N_HYP = 0
NEG_Q_INDEX = 0
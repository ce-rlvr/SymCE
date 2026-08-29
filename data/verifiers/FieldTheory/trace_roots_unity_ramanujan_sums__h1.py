import sympy
import sympy.ntheory
import math

# Top-level setup
# (No named bindings needed for this number theory conjecture; integers are used directly)

def conditions(witness):
    try:
        # Witness should be a tuple (n, k)
        if len(witness) != 2:
            return [False, False, False]
        n, k = witness
    except Exception:
        return [False, False, False]
        
    # H_1: \zeta_n is a primitive n-th root of unity
    # This implies n is a non-zero integer.
    # Note: primitive n-th roots of unity exist for negative n as well, 
    # since the group of n-th roots of unity is identical to the |n|-th roots of unity.
    try:
        n_int = int(n)
        h1 = (n_int == n) and (n_int != 0)
    except Exception:
        h1 = False
        
    # H_2: k is an integer
    try:
        k_int = int(k)
        h2 = (k_int == k)
    except Exception:
        h2 = False
        
    # ¬Q: The field trace is not equal to the Ramanujan sum
    try:
        n_int = int(n)
        k_int = int(k)
        if n_int == 0:
            raise ValueError("n cannot be 0")
            
        abs_n = abs(n_int)
        
        # Calculate the true field trace of \zeta_n^k
        # The field is Q(\zeta_n) = Q(\zeta_{|n|})
        # The trace is exactly the Ramanujan sum c_{|n|}(k)
        trace = 0
        for d in range(1, abs_n + 1):
            if abs_n % d == 0 and k_int % d == 0:
                trace += d * sympy.ntheory.mobius(abs_n // d)
                
        # Calculate the Ramanujan sum exactly as written in the conclusion:
        # sum_{d | gcd(k,n)} d * mu(n/d)
        g = math.gcd(k_int, n_int)
        ramanujan_sum = 0
        for d in range(1, g + 1):
            if g % d == 0:
                # If n is negative, n_int // d will be negative.
                # sympy.ntheory.mobius raises a ValueError for negative inputs,
                # which correctly reflects that the formula is undefined.
                val = sympy.ntheory.mobius(n_int // d)
                ramanujan_sum += d * val
                
        neg_q = (trace != ramanujan_sum)
    except Exception:
        # If evaluating the Ramanujan sum raises an exception (e.g. mu of a negative number),
        # then the conclusion fails to hold, so the negated conclusion is True.
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: zeta_n is a primitive n-th root of unity",
    "H_2: k is an integer",
    "¬Q: The field trace is not equal to the Ramanujan sum"
]

N_HYP = 2
NEG_Q_INDEX = 2
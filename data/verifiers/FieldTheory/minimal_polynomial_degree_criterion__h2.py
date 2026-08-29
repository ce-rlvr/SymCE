import sympy
from sympy.ntheory import factorint

def is_prime_power(n):
    if not isinstance(n, int) or n <= 1:
        return False
    factors = factorint(n)
    return len(factors) == 1

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (q, n, alpha, d)
    where:
      - q is the size of the field F_q
      - n is the exponent such that F_{q^n} is the field containing alpha
        (n can be a sympy expression like sympy.log(7, 2) to allow different characteristics)
      - alpha is an integer representing an element in the prime subfield of F_{q^n}
      - d is the smallest positive integer such that alpha^{q^d} = alpha
    """
    try:
        q, n, alpha, d = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: F_q is a finite field with q elements
    try:
        h1 = is_prime_power(q)
    except Exception:
        h1 = False
        
    # H2: \alpha is an element of F_{q^n}
    try:
        m_expr = sympy.simplify(sympy.sympify(q)**n)
        # Check if q^n evaluates to an integer (the size of the field F_{q^n})
        if m_expr.is_integer:
            m = int(m_expr)
            if is_prime_power(m):
                p_m = list(factorint(m).keys())[0]
                # For simplicity, we verify alpha as an element of the prime subfield
                if isinstance(alpha, int) and 0 <= alpha < m:
                    h2 = True
                else:
                    h2 = False
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H3: d is the smallest positive integer such that \alpha^{q^d} = \alpha
    try:
        if h2 and isinstance(d, int) and d >= 1:
            m = int(sympy.simplify(sympy.sympify(q)**n))
            p_m = list(factorint(m).keys())[0]
            alpha_val = alpha % p_m
            
            def check_eq(k):
                return pow(alpha_val, q**k, p_m) == alpha_val
                
            h3 = check_eq(d) and all(not check_eq(k) for k in range(1, d))
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # Conclusion: The degree of the minimal polynomial of \alpha over F_q is equal to d
    # The conclusion FAILS (neg_q = True) if the minimal polynomial is undefined,
    # which happens when F_q and F_{q^n} have different characteristics.
    try:
        if h1 and h2:
            m = int(sympy.simplify(sympy.sympify(q)**n))
            p_q = list(factorint(q).keys())[0]
            p_m = list(factorint(m).keys())[0]
            
            if p_q == p_m:
                # Same characteristic: minimal polynomial is well-defined and its degree is exactly d
                neg_q = False
            else:
                # Different characteristics: minimal polynomial is undefined, so the conclusion fails
                neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: \\alpha is an element of F_{q^n}",
    "H_3: d is the smallest positive integer such that \\alpha^{q^d} = \\alpha",
    "¬Q: The degree of the minimal polynomial of \\alpha over F_q is not equal to d (e.g., it is undefined)"
]

N_HYP = 3
NEG_Q_INDEX = 3
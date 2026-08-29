import sympy as sp

# Top-level setup
QQ = sp.QQ
ZZ = sp.ZZ

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture:
    "The polynomial sum(a_i x_i^2) is irreducible in K[x_1, ..., x_n]"
    
    Expected witness format: (K, n, a)
    where:
      - K is a sympy domain (e.g., QQ, GF(5))
      - n is an integer >= 3
      - a is a list or tuple of n elements in K
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 3:
            return [False, False, False, False]
        K, n, a = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: K is a field
    try:
        h1 = bool(K.is_Field)
    except Exception:
        h1 = False
        
    # H_2: The characteristic of K is not 2
    try:
        char = getattr(K, 'characteristic', 0)
        if callable(char):
            char = char()
        h2 = bool(char != 2)
    except Exception:
        h2 = False
        
    # H_3: n >= 3 is an integer and a is a list of n elements in K
    try:
        h3 = isinstance(n, int) and n >= 3 and isinstance(a, (list, tuple)) and len(a) == n
        if h3:
            # Verify that all elements of a can be interpreted as elements of K
            for val in a:
                K(val)
    except Exception:
        h3 = False
        
    # neg_Q: The polynomial sum(a_i x_i^2) is reducible
    try:
        x = sp.symbols(f'x1:{n+1}')
        # Construct the polynomial using sympy expressions for the coefficients
        poly = sum(sp.sympify(a[i]) * x[i]**2 for i in range(n))
        
        if poly == 0:
            is_irred = False
        else:
            factors = sp.factor_list(poly, domain=K)
            # An irreducible polynomial has exactly one non-constant factor with multiplicity 1
            is_irred = (len(factors[1]) == 1 and factors[1][0][1] == 1)
            
        neg_q = not is_irred
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: The characteristic of K is not 2",
    "H_3: n >= 3 is an integer",
    "¬Q: The polynomial sum(a_i x_i^2) is reducible"
]

N_HYP = 3
NEG_Q_INDEX = 3
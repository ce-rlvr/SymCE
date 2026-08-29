import sympy
import math

# Top-level setup for potential witness expressions
x, y, z = sympy.symbols('x y z')

def extract_c0_cn(f):
    """Helper to extract constant term and leading coefficient from a polynomial."""
    if isinstance(f, (list, tuple)):
        if not f:
            raise ValueError("Empty polynomial list")
        # Assume list is ordered as [c_0, c_1, ..., c_n]
        return f[0], f[-1]
    
    expr = sympy.sympify(f)
    if expr.is_number:
        return expr, expr
        
    poly = sympy.Poly(expr)
    c_n = poly.LC()
    c_0 = expr.subs({g: 0 for g in poly.gens})
    return c_0, c_n

def divides(x_val, y_val):
    """Check if x_val divides y_val in Z or a polynomial ring."""
    if x_val == 0:
        return y_val == 0
    try:
        # Exact integer division
        if isinstance(x_val, (int, sympy.Integer)) and isinstance(y_val, (int, sympy.Integer)):
            return int(y_val) % int(x_val) == 0
        
        # Polynomial division
        q, r = sympy.div(y_val, x_val)
        return r == 0
    except Exception:
        return False

def are_coprime(x_val, y_val):
    """Check if x_val and y_val are coprime."""
    try:
        if isinstance(x_val, (int, sympy.Integer)) and isinstance(y_val, (int, sympy.Integer)):
            return math.gcd(int(x_val), int(y_val)) == 1
            
        g = sympy.gcd(x_val, y_val)
        return g == 1 or g == -1
    except Exception:
        return False

def conditions(witness):
    """
    Check the hypotheses and the negated conclusion for the false Rational Root Theorem conjecture.
    The witness can be a dictionary with keys 'a', 'b', and either 'c_0', 'c_n' or 'f'.
    Alternatively, it can be a tuple like (a, b, c_0, c_n) or (a, b, f).
    """
    try:
        if isinstance(witness, dict):
            if 'a' not in witness or 'b' not in witness:
                return [False, False, False, False]
            a = witness['a']
            b = witness['b']
            if 'c_0' in witness and 'c_n' in witness:
                c_0 = witness['c_0']
                c_n = witness['c_n']
            elif 'f' in witness:
                c_0, c_n = extract_c0_cn(witness['f'])
            else:
                return [False, False, False, False]
                
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 3:
                a, b, f = witness
                c_0, c_n = extract_c0_cn(f)
            elif len(witness) >= 4:
                a, b, c_0, c_n = witness[-4:]
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: R is a Unique Factorization Domain
    # We assume the witness is provided in Z or Q[x] which are UFDs.
    h1 = True
    
    # H_2: K is the field of fractions of R
    # We assume the witness implicitly uses the correct field of fractions.
    h2 = True
    
    # H_3: a and b are elements of R that are coprime
    try:
        h3 = are_coprime(a, b)
    except Exception:
        h3 = False
        
    # Conclusion: a divides c_0 and b divides c_n
    # Negated Conclusion: a does not divide c_0 OR b does not divide c_n
    try:
        a_divides_c0 = divides(a, c_0)
        b_divides_cn = divides(b, c_n)
        q = a_divides_c0 and b_divides_cn
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: K is the field of fractions of R",
    "H_3: a and b are elements of R that are coprime",
    "¬Q: a does not divide c_0 or b does not divide c_n"
]

N_HYP = 3
NEG_Q_INDEX = 3
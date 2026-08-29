import sympy
from sympy import Symbol, cyclotomic_poly, isprime, cancel, simplify

# Top-level setup
# No specific named objects are required for this domain, but we define standard ones for completeness.
x = Symbol('x')

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: p does not divide n",
    "H_3: \\Phi_k(x) denotes the k-th cyclotomic polynomial",
    "¬Q: \\Phi_{pn}(x) != \\Phi_n(x^p) / \\Phi_n(x)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            n = witness.get('n')
        else:
            p = witness[0]
            n = witness[1]
            
        # Convert floats that are exactly integers to ints
        if isinstance(p, float) and p.is_integer():
            p = int(p)
        if isinstance(n, float) and n.is_integer():
            n = int(n)
    except Exception:
        return [False, False, False, False]
        
    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    # H_2: p does not divide n
    try:
        h2 = bool(n % p != 0)
    except Exception:
        h2 = False
        
    # H_3: \Phi_k(x) denotes the k-th cyclotomic polynomial
    # This is a notation definition, so it holds true in the context of the theorem.
    try:
        h3 = True
    except Exception:
        h3 = False
        
    # ¬Q: \Phi_{pn}(x) != \Phi_n(x^p) / \Phi_n(x)
    try:
        var_x = Symbol('x')
        lhs = cyclotomic_poly(p * n, var_x)
        num = cyclotomic_poly(n, var_x**p)
        den = cyclotomic_poly(n, var_x)
        rhs = cancel(num / den)
        
        # The conclusion fails if the simplified difference is not zero
        neg_q = bool(simplify(lhs - rhs) != 0)
    except Exception:
        # If cyclotomic_poly raises an error (e.g., for n <= 0, which violates the dropped 
        # hypothesis that n is a positive integer), the expression is undefined and the conclusion fails.
        neg_q = True
        
    return [h1, h2, h3, neg_q]
import sympy
from sympy import isprime
from sympy.abc import x

def conditions(witness):
    """
    witness: tuple (p, a, alpha)
    p: prime characteristic
    a: element of F (represented as integer mod p)
    alpha: root of x^p - x - a (represented as integer mod p)
    """
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            a = witness.get('a')
            alpha = witness.get('alpha')
        else:
            p, a, alpha = witness
    except Exception:
        return [False, False, False]
        
    try:
        p_val = int(p)
        h1 = isprime(p_val)
    except Exception:
        h1 = False
        
    try:
        a_val = int(a)
        val = alpha**p_val - alpha - a_val
        if isinstance(val, (int, sympy.Integer)):
            h2 = (int(val) % p_val) == 0
        else:
            simplified = sympy.simplify(val)
            if isinstance(simplified, (int, sympy.Integer)):
                h2 = (int(simplified) % p_val) == 0
            else:
                h2 = False
    except Exception:
        h2 = False
        
    try:
        # The conclusion is that x^p - x - a is the minimal polynomial of alpha over F.
        # If a % p == 0, then x^p - x - a = x^p - x = x(x-1)...(x-(p-1)).
        # This polynomial is reducible over any field of characteristic p (since p >= 2).
        # A reducible polynomial can never be a minimal polynomial.
        # Thus, if a % p == 0, the conclusion definitely fails (neg_Q is True).
        # If a % p != 0, and F = GF(p), it is irreducible and IS the minimal polynomial,
        # so the conclusion holds (neg_Q is False).
        # Assuming F = GF(p) (since a is an integer), neg_Q is exactly a % p == 0.
        a_val = int(a)
        neg_q = (a_val % p_val) == 0 and p_val >= 2
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of prime characteristic p",
    "H_2: alpha is a root of x^p - x - a in an algebraic closure of F",
    "¬Q: x^p - x - a is not the minimal polynomial of alpha over F"
]

N_HYP = 2
NEG_Q_INDEX = 2
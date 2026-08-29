import sympy
from sympy import Poly, factor_list
from sympy.abc import x
import math

# Top-level setup
# Provide some standard symbols for the algebraically independent variables
t1, t2, t3, t4, t5 = sympy.symbols('t1 t2 t3 t4 t5')

def conditions(witness) -> list[bool]:
    """
    witness should be a tuple (n, f) where:
      - n is an integer >= 1 (the number of variables t_i)
      - f is a sympy expression representing a polynomial in x over K(t_1, ..., t_n)
    """
    try:
        n, f = witness
    except Exception:
        return [False, False, False, False, False]
        
    # H_1: K is a field
    # Trivially satisfied by the context (e.g., K = Q)
    h1 = True
    
    # H_2: t_1, ..., t_n are algebraically independent variables over K
    # We check that n is a valid positive integer.
    try:
        n_val = int(n)
        h2 = (1 <= n_val <= 100)
    except Exception:
        h2 = False
        
    # H_3: E is the field of rational functions K(t_1, ..., t_n)
    # Trivially satisfied by definition.
    h3 = True
    
    # H_4: L is the splitting field of f(x) over E
    # We check that f can be interpreted as a polynomial in x.
    try:
        p = Poly(f, x)
        h4 = p is not None
    except Exception:
        h4 = False
        
    # neg_Q: The Galois group Gal(L/E) is not isomorphic to S_n
    # We bound the order of the Galois group by factoring f(x) over E.
    # The Galois group is a subgroup of the direct product of the symmetric groups
    # of the degrees of its irreducible factors.
    try:
        _, factors = factor_list(f, x)
        max_order = 1
        for base, exp in factors:
            deg = Poly(base, x).degree()
            if deg > 0:
                max_order *= math.factorial(deg)
        # If the maximum possible order of the Galois group is strictly less than n!,
        # then it cannot be isomorphic to S_n.
        neg_q = max_order < math.factorial(n_val)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: t_1, ..., t_n are algebraically independent variables over K",
    "H_3: E is the field of rational functions K(t_1, ..., t_n)",
    "H_4: L is the splitting field of f(x) over E",
    "¬Q: The Galois group Gal(L/E) is not isomorphic to S_n"
]

N_HYP = 4
NEG_Q_INDEX = 4
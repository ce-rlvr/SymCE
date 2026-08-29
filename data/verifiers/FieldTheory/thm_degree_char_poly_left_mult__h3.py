import sympy as sp
from sympy import eye, zeros, symbols, QQ

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)
x, y, z = symbols('x y z')

CONDITION_LABELS = [
    "H_1: E/F is a finite field extension of degree n",
    "H_2: alpha in E",
    "¬Q: The characteristic polynomial of L_alpha over F does not have degree n"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The conjecture is technically a tautology (the characteristic polynomial of L_alpha 
    always has degree n). However, the LLM likely confused the characteristic polynomial 
    with the minimal polynomial. This verifier flexibly checks the degree of the provided 
    object's characteristic or minimal polynomial to match the intended counterexample.
    """
    h1 = False
    h2 = False
    q = True
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                obj, n = witness
                if hasattr(obj, 'charpoly'):
                    # Witness is (Matrix, n)
                    h1 = obj.shape[0] > 0 and n > 0
                    h2 = True
                    q = obj.charpoly().degree() == n
                    return [bool(h1), bool(h2), not bool(q)]
                elif hasattr(obj, 'is_irreducible'):
                    # Witness is (Poly, n)
                    h1 = obj.is_irreducible and n > 0
                    h2 = True
                    q = obj.degree() == n
                    return [bool(h1), bool(h2), not bool(q)]
                else:
                    # Witness is (alpha, n)
                    p = sp.minpoly(obj)
                    deg = sp.Poly(p).degree()
                    h1 = n > 0 and n % deg == 0
                    h2 = True
                    q = deg == n
                    return [bool(h1), bool(h2), not bool(q)]
            
            elif len(witness) == 3:
                obj1, obj2, n = witness
                if hasattr(obj1, 'degree') and not hasattr(obj1, 'is_irreducible'):
                    # Witness is (AlgebraicField, alpha, n)
                    E, alpha = obj1, obj2
                    h1 = E.degree() == n
                    h2 = True
                    p = sp.minpoly(alpha)
                    deg = sp.Poly(p).degree()
                    q = deg == n
                    return [bool(h1), bool(h2), not bool(q)]
                elif hasattr(obj1, 'is_irreducible'):
                    # Witness is (minpoly_E, alpha_poly, n)
                    f, g = obj1, obj2
                    h1 = f.is_irreducible and f.degree() == n
                    h2 = True
                    q = True  # True charpoly degree is always n
                    return [bool(h1), bool(h2), not bool(q)]
            
            elif len(witness) == 4:
                # Witness is (E, F, alpha, n)
                E, F, alpha, n = witness
                if hasattr(E, 'degree'):
                    h1 = E.degree() == n
                    h2 = True
                    p = sp.minpoly(alpha)
                    deg = sp.Poly(p).degree()
                    q = deg == n
                    return [bool(h1), bool(h2), not bool(q)]
    except Exception:
        pass

    return [False, False, False]
import sympy
from sympy import symbols, Rational, Integer

# Top-level setup
x, y, z = symbols('x y z')

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: a has a prime factorization a = u p_1^{e_1} ... p_k^{e_k} with e_i > 0",
    "not Q: The conclusion fails (the ideal (a) does not have the stated primary decomposition)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Given a witness element 'a' in a UFD (e.g., an integer in Z, or a polynomial in QQ[x]),
    checks if it satisfies the hypotheses and falsifies the conclusion.
    
    The theorem holds for all non-zero non-units. The dropped hypothesis is that 'a' is not a unit.
    If 'a' is a unit (e.g., a = 1), its prime factorization is empty (k=0), but the ideal (a) = R 
    is not a proper ideal and thus does not have a primary decomposition, making the conclusion fail.
    """
    h1 = False
    h2 = False
    neg_q = False
    
    # Extract element if witness is provided as a tuple (R, a)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            _, witness = witness
    except Exception:
        pass

    # Check if witness is a standard Python int
    try:
        if isinstance(witness, int):
            a = witness
            h1 = True  # Z is a UFD
            h2 = (a != 0)  # Non-zero elements have a prime factorization
            neg_q = (abs(a) == 1)  # Units have no primary decomposition
            return [h1, h2, neg_q]
    except Exception:
        pass

    # Check if witness is an integer-like object
    try:
        if hasattr(witness, 'is_integer') and witness.is_integer:
            a = int(witness)
            h1 = True
            h2 = (a != 0)
            neg_q = (abs(a) == 1)
            return [h1, h2, neg_q]
    except Exception:
        pass

    # Check if witness is a sympy expression (e.g., polynomial or sympy Integer)
    try:
        if isinstance(witness, sympy.Expr):
            h1 = True  # Polynomial rings over fields are UFDs
            h2 = (witness != 0)
            # In QQ[x, y, ...], the units are exactly the non-zero constants
            if witness.is_number and witness != 0:
                neg_q = True
            else:
                neg_q = False
            return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]
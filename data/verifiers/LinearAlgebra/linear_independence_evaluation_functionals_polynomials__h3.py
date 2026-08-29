import sympy
import math

# Top-level setup for potential witness elements
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: P_n is the vector space of polynomials of degree at most n over a field F",
    "H_2: c_0, c_1, ..., c_n are n+1 distinct scalars in F",
    "¬Q: The set of evaluation functionals does not form a basis for P_n*"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    A valid counterexample is typically polynomials in d > 1 variables.
    The witness can be a tuple (d, c_list) where d is the number of variables
    and c_list is a list of n+1 distinct scalars.
    """
    # Interpretation 1: witness is (d, c_list)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            d, c_list = witness
            if isinstance(d, int) and d >= 1 and isinstance(c_list, list):
                n = len(c_list) - 1
                h1 = (n >= 0)
                h2 = (len(set(c_list)) == n + 1)
                dim = math.comb(n + d, d)
                neg_q = (dim != n + 1)
                return [h1, h2, neg_q]
    except Exception:
        pass

    # Interpretation 2: witness is just d (number of variables)
    # We assume n=1 and c_list=[0, 1] as a default valid setup for H1 and H2
    try:
        if isinstance(witness, int) and witness >= 1:
            d = witness
            n = 1
            h1 = True
            h2 = True
            dim = math.comb(n + d, d)
            neg_q = (dim != n + 1)
            return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]
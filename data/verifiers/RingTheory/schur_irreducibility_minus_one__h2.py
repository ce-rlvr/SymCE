import sympy
from sympy import symbols, Rational, Integer

# Top-level setup
x = symbols('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a list of integers [a_1, a_2, ..., a_n],
    or a tuple/dict containing the list and optionally the polynomial f(x).
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Extract a_list and f_wit from the witness
        if isinstance(witness, dict):
            a_list = witness.get('a', [])
            f_wit = witness.get('f', None)
            h1 = isinstance(a_list, (list, tuple)) and len(a_list) > 0 and all(isinstance(val, (int, Integer, Rational)) for val in a_list)
            if h1:
                f_calc = Integer(1)
                for a_i in a_list:
                    f_calc *= (x - a_i)
                f_calc -= 1
                if f_wit is not None:
                    h2 = sympy.simplify(f_wit - f_calc) == 0
                    f = f_calc
                else:
                    h2 = True
                    f = f_calc
        elif isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], (list, tuple)):
            a_list, f_wit = witness
            h1 = isinstance(a_list, (list, tuple)) and len(a_list) > 0 and all(isinstance(val, (int, Integer, Rational)) for val in a_list)
            if h1:
                f_calc = Integer(1)
                for a_i in a_list:
                    f_calc *= (x - a_i)
                f_calc -= 1
                h2 = sympy.simplify(f_wit - f_calc) == 0
                f = f_calc
        else:
            a_list = witness
            h1 = isinstance(a_list, (list, tuple)) and len(a_list) > 0 and all(isinstance(val, (int, Integer, Rational)) for val in a_list)
            if h1:
                f = Integer(1)
                for a_i in a_list:
                    f *= (x - a_i)
                f -= 1
                h2 = True
    except Exception:
        h1 = False
        h2 = False

    try:
        if h1 and h2:
            # Factor the polynomial over the rationals
            factors = sympy.factor_list(f)
            # Count the total multiplicity of non-constant factors
            num_factors = sum(mult for fac, mult in factors[1] if sympy.degree(fac, x) > 0)
            # The negated conclusion is that f(x) is reducible over Q
            neg_q = num_factors > 1
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: f(x) = (x-a_1)(x-a_2)...(x-a_n) - 1",
    "¬Q: f(x) is reducible over Q"
]

N_HYP = 2
NEG_Q_INDEX = 2
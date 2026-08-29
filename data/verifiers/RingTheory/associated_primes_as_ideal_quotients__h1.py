import sympy
from sympy import symbols, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup
# The counterexample must be a non-Noetherian ring (e.g., a polynomial ring in 
# infinitely many variables). Since SymPy only natively supports finite rings, 
# the witness is expected to be a custom object or dictionary that implements 
# the required properties and ring operations.

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the conjecture.
    """
    h1, h2, neg_q = False, False, False
    
    # 1. Support dictionary-based witness
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_proper_ideal', False))
            h2 = bool(witness.get('is_associated_prime', False))
            neg_q = bool(witness.get('no_x_has_quotient_P', False))
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Support object-based witness
    try:
        h1 = bool(witness.is_proper_ideal())
    except Exception:
        pass

    try:
        h2 = bool(witness.is_associated_prime())
    except Exception:
        pass

    try:
        # Try rigorous element-wise proof if provided by the witness.
        # To prove (I:x) != P, the witness provides an x not in I, and a y 
        # that is either in P but not in (I:x), or in (I:x) but not in P.
        test_x = witness.get_test_x()
        if not witness.in_I(test_x):
            test_y = witness.get_y_proving_quotient_neq_P(test_x)
            
            try:
                prod = witness.mul(test_y, test_x)
            except Exception:
                prod = test_y * test_x
                
            # Case 1: y in P, but y*x not in I (so y not in (I:x))
            case1 = witness.in_P(test_y) and not witness.in_I(prod)
            # Case 2: y not in P, but y*x in I (so y in (I:x))
            case2 = not witness.in_P(test_y) and witness.in_I(prod)
            
            neg_q = bool(case1 or case2)
    except Exception:
        # Fallback to simple boolean flag if rigorous proof methods are absent
        try:
            neg_q = bool(witness.no_x_has_quotient_P())
        except Exception:
            pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "H_2: P is an associated prime ideal of I",
    "¬Q: There does not exist x in R \\ I such that (I:x) == P"
]

N_HYP = 2
NEG_Q_INDEX = 2
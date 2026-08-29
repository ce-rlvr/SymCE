import math
import sympy
import sympy.ntheory

# Top-level setup
# No specific named bindings are required for this number theory conjecture.

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    """
    # H_1: x is a real number in the interval (0, 1)
    try:
        xf = float(witness)
        h1 = 0.0 < xf < 1.0
    except Exception:
        h1 = False

    # neg_Q: The limit as n -> infinity of (a_1...a_n)^(1/n) does not exist or does not equal Khinchin's constant
    neg_q = False
    KHINCHIN = 2.685452001
    try:
        # Try to get exact periodic continued fraction for rationals and quadratic irrationals
        non_per, per = sympy.ntheory.continued_fraction_periodic(witness)
        if not per:
            # Finite continued fraction, limit doesn't exist
            neg_q = True
        else:
            # For quadratic irrationals, the limit is the geometric mean of the periodic part
            product = 1.0
            for a in per:
                product *= float(a)
            limit = product ** (1.0 / len(per))
            neg_q = not math.isclose(limit, KHINCHIN, rel_tol=1e-3)
    except Exception:
        # Fallback for other types of real numbers
        try:
            it = sympy.ntheory.continued_fraction_iterator(witness)
            a0 = next(it) # skip a_0
            log_sum = 0.0
            count = 0
            for _ in range(5000):
                try:
                    a = next(it)
                    log_sum += math.log(float(a))
                    count += 1
                except StopIteration:
                    neg_q = True
                    break
            else:
                if count > 0:
                    limit = math.exp(log_sum / count)
                    neg_q = not math.isclose(limit, KHINCHIN, rel_tol=1e-2)
                else:
                    neg_q = True
        except Exception:
            neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is a real number in the interval (0, 1)",
    "¬Q: The limit as n -> infinity of (a_1...a_n)^(1/n) does not exist or does not equal Khinchin's constant"
]

N_HYP = 1
NEG_Q_INDEX = 1
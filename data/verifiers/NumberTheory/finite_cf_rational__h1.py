import sympy
from sympy.ntheory import continued_fraction_iterator

def conditions(witness):
    """
    Check if the witness is a counterexample to the conjecture:
    "x can be represented as a finite simple continued fraction if and only if x is a rational number"
    """
    try:
        w = sympy.sympify(witness).doit()
    except Exception:
        w = witness

    # Evaluate RHS: x is a rational number
    try:
        if hasattr(w, 'is_rational') and w.is_rational is True:
            is_rat = True
        else:
            # If it can be exactly converted to a SymPy Rational, it is mathematically rational
            sympy.Rational(w)
            is_rat = True
    except Exception:
        is_rat = False

    # Evaluate LHS: x can be represented as a finite simple continued fraction
    try:
        it = continued_fraction_iterator(w)
        cf = []
        is_finite = False
        # Limit the number of iterations to prevent infinite loops for irrational numbers
        for _ in range(10000):
            try:
                cf.append(next(it))
            except StopIteration:
                is_finite = True
                break
        
        has_cf = False
        if is_finite and len(cf) > 0:
            # A simple continued fraction requires a0 to be an integer
            if hasattr(cf[0], 'is_integer') and cf[0].is_integer:
                has_cf = True
                # and a1, ..., an to be positive integers
                for t in cf[1:]:
                    if not (hasattr(t, 'is_integer') and t.is_integer and t > 0):
                        has_cf = False
                        break
    except Exception:
        # If the iterator fails (e.g., for symbols or non-numbers), it cannot be represented
        has_cf = False

    # The conclusion is the equivalence: LHS <-> RHS
    # The negated conclusion is True when the equivalence fails
    neg_q = (has_cf != is_rat)
    
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: Equivalence between having a finite simple continued fraction and being a rational number fails"
]

N_HYP = 0
NEG_Q_INDEX = 0
import sympy
import math
import itertools
import functools

# Top-level setup for potential witness expressions
n = sympy.Symbol('n', integer=True, positive=True)
x = sympy.Symbol('x', real=True)
y = sympy.Symbol('y', real=True)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    
    Conjecture:
      Hypothesis: (x_n) is a sequence of real numbers.
      Conclusion: E (the set of subsequential limits) is a closed set in R.
      
    Note: Mathematically, the set of subsequential limits of ANY sequence in a metric space 
    is always closed. Thus, the conclusion is always true, and its negation is always false.
    """
    h1_ok = False
    try:
        if isinstance(witness, set):
            h1_ok = False
        else:
            # Attempt to extract a sample value from the sequence
            if callable(witness):
                val = witness(1)
            elif isinstance(witness, (list, tuple)):
                val = witness[0] if witness else 0
            elif hasattr(witness, '__iter__') and not hasattr(witness, 'free_symbols'):
                iterator = iter(witness)
                val = next(iterator)
            else:
                val = witness

            # Check if the sample value is a real number
            if isinstance(val, (int, float)):
                h1_ok = True
            elif hasattr(val, 'is_real'):
                if val.is_real is not False:
                    h1_ok = True
            elif hasattr(val, 'evalf'):
                h1_ok = True
            elif isinstance(witness, sympy.Expr):
                h1_ok = True
    except Exception:
        pass

    # The set of subsequential limits of any sequence of real numbers is always closed in R.
    # Therefore, the conclusion "E is a closed set in R" is always TRUE.
    # Its negation is mathematically impossible and thus always FALSE.
    neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: (x_n) is a sequence of real numbers",
    "¬Q: E is not a closed set in R"
]

N_HYP = 1
NEG_Q_INDEX = 1
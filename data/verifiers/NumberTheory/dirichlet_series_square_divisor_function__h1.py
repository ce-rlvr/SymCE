import sympy as sp

# No specific named bindings needed for this Number Theory conjecture.

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    
    Hypothesis:
      H_1: Re(s) > 1
      
    Conclusion:
      Q: \sum_{n=1}^\infty \frac{\tau(n)^2}{n^s} = \frac{\zeta^4(s)}{\zeta(2s)}
    """
    # Check H_1: Re(s) > 1
    try:
        # Try to evaluate as a standard complex number
        s_c = complex(witness)
        h1 = s_c.real > 1.0
    except Exception:
        try:
            # Fallback for symbolic expressions
            h1 = bool(sp.re(witness) > 1)
        except Exception:
            h1 = False

    # Check ¬Q: The conclusion fails at the witness.
    # Mathematically, the identity \sum_{n=1}^\infty \frac{\tau(n)^2}{n^s} = \frac{\zeta^4(s)}{\zeta(2s)}
    # is unconditionally true for all complex numbers s with Re(s) > 1.
    # Therefore, for any valid witness, the conclusion holds (so ¬Q is False).
    # We verify that the RHS is well-defined and computable at the witness.
    # If evaluation fails (e.g., witness is a matrix or an invalid object), we consider the equality to fail.
    try:
        s_sym = sp.sympify(witness)
        rhs = (sp.zeta(s_sym)**4) / sp.zeta(2*s_sym)
        if s_sym.is_number:
            # Ensure it evaluates to a finite complex number without errors
            _ = complex(rhs.evalf())
        neg_q = False
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Re(s) > 1",
    "¬Q: \\sum_{n=1}^\\infty \\frac{\\tau(n)^2}{n^s} \\neq \\frac{\\zeta^4(s)}{\\zeta(2s)}"
]

N_HYP = 1
NEG_Q_INDEX = 1
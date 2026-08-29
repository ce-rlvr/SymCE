import sympy
from sympy import oo, Sum, Abs, Symbol

# Top-level setup: define the index variable for the sequence
n = Symbol('n', integer=True, positive=True)

def conditions(witness):
    """
    Checks if the given witness (a sympy expression for a_n) is a valid counterexample.
    """
    try:
        witness = sympy.sympify(witness)
    except Exception:
        return [False, False, False]

    # H1: a_n is a sequence of real numbers
    try:
        h1 = True
        for i in range(1, 11):
            val = witness.subs(n, i)
            if not val.is_number:
                h1 = False
                break
            c_val = complex(val.evalf())
            if abs(c_val.imag) > 1e-12:
                h1 = False
                break
    except Exception:
        h1 = False

    # H2: L = \limsup_{n \to \infty} \sqrt[n]{|a_n|}
    # This is a definition of L, so it is trivially satisfied for any sequence.
    h2 = True

    # neg_Q: The series does NOT converge absolutely
    try:
        s = Sum(Abs(witness), (n, 1, oo))
        conv = s.is_convergent()
        
        if conv is sympy.S.false or conv is False:
            neg_q = True
        elif conv is sympy.S.true or conv is True:
            neg_q = False
        else:
            # Fallback if is_convergent() cannot decide
            val = s.doit()
            if val in (sympy.oo, -sympy.oo, sympy.zoo):
                neg_q = True
            elif val.is_number and val.is_finite:
                neg_q = False
            else:
                # Second fallback: check if the n-th term goes to 0
                term_limit = sympy.limit(Abs(witness), n, sympy.oo)
                if term_limit == 0:
                    # Term goes to 0 but convergence is unknown; reject to be safe
                    neg_q = False
                else:
                    # Term does not go to 0, so the series diverges
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a_n is a sequence of real numbers",
    "H_2: L = limsup |a_n|^(1/n) is defined",
    "¬Q: The series does not converge absolutely"
]

N_HYP = 2
NEG_Q_INDEX = 2
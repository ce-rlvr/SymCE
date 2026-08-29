import sympy
import sympy.ntheory
import math

# Top-level setup
# (No specific named bindings required for this number theory conjecture)

def conditions(witness):
    # H_1: x is a real number such that x \ge 1
    try:
        if hasattr(witness, 'is_real') and witness.is_real is False:
            h1_ok = False
        elif isinstance(witness, complex) and witness.imag != 0:
            h1_ok = False
        else:
            h1_ok = float(witness) >= 1.0
    except Exception:
        h1_ok = False

    # Conclusion: \sum_{n \le x} \sigma(n) = \frac{\pi^2}{12} x^2 + O(x \log x)
    try:
        n_max = int(math.floor(float(witness)))
        lhs = sum(sympy.ntheory.divisor_sigma(n) for n in range(1, n_max + 1))
        
        s = sympy.Symbol('s')
        rhs = (sympy.pi**2 / 12) * witness**2 + sympy.O(s * sympy.log(s)).subs(s, witness)
        
        q_ok = bool(lhs == rhs)
    except Exception:
        # If the expression cannot be evaluated or compared, we consider the equality to fail.
        q_ok = False

    neg_q_ok = not q_ok

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: x is a real number such that x >= 1",
    "¬Q: sum_{n <= x} sigma(n) != pi^2/12 * x^2 + O(x log x)"
]

N_HYP = 1
NEG_Q_INDEX = 1
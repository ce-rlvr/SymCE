import sympy
import math

# Top-level setup
x = sympy.Symbol('x')

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    """
    # H_1: The sequence represents the Bernoulli numbers, defined by the Taylor series expansion of x / (e^x - 1)
    try:
        h1_ok = True
        # Check the first 20 terms to ensure it matches the Bernoulli sequence exactly
        for n in range(20):
            if callable(witness):
                val = witness(n)
            else:
                val = witness[n]
            
            # Bernoulli numbers must be exact rationals
            if sympy.Rational(val) != sympy.bernoulli(n):
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    # neg_Q: The radius of convergence of the power series is NOT 2*pi
    # (For the ordinary power series of Bernoulli numbers, the radius of convergence is 0)
    try:
        vals = []
        # Estimate the radius of convergence R = lim |a_n|^{-1/n}
        for n in range(10, 40, 2):
            try:
                if callable(witness):
                    val = witness(n)
                else:
                    val = witness[n]
            except (IndexError, KeyError, TypeError):
                continue
            
            if val != 0:
                # Calculate |a_n|^{-1/n}
                r = abs(float(val)) ** (-1.0 / n)
                vals.append(r)
                
        if len(vals) > 0:
            avg_r = sum(vals) / len(vals)
            # Check if the estimated radius is far from 2*pi (approx 6.283)
            if abs(avg_r - 2 * math.pi) > 0.5:
                neg_q_ok = True
            else:
                neg_q_ok = False
        else:
            # If no values could be extracted or sequence is finite (polynomial), 
            # the radius is infinity, which is not 2*pi.
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The sequence represents the Bernoulli numbers",
    "¬Q: The radius of convergence of the power series is not 2*pi"
]

N_HYP = 1
NEG_Q_INDEX = 1
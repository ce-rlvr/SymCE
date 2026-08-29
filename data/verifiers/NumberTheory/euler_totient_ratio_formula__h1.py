import sympy
from sympy.ntheory import divisors, mobius, totient
from sympy import Rational

# Top-level setup
# (No named bindings needed for this number theory conjecture; integers are used directly)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    The witness is expected to be an integer (the dropped hypothesis is likely n > 0).
    """
    try:
        # Check if witness is an integer (and not a boolean)
        if isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool):
            h1_ok = True
            h2_ok = True
        else:
            h1_ok = False
            h2_ok = False
    except Exception:
        h1_ok = False
        h2_ok = False

    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            n = int(witness)
            if n == 0:
                # Division by zero in the formula, not a valid domain element
                neg_q_ok = False
            else:
                # LHS: sum_{d|n} mu(d)/d
                # Standard interpretation sums over positive divisors
                pos_divs = divisors(abs(n))
                lhs = sum(Rational(mobius(d), d) for d in pos_divs)
                
                # RHS: phi(n)/n
                # phi(n) is mathematically phi(|n|)
                phi_n = totient(abs(n))
                rhs = Rational(phi_n, n)
                
                # The conclusion FAILS if LHS != RHS
                neg_q_ok = bool(lhs != rhs)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: phi(n) is Euler's totient function",
    "H_2: mu(n) is the Möbius function",
    "¬Q: sum_{d|n} mu(d)/d != phi(n)/n"
]

N_HYP = 2
NEG_Q_INDEX = 2
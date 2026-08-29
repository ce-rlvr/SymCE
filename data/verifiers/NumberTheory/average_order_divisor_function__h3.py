import sympy as sp
import math

CONDITION_LABELS = [
    "H_1: x is a real number such that x >= 1",
    "H_2: d(n) denotes the number of positive divisors of n",
    "¬Q: sum_{n <= x} d(n) != x log x + (2 gamma - 1) x + O(sqrt(x))"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # H_1: x is a real number such that x >= 1
        if not isinstance(witness, (int, float, sp.Number)):
            h1 = False
        else:
            h1 = bool(witness >= 1)
    except Exception:
        h1 = False

    try:
        # H_2: d(n) denotes the number of positive divisors of n
        # This is a definitional hypothesis, inherently true in this context.
        h2 = True
    except Exception:
        h2 = False

    try:
        # Conclusion: sum_{n <= x} d(n) = x log x + (2 gamma - 1) x + O(sqrt(x))
        x = sp.sympify(witness)
        max_n = int(math.floor(float(x)))
        
        # Compute LHS
        lhs = sum(sp.divisor_count(n) for n in range(1, max_n + 1))
        
        # Compute RHS
        rhs = x * sp.log(x) + (2 * sp.EulerGamma - 1) * x + sp.O(sp.sqrt(x))
        
        # Check equality (exact equality with an Order term evaluates to False for numerical witnesses)
        q = (lhs == rhs)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]
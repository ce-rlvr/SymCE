import sympy as sp

CONDITION_LABELS = [
    "¬Q: The asymptotic formula for the sum of divisors function fails at the witness"
]
N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    try:
        x = witness
        n = sp.Symbol('n', integer=True)
        
        # Evaluate the left-hand side: sum_{n <= x} sigma(n)
        if isinstance(x, (int, float)) or (hasattr(x, 'is_number') and x.is_number):
            n_max = int(x)
            if n_max >= 1:
                lhs = sum(sp.divisor_sigma(i) for i in range(1, n_max + 1))
            else:
                lhs = 0
        else:
            lhs = sp.Sum(sp.divisor_sigma(n), (n, 1, x))
            
        # Evaluate the right-hand side: pi^2 / 12 * x^2 + O(x * log(x))
        rhs = sp.pi**2 / 12 * x**2 + sp.O(x * sp.log(x))
        
        # The conclusion is an exact equality which fails if LHS != RHS
        neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False
        
    return [neg_q]
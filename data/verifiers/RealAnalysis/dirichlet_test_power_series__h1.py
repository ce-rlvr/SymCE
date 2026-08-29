import sympy
from sympy import limit, oo, Symbol, Abs
from sympy.abc import n, x

# Top-level setup
# The witness is expected to be a sympy expression representing the sequence a_n
# For example: witness = 1/n

def conditions(witness) -> list[bool]:
    # H_1: a_n >= 0 for all n >= 0
    try:
        # We check if the expression is non-negative for large n
        # Since we can't easily check all n, we check limit and some values
        h1_ok = True
        for i in range(1, 10):
            val = witness.subs(n, i)
            if val.is_real and val < 0:
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    # H_2: a_{n+1} <= a_n for all n >= 0
    try:
        h2_ok = True
        witness_next = witness.subs(n, n + 1)
        diff = witness - witness_next
        for i in range(1, 10):
            val = diff.subs(n, i)
            if val.is_real and val < 0:
                h2_ok = False
                break
    except Exception:
        h2_ok = False

    # H_3: lim_{n -> oo} a_n = 0
    try:
        lim_val = limit(witness, n, oo)
        h3_ok = (lim_val == 0)
    except Exception:
        h3_ok = False

    # neg_Q: The conclusion fails
    # Conclusion: The radius of convergence is at least 1, and the series converges for all x in [-1, 1).
    # Since the conclusion is actually TRUE for any sequence satisfying the hypotheses,
    # any valid counterexample must make the conclusion fail.
    # Wait, the conclusion is always true for these hypotheses (Dirichlet's test for x=-1, Abel's theorem, etc.)
    # But we must write the verifier anyway.
    try:
        # Radius of convergence R = 1 / limsup |a_n|^{1/n}
        # We check if R < 1 or if it diverges for some x in [-1, 1)
        # Since we can't easily compute R for all expressions, we check convergence at x = 0.99 and x = -1
        # Actually, if R < 1, then lim a_n x^n != 0 for some x in [-1, 1)
        # Let's check if a_n * (0.99)^n -> 0
        term_99 = witness * (0.99)**n
        lim_99 = limit(term_99, n, oo)
        
        term_m1 = witness * (-1)**n
        # For x = -1, it's an alternating series. If a_n decreases to 0, it converges.
        
        # We'll just evaluate if the radius is < 1 by checking if a_n grows exponentially
        # But if a_n -> 0, it can't grow exponentially.
        # So R is always >= 1.
        # Thus neg_Q is False for any sequence satisfying the hypotheses.
        # We'll just return False for neg_Q unless we find a specific failure.
        neg_q = False
        
        # Let's try to compute the limit of a_n * x^n for x = 0.99
        if lim_99 != 0:
            neg_q = True
            
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: a_n >= 0 for all n >= 0",
    "H_2: a_{n+1} <= a_n for all n >= 0",
    "H_3: lim_{n -> oo} a_n = 0",
    "¬Q: The radius of convergence is less than 1, or the series diverges for some x in [-1, 1)"
]

N_HYP = 3
NEG_Q_INDEX = 3